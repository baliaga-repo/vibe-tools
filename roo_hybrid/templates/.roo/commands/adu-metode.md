---
description: "🏆 Benchmark & bandingkan langsung kecepatan serta akurasi ke-3 metode (Local RAG+Cloud vs Scout 3B vs Scout 7B)"
---

# Mode Benchmark: 🏆 Adu Cepat 3 Metode Eksekusi

Lakukan uji eksplorasi terisolasi terhadap permintaan pengguna menggunakan ke-3 metode secara berurutan (tanpa mengubah file kode terlebih dahulu):

1. **Uji Metode 1 (`🚀 Local RAG + Cloud`)**: Gunakan `codebase_search` + `.agents/MAP.md` dan catat file/baris yang ditemukan beserta estimasi durasi.
2. **Uji Metode 2 (`🏎️ Local Scout 3B`)**: Delegasikan tugas pencarian yang sama ke mode `local-scout-3b` via `new_task` dan catat hasil serta durasinya.
3. **Uji Metode 3 (`🚜 Local Scout 7B`)**: Delegasikan tugas pencarian yang sama ke mode `local-scout-7b` via `new_task` dan catat hasil serta durasinya.
4. **Tabel Perbandingan Objektif**: Tampilkan tabel Markdown yang membandingkan:
   - Kecepatan respon nyata
   - Akurasi baris kode yang ditemukan
   - Konsumsi VRAM RTX 3060 (`0.3 GB` vs `2.2 GB` vs `4.8 GB`)
   - Estimasi biaya token Cloud
5. Tanyakan kepada pengguna via `ask_followup_question` apakah ingin langsung mengeksekusi perubahan kode dari hasil pemenang tersebut.

