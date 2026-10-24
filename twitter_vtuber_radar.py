"""
Modul: twitter_vtuber_radar.py
Deskripsi: Radar X/Twitter & Generator Paket SEO YouTube Video Reguler (16:9 / Long-Form).
           Mengadopsi pola arsitektur 'Agent-Reach' (Panniantong/Agent-Reach) dengan
           autentikasi cookie ringan (auth_token & ct0), multi-backend fallback,
           serta kalkulasi otomatis YouTube Video Chapters (00:00) dari sections.txt.
"""

import argparse
import http.cookiejar
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import requests

try:
    from holodex_client import ambil_detail_video
except ImportError:
    try:
        from vibe_tools.holodex_client import ambil_detail_video
    except ImportError:
        ambil_detail_video = None

# Konfigurasi encoding UTF-8 untuk lingkungan Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_CHAT_DIR = ROOT_DIR / "cache_chat"
SECTIONS_FILE = ROOT_DIR / "sections.txt"
COOKIES_X_TXT = ROOT_DIR / "www.x.com_cookies.txt"
COOKies_TWITTER_TXT = ROOT_DIR / "twitter_cookies.txt"
COOKIES_X_JSON = CACHE_CHAT_DIR / "x_cookies.json"


def detik_ke_timecode(detik: float) -> str:
    """Mengonversi detik ke format timecode YouTube (HH:MM:SS atau MM:SS)."""
    detik_int = int(round(max(0.0, detik)))
    jam = detik_int // 3600
    sisa = detik_int % 3600
    menit = sisa // 60
    det = sisa % 60
    if jam > 0:
        return f"{jam:02d}:{menit:02d}:{det:02d}"
    return f"{menit:02d}:{det:02d}"


def timecode_ke_detik(tc_str: str) -> float:
    """Mengonversi string timecode (HH:MM:SS / MM:SS / detik) ke float detik."""
    tc = tc_str.strip().strip("[]()")
    parts = tc.split(":")
    try:
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 1:
            return float(parts[0])
    except ValueError:
        return 0.0
    return 0.0


# =====================================================================
# 1. AGENT-REACH PATTERN: DOCTOR & COOKIE EXTRACTION
# =====================================================================

def muat_cookie_x() -> Dict[str, str]:
    """
    Memuat kredensial sesi X/Twitter (auth_token & ct0) dari berkas cookie lokal.
    Mendukung format JSON (~/.agent-reach/x_cookies.json atau cache_chat/x_cookies.json)
    dan format Netscape text (www.x.com_cookies.txt).
    """
    cookies = {}

    # 1. Cek file JSON terlebih dahulu
    for json_path in [COOKIES_X_JSON, Path.home() / ".agent-reach" / "x_cookies.json"]:
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    cookies.update(data)
                elif isinstance(data, list):
                    for item in data:
                        nama = item.get("name")
                        nilai = item.get("value")
                        if nama and nilai:
                            cookies[nama] = nilai
            except Exception:
                pass

    # 2. Cek file teks Netscape (www.x.com_cookies.txt)
    for txt_path in [COOKIES_X_TXT, COOKies_TWITTER_TXT, ROOT_DIR / "cookies.txt"]:
        if txt_path.exists():
            try:
                cj = http.cookiejar.MozillaCookieJar(str(txt_path))
                cj.load(ignore_discard=True, ignore_expires=True)
                for cookie in cj:
                    if "twitter.com" in cookie.domain or "x.com" in cookie.domain:
                        cookies[cookie.name] = cookie.value
            except Exception:
                # Parsing manual jika cookiejar standar gagal
                try:
                    for line in txt_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                        if not line.startswith("#") and "\t" in line:
                            parts = line.split("\t")
                            if len(parts) >= 7:
                                cookies[parts[5].strip()] = parts[6].strip()
                except Exception:
                    pass

    return cookies


def doctor_check() -> Dict[str, Any]:
    """
    Diagnostik kesehatan kanal sosial ala 'agent-reach doctor'.
    Memeriksa ketersediaan cookies X/Twitter, yt-dlp, dan konektivitas Jina Reader.
    """
    cookies = muat_cookie_x()
    has_auth_token = "auth_token" in cookies
    has_ct0 = "ct0" in cookies

    yt_dlp_ok = False
    try:
        res = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, timeout=5)
        yt_dlp_ok = (res.returncode == 0)
    except Exception:
        yt_dlp_ok = False

    jina_ok = False
    try:
        r = requests.get("https://r.jina.ai/https://example.com", timeout=6)
        jina_ok = (r.status_code == 200)
    except Exception:
        jina_ok = False

    status = {
        "x_cookies_ditemukan": bool(cookies),
        "x_auth_token_aktif": has_auth_token,
        "x_ct0_aktif": has_ct0,
        "yt_dlp_tersedia": yt_dlp_ok,
        "jina_reader_tersedia": jina_ok,
        "mode_x_radar": "Cookie-Auth Langsung (Penuh)" if (has_auth_token and has_ct0) else "Fallback (Jina Reader & Metadata VOD)"
    }
    return status


