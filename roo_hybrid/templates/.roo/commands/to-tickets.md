---
description: "🎫 Pecah spesifikasi teknis menjadi tiket Boomerang Subtask kecil yang berurutan dan dapat diuji"
---

# Dekomposisi Tiket Rekayasawan (/to-tickets)

1. Baca dokumen spesifikasi target di `docs/specs/`.
2. Pecah implementasi menjadi tiket-tiket kecil yang mandiri, berurutan berdasarkan dependensi, dan mematuhi batas maksimal **300 baris per file Python**.
3. Setiap tiket wajib mencantumkan: File target, Kontrak fungsi (type hints), dan Perintah verifikasi (`python -m py_compile` / `pytest -q`).
4. Tanyakan kepada pengguna metode eksekusi yang diinginkan (`/pakai-rag`, `/pakai-3b`, atau `/pakai-7b`) sebelum mulai mengeksekusi tiket pertama.

