"""
Modul: auto_highlighter_argon.py
Deskripsi: Otomasi ekstraksi highlight VTuber menggunakan model penalaran Google Gemini (Gemini 4 Argon / Gemini 3.8 Flash).
           Menganalisis lonjakan CPM livechat & transkrip secara lokal (Headless),
           menghasilkan rangkuman highlight tanpa peramban (browser),
           serta menyimpan output langsung ke sections.txt dan marker DaVinci Resolve.
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import requests

# Konfigurasi encoding UTF-8 untuk terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Impor pengekspor marker DaVinci Resolve jika tersedia
sys.path.append(str(Path(__file__).resolve().parent.parent / "cache_chat" / "davinci_core"))
try:
    # pyrefly: ignore[missing-import]
    from marker_exporter import ekspor_ke_csv, ekspor_ke_edl, injeksi_marker_ke_resolve
except ImportError:
    ekspor_ke_csv = None
    ekspor_ke_edl = None
    injeksi_marker_ke_resolve = None

# Pastikan direktori root project terdaftar di sys.path untuk impor core
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.chat_peak_detector import (
    timecode_ke_detik,
    detik_ke_timecode,
    analisis_lonjakan_cpm
)

# Deteksi SDK Google Antigravity resmi
try:
    import asyncio
    import google.antigravity as ag
    ANTIGRAVITY_SDK_TERSEDIA = True
except ImportError:
    ANTIGRAVITY_SDK_TERSEDIA = False

# Daftar kata kunci pemicu reaksi chat sesuai standar prompt_rangkum.txt
KATA_KUNCI_REAKSI = [
    "haha", "wkwk", "wk", "lol", "kekw", "kusa", "草", "laughing", "joy",
    ":v", "hah", "lah", "huh", "nani", "apa", "what", "scam", "gws", "gsh",
    "imut", "lucu", "kawai", "tskr", "bless", "wholesome", "bengecc", "face-red",
    "cry", "silly", "わらう", "イヒヒ", "かわい", "membership", "superchat"
]


def muat_livechat(chat_path: str) -> List[Dict[str, Any]]:
    """
    Membaca berkas livechat (CSV atau JSON) dan mengembalikan daftar pesan chat.
    Format pesan: {'waktu_detik': float, 'waktu_str': str, 'pengirim': str, 'pesan': str, 'skor_reaksi': int}
    """
    hasil = []
    p = Path(chat_path)
    if not p.exists():
        print(f"[WARNING] Berkas livechat tidak ditemukan: {chat_path}")
        return hasil

    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [x.strip() for x in line.split("|", 2)]
            if len(parts) >= 2:
                tc_str = parts[0]
                sec = timecode_ke_detik(tc_str)
                isi = parts[1] if len(parts) == 2 else parts[2]
                pengirim = parts[1] if len(parts) >= 3 else ""

                # Hitung kemunculan kata kunci reaksi
                pesan_lower = isi.lower()
                skor = sum(1 for kw in KATA_KUNCI_REAKSI if kw in pesan_lower)
                # Tambahan skor jika diakhiri huruf 'w' bergaya Jepang (misal: "yabaiw", "kawaiiw")
                if re.search(r"[a-z]w+$", pesan_lower):
                    skor += 1

                hasil.append({
                    "waktu_detik": sec,
                    "waktu_str": tc_str,
                    "pengirim": pengirim,
                    "pesan": isi,
                    "skor_reaksi": skor
                })

    return hasil


def muat_transkrip(transkrip_path: str) -> List[Dict[str, Any]]:
    """
    Membaca berkas transkrip teks dan mengembalikan daftar tuturan.
    Format: {'waktu_detik': float, 'waktu_str': str, 'teks': str}
    """
    hasil = []
    p = Path(transkrip_path)
    if not p.exists():
        return hasil

    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [x.strip() for x in line.split("|", 1)]
            if len(parts) >= 2:
                tc_str = parts[0]
                sec = timecode_ke_detik(tc_str)
                teks = parts[1]
                hasil.append({
                    "waktu_detik": sec,
                    "waktu_str": tc_str,
                    "teks": teks
                })

    return hasil


def panggil_gemini_api(
    prompt_teks: str,
    model_name: str = "gemini-4-argon",
    thinking_level: str = "HIGH"
) -> str:
    """
    Memanggil Google Gemini API secara langsung menggunakan API key dari gemini_key.txt
    dengan konfigurasi thinkingConfig (HIGH).
    """
    key_path = Path("C:/Users/mobog/.gemini/gemini_key.txt")
    if not key_path.exists():
        raise FileNotFoundError(f"Berkas kunci API Gemini tidak ditemukan: {key_path}")

    api_key = key_path.read_text(encoding="utf-8").strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_teks}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8192,
            "thinkingConfig": {
                "thinkingLevel": thinking_level.upper()
            }
        }
    }

    print(f"[INFO] Memanggil REST API model '{model_name}' (Thinking Level: {thinking_level.upper()})...")
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        print(f"[WARNING] Model '{model_name}' mengembalikan status {resp.status_code}.")
        # Coba fallback ke model flash lainnya
        fallback_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3.8-flash", "gemini-3.5-flash"]
        for fb in fallback_models:
            if fb == model_name:
                continue
            print(f"[INFO] Mencoba fallback ke model '{fb}' (Thinking Level: {thinking_level.upper()})...")
            url_fb = f"https://generativelanguage.googleapis.com/v1beta/models/{fb}:generateContent?key={api_key}"
            resp_fb = requests.post(url_fb, headers=headers, json=payload, timeout=120)
            if resp_fb.status_code != 200:
                payload_basic = {
                    "contents": payload["contents"],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192}
                }
                resp_fb = requests.post(url_fb, headers=headers, json=payload_basic, timeout=120)
            if resp_fb.status_code == 200:
                data = resp_fb.json()
                teks_hasil = data["candidates"][0]["content"]["parts"][0]["text"]
                return f"# Dihasilkan oleh: {fb} (Fallback dari {model_name})\n\n" + teks_hasil

        if resp.status_code == 429:
            pesan_429 = (
                "\n" + "=" * 60 + "\n"
                "❌ KUOTA REST API GEMINI HABIS (HTTP 429 / RESOURCE_EXHAUSTED)\n"
                "Batas kuota harian/menit API Key Google AI Studio telah tercapai.\n\n"
                "👉 SOLUSI TERBAIK (GRATIS & TANPA BATAS KUOTA):\n"
                "Gunakan tombol 'Ekstrak Otomatis via Chromium (Mode B)' di tab Ringkasan Chat!\n"
                "Mode B berjalan otomatis via peramban Chromium tanpa memerlukan kuota API Key.\n"
                + "=" * 60
            )
            print(pesan_429)
            raise RuntimeError(pesan_429)

        raise RuntimeError(f"Gagal memanggil API Gemini (Status {resp.status_code}): {resp.text}")

    data = resp.json()
    teks_hasil = data["candidates"][0]["content"]["parts"][0]["text"]
    return f"# Dihasilkan oleh: {model_name} ({thinking_level.upper()})\n\n" + teks_hasil


async def jalankan_subagent_antigravity(
    prompt_teks: str,
    model_name: str = "gemini-4-argon",
    thinking_level: str = "high"
) -> str:
    """
    Menjalankan penalaran menggunakan official Google Antigravity Agentic Subagent.
    Mengonfigurasi ModelTarget secara eksplisit ke gemini-4-argon dengan ThinkingLevel.HIGH.
    """
    key_path = Path("C:/Users/mobog/.gemini/gemini_key.txt")
    api_key = key_path.read_text(encoding="utf-8").strip() if key_path.exists() else None

    # Pemetaan eksplisit ke ModelTarget dan ThinkingLevel.HIGH di SDK Antigravity
    level_enum = ag.models.ThinkingLevel(thinking_level.lower())
    target_model = ag.models.ModelTarget(
        name=model_name,
        endpoint=ag.models.GeminiAPIEndpoint(
            api_key=api_key,
            options=ag.models.GeminiModelOptions(thinking_level=level_enum),
        ),
    )

    config = ag.LocalAgentConfig(
        model=target_model,
        capabilities=ag.CapabilitiesConfig(),
    )

    async with ag.Agent(config) as agent:
        response = await agent.chat(prompt_teks)
        full_text = []
        async for token in response:
            full_text.append(token)
        hasil = "".join(full_text)
        if not hasil.strip():
            raise RuntimeError("Respons kosong dari Antigravity Subagent.")
        return f"# Dihasilkan oleh: {model_name} ({thinking_level.upper()}) — Antigravity SDK\n\n" + hasil


def panggil_ai_agentic(
    prompt_teks: str,
    model_name: str = "gemini-4-argon",
    thinking_level: str = "high"
) -> str:
    """
    Memanggil Antigravity Agentic Subagent (Gemini 4 Argon High), dengan fallback ke REST API Gemini.
    Juga menyimpan prompt klaster ke cache_chat/_klaster_prompt.txt untuk eksekusi langsung di Antigravity IDE.
    """
    try:
        base_dir = Path(__file__).resolve().parent.parent
        prompt_cache = base_dir / "cache_chat" / "_klaster_prompt.txt"
        prompt_cache.parent.mkdir(parents=True, exist_ok=True)
        prompt_cache.write_text(prompt_teks, encoding="utf-8")
    except Exception:
        pass

    if ANTIGRAVITY_SDK_TERSEDIA:
        try:
            print(f"[INFO] Meluncurkan official Google Antigravity Subagent ({model_name} — {thinking_level.upper()})...")
            return asyncio.run(
                jalankan_subagent_antigravity(
                    prompt_teks,
                    model_name=model_name,
                    thinking_level=thinking_level
                )
            )
        except Exception as e:
            print(f"[INFO] Antigravity Subagent beralih ke REST engine: {e}")

    # Fallback ke engine REST API
    return panggil_gemini_api(prompt_teks, model_name=model_name, thinking_level=thinking_level.upper())


def buat_prompt_analisis(
    klaster_segmen: List[Dict[str, Any]],
    vtuber_name: str = "VTuber",
    vod_title: str = "VTuber Livestream Highlight"
) -> str:
    """
    Menyusun prompt reasoning terstruktur dan ringkas sesuai pedoman anti-halusinasi.
    """
    baris_data = []
    for k in klaster_segmen:
        cuplikan = " ".join(k["cuplikan_chat"][:3])
        dialog = k["dialog_transkrip"]
        if len(dialog) > 120:
            dialog = dialog[:117] + "..."
        baris_data.append(
            f"[#{k['nomor']}] {k['mulai_tc']}-{k['selesai_tc']} | Chat:{k['total_chat']} | "
            f"Reaksi:{k['jumlah_reaksi']} | Chat:\"{cuplikan}\" | Tuturan:\"{dialog}\""
        )

    data_terstruktur = "\n".join(baris_data)

    prompt = f"""Tolong buatkan rangkuman highlight dan daftar timestamp YouTube untuk livestream VTuber berikut:
