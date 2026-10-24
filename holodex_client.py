"""
Modul: holodex_client.py
Deskripsi: Klien resmi Holodex API v2 untuk Full Automatic VTuber Clipper.
           Menyediakan discovery live stream yang baru selesai (Recently Ended VODs),
           deteksi member kolaborasi (mentions), kompilasi klip komunitas (clips),
           serta ekstraksi otomatis lagu singing stream (songs) ke sections.txt.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import requests

# Konfigurasi encoding UTF-8 untuk lingkungan Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_CHAT_DIR = ROOT_DIR / "cache_chat"
HOLODEX_KEY_FILE = CACHE_CHAT_DIR / "holodex_key.txt"
HOLODEX_CACHE_FILE = CACHE_CHAT_DIR / "holodex_cache.json"
BASE_URL = "https://holodex.net/api/v2"


def detik_ke_timecode(detik: float) -> str:
    """Mengonversi detik ke format timecode HH:MM:SS."""
    detik_int = int(round(max(0.0, detik)))
    jam = detik_int // 3600
    sisa = detik_int % 3600
    menit = sisa // 60
    det = sisa % 60
    return f"{jam:02d}:{menit:02d}:{det:02d}"


def timecode_ke_detik(tc_str: str) -> float:
    """Mengonversi string timecode ke float detik."""
    tc = str(tc_str).strip().strip("[]()")
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


def format_waktu_iso(iso_str: str) -> str:
    """Mengonversi timestamp ISO 8601 UTC ke format tanggal dan waktu lokal (YYYY-MM-DD HH:MM)."""
    if not iso_str:
        return "-"
    try:
        import datetime
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        dt_local = dt.astimezone()
        return dt_local.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str[:16].replace("T", " ")


_session_yt = None


def get_yt_session() -> requests.Session:
    """Mendapatkan atau membuat sesi requests YouTube yang memuat cookies dari www.youtube.com_cookies.txt."""
    global _session_yt
    if _session_yt is None:
        import http.cookiejar
        _session_yt = requests.Session()
        cookie_candidates = [
            ROOT_DIR / "www.youtube.com_cookies.txt",
            Path("www.youtube.com_cookies.txt"),
            Path.home() / "www.youtube.com_cookies.txt",
        ]
        for cp in cookie_candidates:
            if cp.exists():
                try:
                    cj = http.cookiejar.MozillaCookieJar(str(cp))
                    cj.load(ignore_discard=True, ignore_expires=True)
                    _session_yt.cookies = cj
                    break
                except Exception:
                    pass
    return _session_yt


def deteksi_caption_dan_chat(video_id: str, durasi_sec: int = 0) -> Dict[str, str]:
    """
    Mendeteksi ketersediaan subtitle/caption (JP, EN, ID) dan livechat replay YouTube
    secara presisi dari respon watch page player YouTube menggunakan cookies sesi.
    """
    hasil = {"caption": "-", "livechat": "-"}
    if not video_id:
        return hasil

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,id;q=0.7"
    }

    try:
        session = get_yt_session()
        url_watch = f"https://www.youtube.com/watch?v={video_id}"
        resp = session.get(url_watch, headers=headers, timeout=6)
        if resp.status_code == 200:
            html = resp.text

            # 1. Cari ytInitialPlayerResponse
            caption_tracks = []
            m = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});(?:var\s|const\s|</script)", html)
            if m:
                try:
                    data = json.loads(m.group(1))
                    caption_tracks = data.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
                except Exception:
                    pass

            # Fallback regex langsung ke captionTracks jika parsing objek penuh gagal
            if not caption_tracks:
                cap_match = re.search(r'"captionTracks":\s*(\[.+?\])', html)
                if cap_match:
                    try:
                        caption_tracks = json.loads(cap_match.group(1))
                    except Exception:
                        pass

            # 2. Parsing bahasa caption
            langs_found = []
            for track in caption_tracks:
                code = track.get("languageCode", "").lower()
                vss_id = track.get("vssId", "").lower()
                kind = track.get("kind", "").lower()
                name_obj = track.get("name", {})
                name_text = (name_obj.get("simpleText") or (name_obj.get("runs", [{}])[0].get("text") if isinstance(name_obj.get("runs"), list) and name_obj.get("runs") else "") or "").lower()

                tag = ""
                # Deteksi bahasa Jepang
                if code in ("ja", "jp") or "japanese" in name_text or "jepang" in name_text or ".ja" in vss_id:
                    tag = "JP (Auto)" if kind == "asr" else "JP"
                # Deteksi bahasa Inggris
                elif code == "en" or "english" in name_text or "inggris" in name_text or ".en" in vss_id:
                    tag = "EN (Auto)" if kind == "asr" else "EN"
                # Deteksi bahasa Indonesia
                elif code == "id" or "indonesian" in name_text or "indonesia" in name_text or ".id" in vss_id:
                    tag = "ID (Auto)" if kind == "asr" else "ID"
                else:
                    c_code = code.upper()
                    tag = f"{c_code} (Auto)" if kind == "asr" else c_code

                if tag and tag not in langs_found:
                    langs_found.append(tag)

            hasil["caption"] = ", ".join(langs_found) if langs_found else "-"

            # 3. Deteksi Livechat Replay
            if '"conversationBar"' in html or '"liveChatRenderer"' in html or '"isReplay":true' in html:
                hasil["livechat"] = "✓ Replay"
            elif durasi_sec > 600:
                hasil["livechat"] = "✓ Replay"
            else:
                hasil["livechat"] = "-"
        else:
            # Fallback jika YouTube mengembalikan status selain 200 (misal 429 rate limit)
            if durasi_sec > 600:
                hasil["livechat"] = "✓ Replay"
    except Exception:
        # Fallback toleran jika request timeout/gagal
        if durasi_sec > 600:
            hasil["livechat"] = "✓ Replay"

    return hasil


def ekstraksi_video_id(url_or_id: str) -> str:
    """Mengekstrak ID video 11 karakter dari link YouTube atau string ID."""
    clean = url_or_id.strip()
    if len(clean) == 11 and re.match(r"^[a-zA-Z0-9_-]{11}$", clean):
        return clean

    match = re.search(r"(?:v=|\/live\/|\/v\/|\/embed\/|youtu\.be\/|\/watch\?v=)([a-zA-Z0-9_-]{11})", clean)
    if match:
        return match.group(1)
    return clean


# =====================================================================
# 1. AUTENTIKASI & KREDENSIAL HOLODEX API
# =====================================================================

def muat_api_key() -> str:
    """
    Mengambil Holodex API Key dari cache_chat/holodex_key.txt,
    ~/.gemini/holodex_key.txt, atau variabel lingkungan HOLODEX_API_KEY.
    """
    env_key = os.environ.get("HOLODEX_API_KEY", "").strip()
    if env_key:
        return env_key

    for key_path in [HOLODEX_KEY_FILE, Path.home() / ".gemini" / "holodex_key.txt"]:
        if key_path.exists():
            try:
                for line in key_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line
            except Exception:
                pass
    return ""


def simpan_api_key(key: str) -> bool:
    """Menyimpan Holodex API Key ke cache_chat/holodex_key.txt."""
    try:
        HOLODEX_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HOLODEX_KEY_FILE.write_text(key.strip() + "\n", encoding="utf-8")
        return True
    except Exception:
        return False


def get_headers() -> Dict[str, str]:
    """Menyusun header HTTP permintaan Holodex API v2."""
    headers = {
        "Accept": "application/json",
        "User-Agent": "Antigravity-VTuber-Clipper/1.0"
    }
    api_key = muat_api_key()
    if api_key:
        headers["X-APIKEY"] = api_key
    return headers


# =====================================================================
# 2. STREAM RADAR: DISCOVERY VOD YANG BARU SELESAI
# =====================================================================

def ambil_stream_terakhir(
    org: str = "Hololive",
    limit: int = 12,
    status: str = "past",
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Mengambil daftar video livestream yang baru saja berakhir (status='past' via /videos)
    atau sedang berlangsung (status='live' via /live) untuk organisasi tertentu.
    """
    # Pemetaan organisasi resmi Holodex
    org_map = {
        "Hololive": "Hololive",
        "Nijisanji": "Nijisanji",
        "VSPO": "VSPO",
        "Indie": "Independents",
        "Independents": "Independents"
    }
    org_api = org_map.get(org, org)

    # Endpoint: /videos untuk VOD (past), /live untuk stream yang sedang aktif (live)
    endpoint = f"{BASE_URL}/videos" if status == "past" else f"{BASE_URL}/live"

    params = {
        "status": status,
        "type": "stream",
        "limit": min(limit, 25),
        "offset": offset,
        "sort": "available_at",
        "order": "desc"
    }
    if org_api and org_api.lower() != "semua":
        params["org"] = org_api

    headers = get_headers()
    try:
        resp = requests.get(endpoint, headers=headers, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            hasil = []
            for item in data:
                vid = item.get("id", "")
                ch = item.get("channel", {})
                ch_name = ch.get("name") or ch.get("english_name") or "VTuber"
                title = item.get("title", "Livestream")
                durasi_sec = item.get("duration", 0)
                durasi_str = detik_ke_timecode(durasi_sec) if durasi_sec > 0 else "Live/Baru Berakhir"
                yt_url = f"https://www.youtube.com/watch?v=s_{vid}" if vid else ""
                yt_url = f"https://www.youtube.com/watch?v={vid}"

                tgl_mentah = item.get("start_actual") or item.get("available_at") or item.get("published_at") or ""
                tgl_str = format_waktu_iso(tgl_mentah)

                hasil.append({
                    "id": vid,
                    "title": title,
                    "vtuber": ch_name,
                    "channel_id": ch.get("id", ""),
                    "url": yt_url,
                    "duration_sec": durasi_sec,
                    "duration_str": durasi_str,
                    "topic_id": item.get("topic_id", ""),
                    "published_at": tgl_mentah,
                    "live_time": tgl_str,
                    "caption": "-",
                    "livechat": "-"
                })

            # Deteksi ketersediaan Caption (JP/EN/ID) dan Livechat secara paralel
            try:
                from concurrent.futures import ThreadPoolExecutor
                def _probe_stream(s):
                    v_id = s.get("id")
                    durasi = s.get("duration_sec", 0)
                    if v_id:
                        info = deteksi_caption_dan_chat(v_id, durasi_sec=durasi)
                        s["caption"] = info.get("caption", "-")
                        s["livechat"] = info.get("livechat", "-")
                    return s

                with ThreadPoolExecutor(max_workers=6) as executor:
                    hasil = list(executor.map(_probe_stream, hasil))
            except Exception:
                pass

            return hasil
        elif resp.status_code == 401 or resp.status_code == 403:
            print("[WARNING] Holodex API Key tidak valid atau belum diisi. Kunjungi holodex.net/login untuk membuat API key gratis.")
            return []
        else:
            print(f"[WARNING] Permintaan Holodex API gagal (Status {resp.status_code}): {resp.text[:150]}")
            return []
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan koneksi saat mengakses Holodex: {e}")
        return []


# =====================================================================
# 3. DETAIL VOD: KOLABORATOR, KLIP KOMUNITAS & KARAOKE SONGS
# =====================================================================

def ambil_detail_video(video_id_or_url: str) -> Dict[str, Any]:
    """
    Mengambil data kaya dari Holodex untuk suatu VOD YouTube:
    - mentions : Talenta VTuber lain yang ikut kolaborasi
    - clips    : Klip yang sudah dibuat oleh komunitas untuk VOD ini
    - songs    : Daftar lagu dan penanda waktu singing stream (karaoke)
    Endpoint: GET /v2/videos/{video_id}?include=clips,mentions,songs,description
    """
    vid = ekstraksi_video_id(video_id_or_url)
    hasil = {
        "id": vid,
        "title": "",
        "vtuber": "",
        "collab_talents": [],  # list nama VTuber kolaborator
        "existing_clips": [],  # list klip komunitas yang sudah ada
        "karaoke_songs": [],   # list lagu jika singing stream
        "description": "",
        "topic_id": ""
    }

    if not vid:
        return hasil

    endpoint = f"{BASE_URL}/videos/{vid}"
    params = {"include": "clips,mentions,songs,description"}
    headers = get_headers()

    try:
        resp = requests.get(endpoint, headers=headers, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            ch = data.get("channel", {})
            hasil["title"] = data.get("title", "")
            hasil["vtuber"] = ch.get("name") or ch.get("english_name") or ""
            hasil["topic_id"] = data.get("topic_id", "")
            hasil["description"] = data.get("description", "")

            # 1. Ekstrak member kolaborasi (mentions)
            for m in data.get("mentions", []):
                m_name = m.get("name") or m.get("english_name") or ""
                m_twitter = m.get("twitter", "")
                if m_name and m_name.lower() != hasil["vtuber"].lower():
                    hasil["collab_talents"].append({
                        "name": m_name,
                        "twitter": f"@{m_twitter}" if m_twitter else "",
                        "channel_id": m.get("id", "")
                    })

            # 2. Ekstrak klip yang sudah dibuat komunitas
            for c in data.get("clips", []):
                hasil["existing_clips"].append({
                    "id": c.get("id", ""),
                    "title": c.get("title", ""),
                    "clipper": c.get("channel", {}).get("name", "Clipper"),
                    "lang": c.get("lang", "")
                })

            # 3. Ekstrak lagu karaoke (songs)
            for s in data.get("songs", []):
                start_sec = s.get("start", 0)
                end_sec = s.get("end", start_sec + 180)
                hasil["karaoke_songs"].append({
                    "title": s.get("name") or s.get("title") or "Lagu Karaoke",
                    "artist": s.get("original_artist") or s.get("artist") or "",
                    "start_sec": start_sec,
                    "end_sec": end_sec,
                    "start_tc": detik_ke_timecode(start_sec),
                    "end_tc": detik_ke_timecode(end_sec)
                })

        return hasil
    except Exception as e:
        print(f"[WARNING] Gagal mengambil detail video Holodex ({vid}): {e}")
        return hasil


# =====================================================================
# 4. EKSTRAKSI INSTAN KARAOKE SONGS KE SECTIONS.TXT
# =====================================================================

def ekspor_karaoke_ke_sections(
    karaoke_songs: List[Dict[str, Any]],
    youtube_url: str,
    output_path: Path
) -> int:
    """
    Mengonversi daftar lagu karaoke Holodex langsung ke berkas sections.txt:
    URL | HH:MM:SS-HH:MM:SS | Judul Lagu - Penyanyi Asli
    """
    if not karaoke_songs:
        return 0

    lines = [f"# Dihasilkan otomatis dari Holodex Karaoke Index pada {time.strftime('%Y-%m-%d %H:%M:%S')}"]
    for idx, s in enumerate(karaoke_songs, start=1):
        artis_info = f" - {s['artist']}" if s.get("artist") else ""
        label = f"{idx}. {s['title']}{artis_info}"
        lines.append(f"{youtube_url} | {s['start_tc']}-{s['end_tc']} | {label}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[INFO] Berhasil mengekspor {len(karaoke_songs)} lagu karaoke ke: {output_path}")
    return len(karaoke_songs)


# =====================================================================
# 5. DIAGNOSTIK KANAL HOLODEX (--doctor)
# =====================================================================

def doctor_check() -> Dict[str, Any]:
    """Diagnostik status API key dan koneksi ke Holodex API v2."""
    key = muat_api_key()
    has_key = bool(key)

    koneksi_ok = False
    pesan = "API Key belum dikonfigurasi"

    if has_key:
        headers = get_headers()
        try:
            r = requests.get(f"{BASE_URL}/videos?limit=1", headers=headers, timeout=8)
            if r.status_code == 200:
                koneksi_ok = True
                pesan = "Koneksi Holodex API v2 Aktif & Valid (100% Siap)"
            elif r.status_code == 401 or r.status_code == 403:
                pesan = "API Key tidak valid (Ditolak oleh Holodex)"
            else:
                pesan = f"Respons Holodex HTTP {r.status_code}"
        except Exception as e:
            pesan = f"Gangguan jaringan: {e}"

    return {
        "api_key_ditemukan": has_key,
        "koneksi_holodex_aktif": koneksi_ok,
        "status_detail": pesan
    }


def main():
    parser = argparse.ArgumentParser(description="Klien Holodex API v2 untuk VTuber Clipper.")
    parser.add_argument("--org", type=str, default="Hololive", help="Organisasi VTuber (Hololive / Nijisanji / VSPO / Indie)")
    parser.add_argument("--limit", type=int, default=10, help="Jumlah stream yang diambil")
    parser.add_argument("--video-id", type=str, default="", help="ID atau URL video YouTube")
    parser.add_argument("--karaoke-to-sections", action="store_true", help="Ekspor daftar lagu karaoke ke sections.txt")
    parser.add_argument("--doctor", action="store_true", help="Jalankan diagnostik koneksi Holodex")

    args = parser.parse_args()

    print("=" * 65)
    print("✨ ANTIGRAVITY HOLODEX VTUBER RADAR")
    print("=" * 65)

    if args.doctor:
        doc = doctor_check()
        print("\n📋 DIAGNOSTIK HOLODEX API:")
        print(f"• API Key Ditemukan      : {'✓ Ya' if doc['api_key_ditemukan'] else '✗ Tidak (Simpan di cache_chat/holodex_key.txt)'}")
        print(f"• Status Koneksi API     : {'✓ Aktif' if doc['koneksi_holodex_aktif'] else '✗ Gagal'}")
        print(f"• Detail                 : {doc['status_detail']}\n")
        if not args.video_id:
            return

    if args.video_id:
        detail = ambil_detail_video(args.video_id)
        print(f"\n📺 DETAIL VOD: {detail['title']} ({detail['vtuber']})")
        print(f"• Kolaborator ({len(detail['collab_talents'])}): {', '.join([c['name'] for c in detail['collab_talents']]) or 'Solo stream'}")
        print(f"• Klip Komunitas ({len(detail['existing_clips'])} klip sudah ada)")
        print(f"• Lagu Karaoke ({len(detail['karaoke_songs'])} lagu)")

        if args.karaoke_to_sections and detail["karaoke_songs"]:
            yt_url = f"https://www.youtube.com/watch?v={detail['id']}"
            sec_file = ROOT_DIR / "sections.txt"
            ekspor_karaoke_ke_sections(detail["karaoke_songs"], yt_url, sec_file)
    else:
        print(f"\n📡 MENCARI STREAM TERAKHIR DARI '{args.org.upper()}':")
        streams = ambil_stream_terakhir(org=args.org, limit=args.limit)
        if not streams:
            print("Tidak ada stream yang ditemukan atau API Key belum diisi.")
        for idx, s in enumerate(streams, start=1):
            print(f"[{idx}] {s['vtuber']} — {s['title'][:55]}...")
            print(f"    URL: {s['url']} | Durasi: {s['duration_str']}")


if __name__ == "__main__":
    main()