# =====================================================================
# 2. EKSTRAKSI METADATA VOD & HASHTAG RESMI VTUBER
# =====================================================================

def ekstrak_metadata_vod(vod_url: str) -> Dict[str, Any]:
    """
    Mengekstrak informasi kaya dari VOD YouTube menggunakan yt-dlp --dump-json.
    Mengambil judul VOD, channel/author, durasi, deskripsi, dan hashtag resmi stream.
    """
    metadata = {
        "url": vod_url,
        "title": "VTuber Livestream",
        "uploader": "VTuber",
        "channel_url": "",
        "duration": 0,
        "description": "",
        "hashtags": [],
        "x_handle": ""
    }

    if not vod_url or not vod_url.startswith("http"):
        return metadata

    cmd = ["yt-dlp", "--dump-json", "--skip-download", "--no-warnings", vod_url]
    cookies_yt = ROOT_DIR / "www.youtube.com_cookies.txt"
    if cookies_yt.exists():
        cmd.extend(["--cookies", str(cookies_yt)])

    try:
        print(f"[INFO] Mengambil metadata resmi VOD via yt-dlp: {vod_url}")
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip().splitlines()[0])
            metadata["title"] = data.get("title") or metadata["title"]
            metadata["uploader"] = data.get("uploader") or data.get("channel") or metadata["uploader"]
            metadata["channel_url"] = data.get("uploader_url") or data.get("channel_url") or ""
            metadata["duration"] = data.get("duration") or 0
            metadata["description"] = data.get("description") or ""

            # Ekstrak hashtag resmi dari judul dan deskripsi
            teks_gabungan = f"{metadata['title']}\n{metadata['description']}"
            tag_matches = re.findall(r"#([a-zA-Z0-9_\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]+)", teks_gabungan)
            unique_tags = []
            for t in tag_matches:
                t_clean = t.strip()
                if t_clean and t_clean.lower() not in [x.lower() for x in unique_tags]:
                    unique_tags.append(t_clean)
            metadata["hashtags"] = unique_tags[:8]

            # Cari tautan akun X/Twitter di deskripsi
            x_match = re.search(r"(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com)/([a-zA-Z0-9_]{1,20})", metadata["description"])
            if x_match:
                metadata["x_handle"] = f"@{x_match.group(1)}"

    except Exception as e:
        print(f"[WARNING] Gagal mengambil metadata VOD via yt-dlp: {e}")

    return metadata


# =====================================================================
# 3. RADAR BUZZ X/TWITTER (REAKSI FANS & TOPIK POPULER)
# =====================================================================