• Talent: {vtuber_name}
• Judul VOD: {vod_title}

Berikut adalah data klaster momen potensial (hasil deteksi lonjakan reaksi penonton CPM dan dialog transkrip):

{data_terstruktur}

Tugas:
1. Susun minimal 10 segmen kronologis dengan format timecode HH:MM:SS (Waktu Mulai) dan waktu selesai di dalam tanda kurung.
2. Tentukan Top 5 kandidat klip terbaik untuk video highlight / shorts.
3. Berikan 3-5 kutipan ikonik dan rekomendasi hashtag (tanpa simbol '#').

Aturan:
- Gunakan Bahasa Indonesia yang menarik dan natural bagi penonton VTuber.
- Klaim WAJIB berbasis data di atas (jangan mengarang dialog). Jika tuturan transkrip kosong, sebutkan momen bertumpu pada reaksi chat atau visual game.
- Langsung berikan hasil dalam format Markdown persis seperti struktur berikut (tanpa intro/outro basa-basi):

# STRUKTUR LAPORAN (WAJIB PERSIS FORMAT DI BAWAH)
## 1. Timeline Kronologis (Minimal 10 Segmen)
- **HH:MM:SS | [Judul Momen] (Berakhir di HH:MM:SS)**
  - **Aktivitas:** (Deskripsi tuturan/kejadian dari transkrip)
  - **Reaksi Chat:** (Pola pesan dominan)
  - **Jumlah Chat:** (Total pesan unik di jendela waktu)
  - **Konteks:** (Pemicu lonjakan reaksi penonton)

