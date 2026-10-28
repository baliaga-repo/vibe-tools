---
description: "🧩 Pecah script Python monolitik (>300 baris) menjadi arsitektur modular bersih tanpa regresi"
---

# Refactoring Modular Tanpa Regresi (/modular-refactor)

1. Periksa `.agents/MAP.md` dan baca file target secara bertahap (maksimal 100 baris per pembacaan).
2. Rancang pemisahan lapisan sesuai Clean Architecture (`config`, `core`, `bridge`/`adapters`, dan *slim facade* agar import lama tetap 100% kompatibel / zero-regression).
3. Pastikan setiap file baru berusia di bawah **300 baris**, memiliki *type hinting*, serta docstring Bahasa Indonesia.
4. Jalankan `python -m py_compile` pada seluruh file yang dimodifikasi dan perbarui peta berkas dengan `python vibe_tools/graphify_sync.py --map-only`.

