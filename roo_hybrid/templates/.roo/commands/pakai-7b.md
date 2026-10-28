---
description: "🚜 Jalankan tugas dengan Metode 3: Local Scout 7B (qwen2.5-coder:7b di RTX 3060 Rp 0 Akurasi Tinggi) + Cloud Edit (~24-28 dtk)"
---

# Eksekusi Metode 3: 🚜 Local Scout 7B ($0 Deep Explore) + Cloud Edit

Jalankan instruksi pengguna di bawah ini menggunakan **Metode 3 (Local Scout 7B + Cloud)** tanpa menanyakan modal pilihan metode lagi:

1. **Sub-tugas 1 (Penelusuran Mendalam Lokal $0)**: Delegasikan analisis lintas-file (`.agents/MAP.md`, `graphify-out/wiki/`, `search_files`, dan potongan `read_file` maks 100 baris) ke mode `local-scout-7b` (`new_task`).
2. **Sub-tugas 2 (Eksekusi Cloud Presisi)**: Gunakan hasil koordinat file & baris dari `local-scout-7b` untuk mengeksekusi perubahan kode bersih (<300 baris/file) di mode `vibe-coder`.
3. **Sub-tugas 3 (Verifikasi Sintaks & Tes)**: Jalankan `python -m py_compile` atau `pytest -q`.
4. **Telemetry Scorecard**: Tampilkan kartu skor perbandingan aksi lokal ($0, ~4.8 GB VRAM) vs aksi Cloud di akhir respons.

