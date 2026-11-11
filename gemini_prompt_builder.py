"""
[ID]: Modul builder prompt kurasi Gemini Web dengan arsitektur modular dan Facade Pattern.

Menyusun instruksi prompt tingkat lanjut dalam Bahasa Inggris untuk optimasi reasoning BPE LLM,
namun mempertahankan kontrak output laporan markdown secara ketat dalam Bahasa Indonesia
sesuai acuan prompt_rangkum.txt agar kompatibel dengan modul ekstraksi segmen.

[EN]: Gemini Web curation prompt builder module with a modular architecture and Facade Pattern.

Constructs advanced prompt instructions in English for BPE LLM reasoning optimization,
while strictly maintaining the markdown report output contract in Indonesian
based on prompt_rangkum.txt for compatibility with the segment extraction module.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class GeminiPromptConfig:
    """
[ID]: Konfigurasi parameter prompt untuk Gemini Web Automator dan Salin Manual.
[EN]: Configure prompt parameters for Gemini Web Automator and Manual Copy.
"""

    vtuber_name: str = "VTuber"
    vod_title: str = "VTuber Livestream Highlight"
    files_attached: bool = True
    min_segments: int = 10
    top_clips_count: int = 5
    target_window_sec: str = "10-30s"
    safe_mode: bool = False


class GeminiWebPromptBuilder:
    """Builder modular penyusun prompt dwibahasa (Directives EN, Output Report ID)."""

    def __init__(self, config: Optional[GeminiPromptConfig] = None) -> None:
        """
[ID]: Inisialisasi builder dengan konfigurasi prompt.
[EN]: Initialize the builder with the prompt configuration.
"""
        self.config = config or GeminiPromptConfig()

    def format_cluster_data(self, klaster_segmen: Optional[List[Dict[str, Any]]]) -> str:
        """Menyusun baris data klaster ringkas dari deteksi lonjakan CPM."""
        if not klaster_segmen:
            return "(No pre-extracted clusters. Rely entirely on attached files or raw transcript)."

        baris_data: List[str] = []
        for k in klaster_segmen:
            raw_chat = k.get("cuplikan_chat", [])
            cuplikan = " ".join(raw_chat[:3]) if isinstance(raw_chat, (list, tuple)) else str(raw_chat)
            dialog = str(k.get("dialog_transkrip", "") or "")
            if len(dialog) > 120:
                dialog = dialog[:117] + "..."
            baris_data.append(
                f"[#{k.get('nomor', 0)}] {k.get('mulai_tc', '00:00:00')}-{k.get('selesai_tc', '00:00:00')} | "
                f"Chat:{k.get('total_chat', 0)} | Reaksi:{k.get('jumlah_reaksi', 0)} | "
                f"Chat:\"{cuplikan}\" | Tuturan:\"{dialog}\""
            )
        return "\n".join(baris_data)

    def build_safety_guidelines(self) -> str:
        """Menghasilkan aturan moderasi konten Brand-Safe saat safe_mode=True."""
        if not self.config.safe_mode:
            return ""
        return (
            "# CONTENT MODERATION GUIDELINES (BRAND-SAFE MODE)\n"
            "- PRIORITIZE: Wholesome entertainment, humorous gaming highlights, positive streamer-viewer chemistry.\n"
            "- AVOID: Sensitive political chatter, profanity, heated conflicts, and NSFW audience triggers.\n"
            "- BRAND-SAFE FOCUS: Ensure all selected moments are advertiser-friendly while strictly keeping the output structure below.\n\n"
        )

    def build(self, klaster_segmen: Optional[List[Dict[str, Any]]] = None) -> str:
        """
[ID]: Menyusun teks prompt lengkap siap diinjeksikan ke sesi Chromium Gemini Web.
[EN]: Construct the complete prompt text ready to be injected into the Chromium Gemini Web session.
"""
        data_terstruktur = self.format_cluster_data(klaster_segmen)
        lampiran_note = (
            "(Complete livechat & speech transcript files are attached as primary reference data).\n"
            if self.config.files_attached
            else "(No external files attached. Analyze the potential cluster data provided below).\n"
        )
        safety_section = self.build_safety_guidelines()

        return f"""# ROLE & OBJECTIVE
Expert VTuber Highlight Editor & Lead Content Strategist. Map streamer-audience interactions from livestream chat timeline and transcript dialogue into captivating YouTube highlights.
OUTPUT LANGUAGE: STRICTLY INDONESIAN.

# AUDIENCE SAFETY & ANTI-HALLUCINATION RULES
1. CONTEXT: Public gaming and entertainment broadcast archive. The attached files contain pre-processed chronological audience reaction timeline (livechat_timeline.csv) and streamer speech dialogue (transkrip.csv).
2. ZERO HALLUCINATION: All timestamps, statements, and quotes MUST strictly originate from the provided timeline or attached transcript. Never invent dialogue or external facts. If missing, state: "Data tidak tersedia".
3. TIME RESOLUTION: Every segment must have a valid YouTube Start Timecode (HH:MM:SS) and End Timecode in parentheses.