## 2. Kandidat Klip Terbaik
- **Top 5 Kandidat Klip (Prioritas Tinggi):**
  - **Klip #N — HH:MM:SS | [Judul Catchy] (Berakhir di HH:MM:SS)**
  - **Alasan:** (Potensi viralitas & daya tarik)
  - **Statistik Intensitas:** (Burst CPM, sentimen penonton)
  - **Saran Edit:** (Zoom, SFX, subtitle)

## 3. Insight & Kutipan
- **Insight Superchat:** (Jika ada)
- **3-5 Kutipan Ikonik:** HH:MM:SS | "[Nama]: Kutipan dari transkrip"
- **Hashtag:** (Daftar hashtag tanpa simbol '#')
"""
    return prompt


def ekstrak_segmen_dari_markdown(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Mengekstrak timestamp dan judul segmen dari teks laporan Markdown hasil model AI.
    Mendukung bullet '-' maupun '*' serta tanda kurung di dalam judul momen.
    Pola: - **HH:MM:SS | [Judul Momen] (Berakhir di HH:MM:SS)**
    """
    segmen_list = []
    pola = re.compile(
        r"[-*]\s+\*\*(\d{1,2}:\d{2}:\d{2})\s*\|\s*\[?(.+?)\]?\s*\(Berakhir\s+di\s+(\d{1,2}:\d{2}:\d{2})\)\*\*",
        re.IGNORECASE
    )

    for match in pola.finditer(markdown_text):
        mulai_tc = match.group(1)
        judul = match.group(2).strip()
        selesai_tc = match.group(3)
        mulai_sec = timecode_ke_detik(mulai_tc)
        selesai_sec = timecode_ke_detik(selesai_tc)

        # Tentukan warna marker berdasarkan kata kunci judul
        judul_lower = judul.lower()
        warna = "Cyan"
        if any(w in judul_lower for w in ["scream", "teriak", "kaget", "panik", "mati"]):
            warna = "Red"
        elif any(w in judul_lower for w in ["superchat", "donasi", "uang", "gift"]):
            warna = "Fuchsia"
        elif any(w in judul_lower for w in ["imut", "kawaii", "cute", "wholesome", "peluk"]):
            warna = "Pink"
        elif any(w in judul_lower for w in ["lucu", "wkwk", "lol", "ngakak", "lawak"]):
            warna = "Cyan"

        segmen_list.append({
            "title": judul,
            "start_tc": mulai_tc,
            "end_tc": selesai_tc,
            "start_sec": mulai_sec,
            "end_sec": selesai_sec,
            "color": warna,
            "notes": f"Highlight: {judul}"
        })

    return segmen_list


