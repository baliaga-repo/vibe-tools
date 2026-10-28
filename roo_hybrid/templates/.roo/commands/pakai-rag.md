---
description: "🚀 Jalankan tugas dengan Metode 1: Kombo Local RAG (nomic-embed RTX 3060) + Cloud Instan (Gemini Flash / DeepSeek-V3) (~4-6 dtk)"
---

# Eksekusi Metode 1: 🚀 Kombo Local RAG + Cloud Instan

Jalankan instruksi pengguna di bawah ini menggunakan **Metode 1 (Jalur Kilat ~4-6 detik)** tanpa menanyakan modal pilihan metode lagi:

1. **Pencarian Vektor Lokal ($0)**: Gunakan `codebase_search` (diindeks oleh `nomic-embed-text` di RTX 3060) dan/atau baca `.agents/MAP.md` untuk langsung menemukan file dan baris target.
2. **Pembacaan Teriris**: Gunakan `read_file` hanya pada rentang baris yang relevan (maksimal 100 baris).
3. **Eksekusi Cloud Langsung**: Terapkan perubahan dengan `apply_diff` (jika tugas koding) dan jalankan `python -m py_compile <file>` untuk memastikan bebas syntax error.
4. **Telemetry Scorecard**: Tampilkan kartu skor waktu tempuh & penggunaan metode `🚀 Kombo Local RAG + Cloud` di akhir respons.