{safety_section}# PARAMETERS
- VTuber: {self.config.vtuber_name}
- VOD: {self.config.vod_title}
- Window: {self.config.target_window_sec} | Target: >={self.config.min_segments} Segments | Top Clips: {self.config.top_clips_count}
{lampiran_note}
# CANDIDATE CLUSTER DATA
{data_terstruktur}

# REPORT STRUCTURE (USE INDONESIAN EXACTLY AS BELOW)
Output direct Markdown only. Do NOT include Markdown code blocks (```) around the entire output. Do NOT include conversational greetings, intro, or outro.

## 1. Timeline Kronologis (Minimal 10 Segmen)
- **HH:MM:SS | [Judul Momen Menarik] (Berakhir di HH:MM:SS)**
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
- **Hashtag:** (Daftar hashtag relevan dipisahkan spasi atau koma, tanpa simbol '#')
"""


class GeminiWebPromptFacade:
    """
[ID]: Facade tingkat tinggi untuk antarmuka pembentukan prompt terpadu.
[EN]: High-level facade for a unified prompt construction interface.
"""

    @classmethod
    def create_prompt(
        cls,
        klaster_segmen: Optional[List[Dict[str, Any]]] = None,
        vtuber_name: str = "VTuber",
        vod_title: str = "VTuber Livestream Highlight",
        files_attached: bool = True,
        min_segments: int = 10,
        top_clips_count: int = 5,
        safe_mode: bool = False,
    ) -> str:
        """Membuat teks prompt menggunakan builder dengan konfigurasi dinamis."""
        cfg = GeminiPromptConfig(
            vtuber_name=vtuber_name,
            vod_title=vod_title,
            files_attached=files_attached,
            min_segments=min_segments,
            top_clips_count=top_clips_count,
            safe_mode=safe_mode,
        )
        return GeminiWebPromptBuilder(config=cfg).build(klaster_segmen=klaster_segmen)


def buat_prompt_gemini_web(
    klaster_segmen: Optional[List[Dict[str, Any]]] = None,
    vtuber_name: str = "VTuber",
    vod_title: str = "VTuber Livestream Highlight",
    files_attached: bool = True,
    safe_mode: bool = False,
) -> str:
    """
[ID]: Fungsi Facade drop-in replacement yang kompatibel dengan API sebelumnya.
[EN]: Drop-in replacement facade function compatible with the previous API.
"""
    return GeminiWebPromptFacade.create_prompt(
        klaster_segmen=klaster_segmen,
        vtuber_name=vtuber_name,
        vod_title=vod_title,
        files_attached=files_attached,
        safe_mode=safe_mode,
    )


def sanitize_gemini_markdown_report(teks: str) -> str:
    """
    Membersihkan teks respons mentah dari Gemini Web sebelum disimpan ke berkas .md:
    1. Membongkar pembungkus code fence luar (```markdown ... ``` atau ```text ... ```).
    2. Menormalisasi level heading bagian utama (### 1. -> ## 1., dst).
    3. Memangkas kalimat pengantar (preamble) sebelum '## 1. Timeline Kronologis'.
    4. Memangkas penutup code fence atau kalimat penutup setelah bagian akhir.
    """
    if not teks or not isinstance(teks, str):
        return ""
    hasil = teks.strip()

    # 1. Bongkar pembungkus code block luar
    pola_fence = re.match(r"^```(?:markdown|text|md)?\s*\n?(.*?)\n?```$", hasil, re.DOTALL | re.IGNORECASE)
    if pola_fence:
        hasil = pola_fence.group(1).strip()

    # 2. Normalisasi level heading bagian utama
    hasil = re.sub(r"^(?:#{1,3}\s*)?1\.\s*Timeline Kronologis", "## 1. Timeline Kronologis", hasil, flags=re.MULTILINE | re.IGNORECASE)
    hasil = re.sub(r"^(?:#{1,3}\s*)?2\.\s*Kandidat Klip", "## 2. Kandidat Klip", hasil, flags=re.MULTILINE | re.IGNORECASE)
    hasil = re.sub(r"^(?:#{1,3}\s*)?3\.\s*Insight", "## 3. Insight", hasil, flags=re.MULTILINE | re.IGNORECASE)

    # 3. Pangkas teks pengantar sebelum ## 1. Timeline Kronologis
    m = re.search(r"(##\s*1\.\s*Timeline Kronologis.*)", hasil, re.DOTALL | re.IGNORECASE)
    if m:
        hasil = m.group(1).strip()

    # 4. Bersihkan sisa ``` di bagian paling akhir jika ada
    hasil = re.sub(r"\n*```\s*$", "", hasil).strip()
    return hasil