def simpan_ke_sections_txt(
    segmen_list: List[Dict[str, Any]],
    output_path: str = "sections.txt",
    youtube_url: str = "https://www.youtube.com/watch?v=highlight"
) -> int:
    """
    Menyimpan daftar segmen ke format berkas sections.txt:
    URL | HH:MM:SS-HH:MM:SS | Label
    """
    lines = [f"# Dihasilkan otomatis oleh Antigravity Argon AI pada {time.strftime('%Y-%m-%d %H:%M:%S')}"]
    for idx, s in enumerate(segmen_list, start=1):
        # Bersihkan karakter ilegal Windows (< > : " / \ | ? *) agar aman saat diunduh dan dipotong
        clean_title = re.sub(r'[<>:"/\\|?*]', ' ', s['title'])
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        baris = f"{youtube_url} | {s['start_tc']}-{s['end_tc']} | {idx}. {clean_title}"
        lines.append(baris)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return len(segmen_list)


def temukan_folder_channel(
    url: str = "",
    base_dir: Optional[Path] = None
) -> Tuple[Optional[Path], str, str]:
    """
    Menemukan folder channel VTuber aktif (@Channel), nama talent, dan judul VOD secara dinamis.
    Prioritas:
    1. Info aktif dari cache_chat/active_stream_info.json jika tersedia
    2. Folder @* yang berisi livechat.csv terbaru (berdasarkan mtime)
    3. Parsing folder name menjadi nama talent (misal @VestiaZeta -> Vestia Zeta)
    4. Ekstraksi judul VOD dari berkas FULL_*.json atau FULL_*.srt di dalam folder
    """
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent

    active_json = base_dir / "cache_chat" / "active_stream_info.json"
    if active_json.exists():
        try:
            data = json.loads(active_json.read_text(encoding="utf-8", errors="ignore"))
            folder_name = data.get("folder", "")
            if folder_name and (base_dir / folder_name).is_dir():
                target_folder = base_dir / folder_name
                vtuber = data.get("vtuber") or re.sub(r'([a-z])([A-Z])', r'\1 \2', target_folder.name.lstrip('@'))
                vod = data.get("title") or "VTuber Livestream Highlight"
                return target_folder, vtuber, vod
        except Exception:
            pass

    # Cari semua folder @* di direktori kerja yang memiliki livechat.csv
    kandidat = []
    for p in base_dir.glob("@*"):
        if p.is_dir():
            chat_csv = p / "livechat.csv"
            if chat_csv.exists():
                kandidat.append((chat_csv.stat().st_mtime, p))

    if not kandidat:
        if (base_dir / "cache_chat" / "livechat.csv").exists():
            return base_dir / "cache_chat", "VTuber", "VTuber Livestream Highlight"
        return None, "VTuber", "VTuber Livestream Highlight"

    # Urutkan berdasarkan waktu modifikasi terbaru
    kandidat.sort(key=lambda x: x[0], reverse=True)
    folder_terpilih = kandidat[0][1]

    raw_name = folder_terpilih.name.lstrip("@")
    vtuber_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', raw_name)

    vod_title = "VTuber Livestream Highlight"
    for f in folder_terpilih.glob("FULL_*"):
        stem = f.stem.replace("FULL_", "").strip()
        if stem and "transkrip" not in stem.lower():
            vod_title = stem
            break

    return folder_terpilih, vtuber_name, vod_title


