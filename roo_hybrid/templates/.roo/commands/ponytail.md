---
description: "🐴 Terapkan filosofi anti-over-engineering (The 7-Rung Decision Ladder & stdlib-first) pada tugas koding"
---

# Anti Over-Engineering (/ponytail [lite|full|ultra])

Pikirkan solusi seperti developer senior yang paling malas menulis kode ribet: kode terbaik adalah kode yang tidak pernah ditulis.

## 1. Tangga Keputusan (Stop pada tangga pertama yang memecahkan masalah):
1. **YAGNI**: Apakah fitur/kode ini benar-benar perlu ada? Jika tidak, lewati.
2. **Pakai Ulang Kode**: Apakah sudah ada fungsi serupa di repository? Gunakan ulang.
3. **Bawaan Python (Stdlib)**: Gunakan `pathlib`, `itertools`, `collections`, `urllib`, `sqlite3`, dll.
4. **Platform/CLI Asli**: Gunakan flag CLI bawaan (`ffmpeg`, `yt-dlp`) atau fitur OS.
5. **Dependensi yang Sudah Terpasang**: Jangan install library baru jika library yang ada sudah cukup.
6. **Fungsi Biasa / Satu Baris**: Hindari membuat class atau wrapper jika fungsi sederhana sudah cukup.
7. **Implementasi Minimum**: Tulis kode paling ringkas dan mudah dibaca yang menyelesaikan masalah.

## 2. Mode Ketegasan:
- `/ponytail lite`: Hanya terapkan aturan stdlib-first dan larangan dependensi baru.
- `/ponytail full` *(Default)*: Terapkan 7 tangga penuh + tahan kode di file yang ada jika `< 250 baris`.
- `/ponytail ultra`: Pangkas secara agresif—hapus wrapper sekali-pakai dan ringkas baris kode.

## 3. Pengaman Mutlak (Dilarang Malas di Sini):
- Validasi input, penanganan error spesifik, dan isolasi kredensial/cookie YouTube.
- Seluruh docstring dan komentar wajib dalam Bahasa Indonesia.
- Jalankan silent syntax gate (`python -m py_compile <file>`).

