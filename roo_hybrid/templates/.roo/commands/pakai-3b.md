---
description: "🏎️ Jalankan tugas dengan Metode 2: Local Scout 3B (qwen2.5-coder:3b di RTX 3060 Rp 0) + Cloud Edit (~13-16 dtk)"
---

# Eksekusi Metode 2: 🏎️ Local Scout 3B ($0 Explore) + Cloud Edit

Jalankan instruksi pengguna di bawah ini menggunakan **Metode 2 (Local Scout 3B + Cloud)** tanpa menanyakan modal pilihan metode lagi:

1. **Sub-tugas 1 (Kerja Kasar Lokal $0)**: Delegasikan pencarian lokasi file dan rentang baris ke mode `local-scout-3b` (`new_task`) dengan instruksi ringkas maksimal 3 langkah.
2. **Sub-tugas 2 (Eksekusi Cloud Presisi)**: Setelah `local-scout-3b` mengembalikan path file dan nomor baris (atau jika memicu `[FALLBACK_TO_CLOUD]`), jalankan pengeditan kode di mode `vibe-coder` hanya pada rentang baris tersebut.
3. **Sub-tugas 3 (Verifikasi Lokal $0)**: Jalankan `python -m py_compile <file>` untuk memverifikasi sintaks.
4. **Telemetry Scorecard**: Tampilkan kartu skor perbandingan aksi lokal ($0, ~2.2 GB VRAM) vs aksi Cloud di akhir respons.