def main():
    parser = argparse.ArgumentParser(
        description="Otomasi Ekstraksi Highlight VTuber via Antigravity Gemini/Argon AI (Headless)."
    )
    parser.add_argument("--chat", type=str, default="", help="Path ke berkas livechat.csv")
    parser.add_argument("--transcript", type=str, default="", help="Path ke berkas transkrip.csv")
    parser.add_argument("--url", type=str, default="", help="URL video YouTube sumber")
    parser.add_argument("--vtuber", type=str, default="VTuber", help="Nama VTuber")
    parser.add_argument("--vod", type=str, default="VTuber Highlight", help="Judul VOD")
    parser.add_argument("--model", type=str, default="gemini-4-argon", help="Model AI (gemini-4-argon / gemini-3.8-flash)")
    parser.add_argument("--output-sections", type=str, default="sections.txt", help="Path keluaran sections.txt")
    parser.add_argument("--auto-marker", action="store_true", default=True, help="Otomatis injeksikan marker ke DaVinci Resolve jika aktif")
    parser.add_argument("--jarak-min", type=int, default=45, help="Jarak minimum antar puncak highlight (detik, default: 45)")
    parser.add_argument("--buffer-awal", type=float, default=15.0, help="Buffer pre-roll mundur sebelum highlight (detik, default: 15.0)")
    parser.add_argument("--buffer-akhir", type=float, default=10.0, help="Buffer post-roll maju setelah highlight (detik, default: 10.0)")

    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    chat_file = args.chat
    transkrip_file = args.transcript
    url = args.url
    vtuber = args.vtuber
    vod = args.vod

    if not url:
        sec_file = base_dir / "sections.txt"
        if sec_file.exists():
            for line in sec_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    url = line.split("|")[0].strip()
                    break
        if not url:
            url = "https://www.youtube.com/watch?v=source_video"

    # Resolusi otomatis folder channel, talent, dan judul VOD
    auto_folder, auto_vtuber, auto_vod = temukan_folder_channel(url, base_dir)

    if chat_file and Path(chat_file).exists():
        auto_folder = Path(chat_file).parent
    elif not chat_file and auto_folder:
        calon_chat = auto_folder / "livechat.csv"
        if calon_chat.exists():
            chat_file = str(calon_chat)

    if not transkrip_file and auto_folder:
        calon_transkrip = auto_folder / "transkrip.csv"
        if calon_transkrip.exists():
            transkrip_file = str(calon_transkrip)

    if vtuber == "VTuber" and auto_vtuber != "VTuber":
        vtuber = auto_vtuber

    if vod in ("VTuber Highlight", "VTuber Livestream Highlight") and auto_vod != "VTuber Livestream Highlight":
        vod = auto_vod

    print("=" * 60)
    print("🚀 ANTIGRAVITY AGENTIC HIGHLIGHT EXTRACTOR")
    print(f"• Model AI       : {args.model}")
    print(f"• Talent         : {vtuber}")
    print(f"• Judul VOD      : {vod}")
    print(f"• Berkas Chat    : {chat_file}")
    print(f"• Transkrip      : {transkrip_file}")
    print(f"• URL Sumber     : {url}")
    print(f"• Mode Marker    : Hybrid (EDL + CSV + DaVinci Live)")
    print("=" * 60)

    # 1. Muat data
    print("\n[1/5] Membaca data chat & transkrip lokal...")
    chats = muat_livechat(chat_file)
    transkrips = muat_transkrip(transkrip_file)
    print(f"      Ditemukan {len(chats)} baris pesan chat dan {len(transkrips)} baris transkrip.")

    # 2. Analisis lonjakan CPM
    print("\n[2/5] Menghitung baseline CPM & mendeteksi lonjakan reaksi (Sliding Window & Peak Finding)...")
    klaster = analisis_lonjakan_cpm(
        chats,
        transkrips,
        jendela_detik=20,
        pengali_cpm=2.0,
        jarak_min_detik=args.jarak_min,
        buffer_awal_detik=args.buffer_awal,
        buffer_akhir_detik=args.buffer_akhir
    )
    print(f"      Teridentifikasi {len(klaster)} klaster momen potensial.")

    if not klaster:
        print("[ERROR] Tidak ada klaster lonjakan yang terdeteksi.")
        return

    # 3. Panggil Reasoning Model
    print(f"\n[3/5] Mengirim data teragregasi ke Model {args.model} via Antigravity Agent...")
    prompt = buat_prompt_analisis(klaster, vtuber_name=vtuber, vod_title=vod)
    
    t0 = time.time()
    laporan_md = panggil_ai_agentic(prompt, model_name=args.model)
    durasi = time.time() - t0
    print(f"      Model selesai bernalar dalam {durasi:.2f} detik.")

    # Simpan laporan markdown lengkap
    laporan_path = base_dir / "cache_chat" / "hasil_rangkuman.md"
    laporan_path.parent.mkdir(parents=True, exist_ok=True)
    laporan_path.write_text(laporan_md, encoding="utf-8")
    print(f"      Laporan lengkap disimpan ke: {laporan_path}")

    # Otomatis simpan salinan ke folder channel VTuber aktif
    if auto_folder and auto_folder.exists():
        safe_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in vod).strip()
        (auto_folder / f"FULL_{safe_title}_hasil_rangkuman.md").write_text(laporan_md, encoding="utf-8")
        (auto_folder / "hasil_rangkuman.md").write_text(laporan_md, encoding="utf-8")
        print(f"      • Rangkuman terarsip di channel: {auto_folder.name}")

    # 4. Ekstraksi Timestamp & Simpan ke sections.txt
    print("\n[4/5] Mengonversi hasil rangkuman ke format antrean sections.txt...")
    segmen = ekstrak_segmen_dari_markdown(laporan_md)
    if segmen:
        target_sections = str(base_dir / args.output_sections)
        jumlah = simpan_ke_sections_txt(segmen, target_sections, youtube_url=url)
        print(f"      Berhasil menulis {jumlah} segmen ke: {target_sections}")
    else:
        print("      [WARNING] Pola timestamp tidak terdeteksi otomatis dari teks Markdown.")

    # 5. Ekspor Marker DaVinci Resolve
    print("\n[5/5] Mengekspor marker DaVinci Resolve...")
    edl_out = str(base_dir / "cache_chat" / "davinci_markers.edl")
    csv_out = str(base_dir / "cache_chat" / "davinci_markers.csv")

    if ekspor_ke_edl and segmen:
        ekspor_ke_edl(segmen, edl_out, fps=30.0, title="VTuber_Highlights")
        ekspor_ke_csv(segmen, csv_out, fps=30.0)
        print(f"      • File EDL : {edl_out}")
        print(f"      • File CSV : {csv_out}")

        if auto_folder and auto_folder.exists():
            safe_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in vod).strip()
            shutil.copy2(edl_out, auto_folder / f"FULL_{safe_title}_davinci_markers.edl")
            shutil.copy2(edl_out, auto_folder / "davinci_markers.edl")
            shutil.copy2(csv_out, auto_folder / f"FULL_{safe_title}_davinci_markers.csv")
            shutil.copy2(csv_out, auto_folder / "davinci_markers.csv")
            print(f"      • Marker terarsip di channel: {auto_folder.name}")

        if args.auto_marker and injeksi_marker_ke_resolve:
            sukses, pesan = injeksi_marker_ke_resolve(segmen)
            print(f"      • Injeksi Langsung DaVinci: {pesan}")

    # 6. Pembuatan Paket SEO YouTube Video & Chapters Kumulatif (X/Twitter Radar)
    print("\n[6/6] Menghasilkan Paket SEO YouTube Video (16:9) & Chapters...")
    try:
        from twitter_vtuber_radar import (
            ekstrak_metadata_vod,
            ambil_buzz_twitter,
            muat_segmen_sections_txt,
            buat_paket_seo_youtube_video
        )
        vod_meta = ekstrak_metadata_vod(url)
        buzz = ambil_buzz_twitter(vod_meta["hashtags"], vtuber_name=vod_meta["uploader"])
        sections_p = base_dir / args.output_sections
        segmen_terformat = muat_segmen_sections_txt(sections_p)
        out_seo = base_dir / "cache_chat" / "youtube_video_seo.md"
        buat_paket_seo_youtube_video(segmen_terformat, vod_meta, buzz, out_seo)
        print(f"      • Paket SEO YouTube Video tersimpan di: {out_seo}")
    except Exception as e:
        print(f"      [INFO] Pembuatan paket SEO YouTube Video dilewati: {e}")

    print("\n✨ SELESAI! Seluruh proses ekstraksi highlight berjalan tanpa membuka browser.")
    print("=" * 60)


if __name__ == "__main__":
    main()
