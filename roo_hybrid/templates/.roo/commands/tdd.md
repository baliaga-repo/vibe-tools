---
description: "🧪 Jalankan siklus Test-Driven Development (Red-Green-Refactor) ketat menggunakan pytest & mock terisolasi"
---

# Siklus TDD Ketat (/tdd)

1. **RED**: Buat atau perbarui unit test terisolasi di `tests/` (gunakan `unittest.mock` untuk dependensi eksternal seperti FFmpeg, DaVinci Resolve, atau API). Jalankan `pytest -q` untuk memastikan test gagal sesuai ekspektasi.
2. **GREEN**: Tulis kode produksi seminimal mungkin (<300 baris/file, docstring Bahasa Indonesia, type hints lengkap) agar test lulus.
3. **REFACTOR**: Rapikan kode dan jalankan `python -m py_compile` + `pytest -q` untuk memastikan 100% hijau.