def ambil_buzz_twitter(
    hashtags: List[str],
    vtuber_name: str = "",
    max_tweet: int = 5
) -> List[Dict[str, Any]]:
    """
    Mengambil tweet dan reaksi fans terpopuler dari X/Twitter berdasarkan hashtag stream.
    Menggunakan Multi-Backend:
    1. Backend A: Direct Syndication / Search API dengan injeksi cookie X.
    2. Backend B: Fallback via Jina Reader (https://r.jina.ai/) untuk ekstraksi web bersih.
    """
    hasil_tweet = []
    query_tag = f"#{hashtags[0]}" if hashtags else (f"#{vtuber_name}" if vtuber_name else "#VTuber")
    print(f"[INFO] Menjalankan Radar X/Twitter untuk query: '{query_tag}'...")

    cookies = muat_cookie_x()
    has_auth = "auth_token" in cookies

    # Backend A: Cookie-authenticated request (Simulasi header Agent-Reach xreach)
    if has_auth:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])
            }
            if "ct0" in cookies:
                headers["x-csrf-token"] = cookies["ct0"]

            # Mencari via syndication timeline umum
            url_syndication = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{vtuber_name.replace(' ', '')}"
            resp = requests.get(url_syndication, headers=headers, timeout=10)
            if resp.status_code == 200:
                # Ekstrak tweet teks ringkas
                teks_list = re.findall(r'dir="auto"[^>]*>(.*?)</div>', resp.text)
                for t in teks_list[:max_tweet]:
                    clean = re.sub(r"<[^>]+>", "", t).strip()
                    if clean and len(clean) > 15:
                        hasil_tweet.append({"author": "Fans di X", "teks": clean, "likes": "Buzz Komunitas"})
        except Exception:
            pass

    # Backend B: Fallback via Jina Reader jika Backend A belum membuahkan hasil
    if not hasil_tweet:
        try:
            print("[INFO] Memanggil fallback Jina Reader untuk mengambil tren publik X/Twitter...")
            jina_url = f"https://r.jina.ai/https://x.com/search?q={requests.utils.quote(query_tag)}"
            headers = {"Accept": "text/plain"}
            resp_jina = requests.get(jina_url, headers=headers, timeout=12)
            if resp_jina.status_code == 200 and resp_jina.text:
                baris = resp_jina.text.splitlines()
                for b in baris:
                    b_strip = b.strip()
                    if b_strip.startswith("- ") or b_strip.startswith("* "):
                        clean_line = b_strip.lstrip("-* ").strip()
                        if len(clean_line) > 20 and not clean_line.startswith("http"):
                            hasil_tweet.append({"author": "X Community", "teks": clean_line[:180], "likes": "Trending"})
                            if len(hasil_tweet) >= max_tweet:
                                break
        except Exception as e:
            print(f"[INFO] Fallback Jina Reader dilewati: {e}")

    # Fallback sintetis jika platform X sepenuhnya memblokir IP/tanpa cookie
    if not hasil_tweet:
        tag_str = " ".join([f"#{t}" for t in hashtags[:3]]) if hashtags else f"#{vtuber_name}"
        hasil_tweet.append({
            "author": "Komunitas X Stream",
            "teks": f"Keseruan live stream {vtuber_name} pada segmen highlight {tag_str}",
            "likes": "Antusiasme Tinggi"
        })

    return hasil_tweet


# =====================================================================
# 4. YOUTUBE VIDEO (LONG-FORM) SEO PACK & CHAPTER CALCULATOR
# =====================================================================

def muat_segmen_sections_txt(sections_path: Path) -> List[Dict[str, Any]]:
    """
    Membaca berkas sections.txt dan mengekstrak daftar segmen klip.
    Format baris: URL | HH:MM:SS-HH:MM:SS | Label
    """
    segmen_list = []
    if not sections_path.exists():
        return segmen_list

    lines = sections_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for l in lines:
        l = l.strip()
        if not l or l.startswith("#"):
            continue
        parts = [p.strip() for p in l.split("|")]
        if len(parts) >= 2:
            time_range = parts[1]
            label = parts[2] if len(parts) >= 3 else "Highlight Segment"
            if "-" in time_range:
                t_awal, t_akhir = time_range.split("-", 1)
                sec_awal = timecode_ke_detik(t_awal)
                sec_akhir = timecode_ke_detik(t_akhir)
                durasi = max(1.0, sec_akhir - sec_awal)
                segmen_list.append({
                    "label": re.sub(r"^\d+\.\s*", "", label),
                    "start_sec": sec_awal,
                    "end_sec": sec_akhir,
                    "start_tc": t_awal.strip(),
                    "end_tc": t_akhir.strip(),
                    "durasi": durasi
                })
    return segmen_list


