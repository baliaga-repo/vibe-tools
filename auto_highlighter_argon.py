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


def timecode_ke_detik(tc_str: str) -> float:
    """
    Mengonversi string waktu (HH:MM:SS atau MM:SS atau detik) menjadi nilai float detik.
    """
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


def detik_ke_timecode(detik: float) -> str:
    """
    Mengonversi detik ke format timecode HH:MM:SS.
    """
    detik_int = int(round(max(0.0, detik)))
    jam = detik_int // 3600
    sisa = detik_int % 3600
    menit = sisa // 60
    det = sisa % 60
    return f"{jam:02d}:{menit:02d}:{det:02d}"


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


def analisis_lonjakan_cpm(
    chats: List[Dict[str, Any]],
    transkrips: List[Dict[str, Any]],
    jendela_detik: int = 20,
    pengali_cpm: float = 2.0,
    target_segmen_minimal: int = 10
) -> List[Dict[str, Any]]:
    """
    Melakukan pra-agregasi data lokal:
    1. Mengelompokkan pesan ke dalam bin jendela waktu (15-30 detik).
    2. Menghitung baseline CPM rata-rata.
    3. Mendeteksi lonjakan CPM & kata kunci reaksi (> pengali baseline).
    4. Menggabungkan klaster yang berdekatan (< 45 detik) dan menambahkan -10 detik buffer awal.
    5. Menautkan transkrip percakapan ke setiap klaster untuk mencegah halusinasi.
    """
    if not chats:
        return []

    maks_detik = max(c["waktu_detik"] for c in chats)
    jumlah_bin = int(maks_detik // jendela_detik) + 1
    bins = [[] for _ in range(jumlah_bin)]

    for c in chats:
        idx = int(c["waktu_detik"] // jendela_detik)
        if idx < len(bins):
            bins[idx].append(c)

    # Hitung CPM (Chat Per Minute) untuk setiap bin
    cpm_per_bin = [(len(b) * (60.0 / jendela_detik)) for b in bins]
    skor_reaksi_per_bin = [sum(c["skor_reaksi"] for c in b) for b in bins]

    # Baseline dihitung dari bin yang memiliki chat aktif (menghindari idle stream)
    bin_aktif = [cpm for cpm in cpm_per_bin if cpm > 0]
    baseline_cpm = (sum(bin_aktif) / len(bin_aktif)) if bin_aktif else 10.0

    # Penyesuaian otomatis ambang batas pengali jika segmen kurang dari target
    ambang_list = [pengali_cpm, 1.8, 1.5, 1.2]
    klaster_terpilih = []

    for ambang in ambang_list:
        ambang_cpm = baseline_cpm * ambang
        kandidat_bin = []

        for idx, (cpm, skor) in enumerate(zip(cpm_per_bin, skor_reaksi_per_bin)):
            # Lolos jika CPM melebihi ambang batas ATAU ada ledakan kata kunci reaksi tinggi
            if cpm >= ambang_cpm or (skor >= 5 and cpm >= baseline_cpm):
                kandidat_bin.append(idx)

        # Gabungkan bin berdekatan (gap < 45 detik -> gap <= 2 bin pada jendela 20s)
        klaster_mentah = []
        if kandidat_bin:
            awal_bin = kandidat_bin[0]
            akhir_bin = kandidat_bin[0]

            for b in kandidat_bin[1:]:
                if b - akhir_bin <= 2:
                    akhir_bin = b
                else:
                    klaster_mentah.append((awal_bin, akhir_bin))
                    awal_bin = b
                    akhir_bin = b
            klaster_mentah.append((awal_bin, akhir_bin))

        if len(klaster_mentah) >= target_segmen_minimal or ambang == ambang_list[-1]:
            klaster_terpilih = klaster_mentah
            break

    # Format hasil klaster dengan buffer -10 detik dan hubungkan ke transkrip
    segmen_hasil = []
    for idx_klaster, (b_awal, b_akhir) in enumerate(klaster_terpilih, start=1):
        mulai_sec = max(0.0, (b_awal * jendela_detik) - 10.0)
        selesai_sec = ((b_akhir + 1) * jendela_detik) + 5.0

        # Ambil sampel chat di jendela waktu ini
        chat_di_jendela = [
            c for c in chats
            if mulai_sec <= c["waktu_detik"] <= selesai_sec
        ]
        total_chat = len(chat_di_jendela)

        # Cari pola pesan reaksi dominan
        reaksi_list = [c["pesan"] for c in chat_di_jendela if c["skor_reaksi"] > 0]
        cuplikan_chat = [f"{c['waktu_str']} {c['pesan']}" for c in chat_di_jendela[:8]]

        # Ambil transkrip pada rentang waktu ini (anti-halusinasi)
        transkrip_di_jendela = [
            t["teks"] for t in transkrips
            if mulai_sec <= t["waktu_detik"] <= selesai_sec
        ]
        dialog_transkrip = " ".join(transkrip_di_jendela) if transkrip_di_jendela else "Data tuturan tidak tersedia"

        segmen_hasil.append({
            "nomor": idx_klaster,
            "mulai_detik": mulai_sec,
            "selesai_detik": selesai_sec,
            "mulai_tc": detik_ke_timecode(mulai_sec),
            "selesai_tc": detik_ke_timecode(selesai_sec),
            "total_chat": total_chat,
            "dialog_transkrip": dialog_transkrip,
            "cuplikan_chat": cuplikan_chat,
            "jumlah_reaksi": len(reaksi_list)
        })

    return segmen_hasil


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
        # Coba fallback ke model flash dengan tetap mempertahankan thinkingLevel HIGH jika didukung
        fallback_models = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash"]
        for fb in fallback_models:
            if fb == model_name:
                continue
            print(f"[INFO] Mencoba fallback ke model '{fb}' (Thinking Level: {thinking_level.upper()})...")
            url_fb = f"https://generativelanguage.googleapis.com/v1beta/models/{fb}:generateContent?key={api_key}"
            resp_fb = requests.post(url_fb, headers=headers, json=payload, timeout=120)
            if resp_fb.status_code != 200:
                # Jika model fallback menolak thinkingConfig atau sedang 503, coba tanpa thinkingConfig
                payload_basic = {
                    "contents": payload["contents"],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192}
                }
                resp_fb = requests.post(url_fb, headers=headers, json=payload_basic, timeout=120)
            if resp_fb.status_code == 200:
                data = resp_fb.json()
                teks_hasil = data["candidates"][0]["content"]["parts"][0]["text"]
                return f"# Dihasilkan oleh: {fb} (Fallback dari {model_name})\n\n" + teks_hasil

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
    Menyusun prompt reasoning terstruktur sesuai pedoman ketat prompt_rangkum.txt.
    """
    baris_data = []
    for k in klaster_segmen:
        cuplikan = " | ".join(k["cuplikan_chat"][:4])
        baris_data.append(
            f"KLASTER #{k['nomor']} ({k['mulai_tc']} s/d {k['selesai_tc']}):\n"
            f"  - Total Chat: {k['total_chat']} | Reaksi Kunci: {k['jumlah_reaksi']}\n"
            f"  - Transkrip: \"{k['dialog_transkrip']}\"\n"
            f"  - Sampel Chat: {cuplikan}"
        )

    data_terstruktur = "\n\n".join(baris_data)

    prompt = f"""# ROLE & OBJECTIVE
Expert VTuber Highlight Editor & Lead Data Analyst. Map streamer-audience interactions using pre-aggregated chat spikes and transcript.
OUTPUT LANGUAGE: STRICTLY INDONESIAN.

# BACKEND & ANTI-HALLUCINATION RULES
1. ZERO HALLUCINATION: Klaim WAJIB berasal dari data transkrip dan chat berikut. Jangan mengarang kejadian di luar data.
2. Jika transkrip menyatakan "Data tuturan tidak tersedia", sebutkan bahwa momen bertumpu pada reaksi chat murni atau visual game.
3. OUTPUT FORMAT: Direct Markdown only. Tanpa intro atau outro basa-basi.

# PARAMETERS
- VTuber: {vtuber_name}
- VOD: {vod_title}
- Target: Minimal 10 Segmen Kronologis + Top 5 Kandidat Klip Terbaik.

# DATA KLASTER LONJAKAN CPM & TRANSKRIP
{data_terstruktur}

# REPORT STRUCTURE (GUNAKAN FORMAT PERSIS DI BAWAH INI)
## 1. Timeline Kronologis (Minimal 10 Segmen)
- **HH:MM:SS | [Judul Momen] (Berakhir di HH:MM:SS)**
  - **Aktivitas:** (Deskripsi akurat dari transkrip)
  - **Reaksi Chat:** (Pola pesan dominan)
  - **Jumlah Chat:** (Total chat unik)
  - **Konteks:** (Pemicu lonjakan CPM)

## 2. Kandidat Klip Terbaik
- **Top 5 Kandidat Klip (Prioritas Tinggi):**
  - **Klip #N — HH:MM:SS | [Judul Catchy] (Berakhir di HH:MM:SS)**
  - **Alasan:** (Potensi viralitas)
  - **Statistik Intensitas:** (Burst Velocity, Relative Spike, Sentimen)
  - **Saran Edit:** (Zoom, SFX, atau Subtitle)

## 3. Insight & Kutipan
- **Insight Superchat:** (Jika ada)
- **3-5 Kutipan Ikonik:** HH:MM:SS | "[Nama]: Kutipan dari transkrip"
- **Hashtag:** (Misal: hololive, vtuber, clipper. Tanpa simbol '#')
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
        baris = f"{youtube_url} | {s['start_tc']}-{s['end_tc']} | {idx}. {s['title']}"
        lines.append(baris)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return len(segmen_list)


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

    args = parser.parse_args()

    # Deteksi otomatis file jika tidak ditentukan
    base_dir = Path(__file__).resolve().parent.parent
    chat_file = args.chat
    transkrip_file = args.transcript
    url = args.url

    # Cari file livechat default jika kosong
    if not chat_file:
        for p in [base_dir / "@KureijiOllie" / "livechat.csv", base_dir / "@KoboKanaeru" / "livechat.csv", base_dir / "cache_chat" / "livechat.csv"]:
            if p.exists():
                chat_file = str(p)
                break

    if not transkrip_file:
        for p in [base_dir / "@KureijiOllie" / "transkrip.csv", base_dir / "@KoboKanaeru" / "transkrip.csv", base_dir / "cache_chat" / "transkrip.csv"]:
            if p.exists():
                transkrip_file = str(p)
                break

    if not url:
        sec_file = base_dir / "sections.txt"
        if sec_file.exists():
            first_line = sec_file.read_text(encoding="utf-8").splitlines()
            for l in first_line:
                l = l.strip()
                if l and not l.startswith("#"):
                    url = l.split("|")[0].strip()
                    break
        if not url:
            url = "https://www.youtube.com/watch?v=source_video"

    print("=" * 60)
    print("🚀 ANTIGRAVITY AGENTIC HIGHLIGHT EXTRACTOR")
    print(f"• Model AI       : {args.model}")
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
    print("\n[2/5] Menghitung baseline CPM & mendeteksi lonjakan reaksi...")
    klaster = analisis_lonjakan_cpm(chats, transkrips, jendela_detik=20, pengali_cpm=2.0)
    print(f"      Teridentifikasi {len(klaster)} klaster momen potensial.")

    if not klaster:
        print("[ERROR] Tidak ada klaster lonjakan yang terdeteksi.")
        return

    # 3. Panggil Reasoning Model
    print(f"\n[3/5] Mengirim data teragregasi ke Model {args.model} via Antigravity Agent...")
    prompt = buat_prompt_analisis(klaster, vtuber_name=args.vtuber, vod_title=args.vod)
    
    t0 = time.time()
    laporan_md = panggil_ai_agentic(prompt, model_name=args.model)
    durasi = time.time() - t0
    print(f"      Model selesai bernalar dalam {durasi:.2f} detik.")

    # Simpan laporan markdown lengkap
    laporan_path = base_dir / "cache_chat" / "hasil_rangkuman.md"
    laporan_path.parent.mkdir(parents=True, exist_ok=True)
    laporan_path.write_text(laporan_md, encoding="utf-8")
    print(f"      Laporan lengkap disimpan ke: {laporan_path}")

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

        if args.auto_marker and injeksi_marker_ke_resolve:
            sukses, pesan = injeksi_marker_ke_resolve(segmen)
            print(f"      • Injeksi Langsung DaVinci: {pesan}")

    print("\n✨ SELESAI! Seluruh proses ekstraksi highlight berjalan tanpa membuka browser.")
    print("=" * 60)


if __name__ == "__main__":
    main()