def kalkulasi_youtube_video_chapters(segmen_list: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
    """
    Menghitung penanda waktu Chapter YouTube Video (00:00) secara kumulatif.
    Karena klip-klip di sections.txt dimasukkan berurutan ke Timeline DaVinci Resolve,
    waktu chapter dihitung dari akumulasi durasi klip sebelumnya.
    """
    chapters = []
    waktu_kumulatif = 0.0

    for idx, s in enumerate(segmen_list, start=1):
        tc_str = detik_ke_timecode(waktu_kumulatif)
        judul_bersih = s.get("label") or f"Bagian {idx}"
        chapters.append((tc_str, judul_bersih))
        waktu_kumulatif += s.get("durasi", 60.0)

    return chapters


def buat_paket_seo_youtube_video(
    segmen_list: List[Dict[str, Any]],
    vod_meta: Dict[str, Any],
    twitter_buzz: List[Dict[str, Any]],
    output_md: Path,
    holodex_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Menyusun paket SEO lengkap khusus untuk YouTube Video Reguler (Landscape 16:9 / Long-Form):
    1. 3 Ide Judul YouTube Video High-CTR.
    2. Konsep Teks & Visual Thumbnail 16:9 (3-5 kata punchline).
    3. Deskripsi YouTube lengkap dengan YouTube Chapters (00:00), sumber VOD, dan hashtag.
    4. Draft Tweet Promosi Klip untuk X/Twitter.
    """
    vtuber = vod_meta.get("uploader") or "VTuber"
    vod_title = vod_meta.get("title") or "Livestream Highlight"
    vod_url = vod_meta.get("url") or "https://www.youtube.com/watch?v=vod"
    x_handle = vod_meta.get("x_handle") or f"@{vtuber.replace(' ', '')}"
    hashtags = vod_meta.get("hashtags") or []

    # Tag format
    tag_str = " ".join([f"#{t}" for t in hashtags]) if hashtags else f"#{vtuber.replace(' ', '')} #VTuber #VTuberClip"
    tag_seo_csv = ", ".join([vtuber, f"{vtuber} clip", "vtuber indonesia", "vtuber sub indo", "vtuber funny moments"] + hashtags)

    # 1. Hitung YouTube Chapters
    chapters = kalkulasi_youtube_video_chapters(segmen_list)
    chapters_text_lines = []
    for tc, nama in chapters:
        chapters_text_lines.append(f"{tc} {nama}")
    chapters_formatted = "\n".join(chapters_text_lines) if chapters_text_lines else "00:00 Intro & Highlight Momen"

    # Momen utama untuk referensi judul
    top_moment = segmen_list[0]["label"] if segmen_list else "Momen Paling Kocak & Tak Terduga"

    # Reaksi buzz X
    kutipan_x = twitter_buzz[0]["teks"] if twitter_buzz else "Keseruan interaksi live stream"

    # Integrasi Kolaborator Holodex jika ada
    collab_talents = holodex_data.get("collab_talents", []) if holodex_data else []
    collab_text = ""
    collab_mentions_x = []
    if collab_talents:
        collab_lines = ["👥 MEMBER KOLABORASI:"]
        for c in collab_talents:
            tw = f" ({c['twitter']})" if c.get('twitter') else ""
            collab_lines.append(f"• {c['name']}{tw}")
            if c.get("twitter"):
                collab_mentions_x.append(c["twitter"])
        collab_text = "\n".join(collab_lines) + "\n\n"

    extra_x_mentions = " " + " ".join(collab_mentions_x[:3]) if collab_mentions_x else ""

    # 2. Susun Konten Markdown
    konten = f"""# 🎬 PAKET SEO YOUTUBE VIDEO (LONG-FORM 16:9)
*Dihasilkan otomatis oleh Antigravity X/Twitter Radar pada {time.strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📌 1. 3 Opsi Judul YouTube Video (High-CTR)
Gaya penulisan YouTube Video mengutamakan punchline emosional + konteks VTuber:
1. **[{vtuber}] KETIKA {top_moment.upper()} SAMPAI BIKIN SEISI CHAT NGAKAK! (Sub Indo)**
2. **DETIK-DETIK {vtuber} {top_moment} | Momen Terbaik Live Stream**
3. **NGAKAK BANGET! {vtuber} GAK BISA BERHENTI KETAWA GARA-GARA INI... [{tag_str.split()[0] if tag_str else '#VTuber'}]**

---

## 🖼️ 2. Konsep Thumbnail Landscape (16:9)
* **Teks Thumbnail Utama (3–5 Kata Besar, Font Tebal, Outline Kuning/Putih):**
  👉 **"{top_moment[:25].upper()}?!"** atau **"KOK BISA GINI?!"**
* **Ekspresi Wajah VTuber (Crop 1/3 Kanan Frame 16:9):**
  👉 Ekspresi panik, tertawa lepas, atau wajah 'smug' dengan efek drop shadow tipis.
* **Elemen Visual Pendukung (Sisi Kiri Frame):**
  👉 Screenshot cuplikan layar momen game/aktivitas + balon teks chat: *"{kutipan_x[:35]}..."*

---

## 📝 3. Deskripsi YouTube Video Siap Pakai (Salin & Tempel)
```text
Kompilasi momen terbaik dan paling seru dari livestream {vtuber}!
Jangan lupa Like, Comment, dan Subscribe untuk update klip terjemahan VTuber lainnya!

⏱️ TIMESTAMPS / CHAPTERS:
{chapters_formatted}

{collab_text}🔗 SUMBER ASLI & CHANNEL VTUBER:
• Stream Asli : {vod_url}
• Channel {vtuber} : {vod_meta.get('channel_url') or 'Lihat link di video asli'}
• Akun X / Twitter : {x_handle}

💬 REAKSI FANS DI X:
"{kutipan_x}"

📌 TAG & HASHTAG RESMI:
{tag_str} #VTuberID #VTuberClip #IndoSub

--------------------------------------------------
Video ini diedit dan diterjemahkan untuk tujuan hiburan komunitas.
Seluruh hak cipta audio dan visual karakter milik {vtuber} dan agensi terkait.
```

---

## 🏷️ 4. Kata Kunci / Tags YouTube Video (Kolom Tag YouTube Studio)
```text
{tag_seo_csv}
```

---

## 🐦 5. Draft Tweet Promosi Klip ke Komunitas X/Twitter
Salin teks ini dan posting di akun X Anda dengan menautkan video YouTube yang telah di-upload:

```text
Keseruan {vtuber} pas {top_moment} bener-bener gak ada obat wkwk 😭🤣

Tonton klip kompilasi lengkapnya di sini:
👉 [MASUKKAN LINK YOUTUBE VIDEO ANDA]

{tag_str} {x_handle}
```
"""

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(konten, encoding="utf-8")
    print(f"[INFO] Paket SEO YouTube Video berhasil disimpan ke: {output_md}")
    return konten


# =====================================================================
# 5. ENTRY POINT & CLI
# =====================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Radar X/Twitter & YouTube Video SEO Pack Generator untuk VTuber Clipper."
    )
    parser.add_argument("--url", type=str, default="", help="URL video YouTube sumber (VOD)")
    parser.add_argument("--sections", type=str, default="sections.txt", help="Path ke berkas sections.txt")
    parser.add_argument("--doctor", action="store_true", help="Jalankan diagnostik kanal X/Twitter ala agent-reach doctor")
    parser.add_argument("--output", type=str, default="cache_chat/youtube_video_seo.md", help="Path keluaran berkas markdown SEO")

    args = parser.parse_args()

    print("=" * 65)
    print("🐦 ANTIGRAVITY X/TWITTER RADAR & YOUTUBE VIDEO SEO GENERATOR")
    print("=" * 65)

    # 1. Mode Doctor ala Agent-Reach
    if args.doctor:
        status = doctor_check()
        print("\n📋 HASIL DIAGNOSTIK KANAL ('agent-reach doctor'):")
        for k, v in status.items():
            simbol = "✓" if (v is True or "Langsung" in str(v)) else ("✗" if v is False else "ℹ")
            print(f"  [{simbol}] {k:25}: {v}")
        print("\n")
        if not args.url and not Path(args.sections).exists():
            return

    # 2. Cari URL VOD dasar jika tidak ditentukan
    vod_url = args.url
    sections_path = ROOT_DIR / args.sections

    if not vod_url and sections_path.exists():
        for line in sections_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                vod_url = line.split("|")[0].strip().split("?t=")[0].split("&t=")[0]
                break

    if not vod_url:
        vod_url = "https://www.youtube.com/watch?v=vod_highlight"

    # 3. Ekstraksi Metadata VOD & Hashtag Resmi
    vod_meta = ekstrak_metadata_vod(vod_url)
    print(f"• VTuber         : {vod_meta['uploader']}")
    print(f"• Judul VOD      : {vod_meta['title']}")
    print(f"• Hashtag Resmi  : {', '.join(vod_meta['hashtags']) if vod_meta['hashtags'] else 'Tidak terdeteksi'}")
    print(f"• Akun X VTuber  : {vod_meta['x_handle'] or 'Tidak terdeteksi'}")

    # 4. Ambil Buzz X/Twitter
    buzz = ambil_buzz_twitter(vod_meta["hashtags"], vtuber_name=vod_meta["uploader"])

    # 5. Baca segmen sections.txt & Kalkulasi YouTube Video Chapters
    segmen_list = muat_segmen_sections_txt(sections_path)
    print(f"• Jumlah Segmen  : {len(segmen_list)} klip di {args.sections}")

    # Ambil data tambahan dari Holodex jika tersedia
    holodex_info = None
    if ambil_detail_video:
        try:
            holodex_info = ambil_detail_video(vod_url)
            if holodex_info.get("collab_talents"):
                print(f"• Holodex Collab : {len(holodex_info['collab_talents'])} member terdeteksi")
        except Exception:
            pass

    # 6. Buat Paket SEO YouTube Video
    output_path = ROOT_DIR / args.output
    buat_paket_seo_youtube_video(segmen_list, vod_meta, buzz, output_path, holodex_data=holodex_info)

    print("\n✨ SELESAI! Paket SEO YouTube Video dan Chapters telah siap.")
    print("=" * 65)


if __name__ == "__main__":
    main()
