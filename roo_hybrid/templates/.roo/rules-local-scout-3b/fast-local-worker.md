# Fast Local Worker Rules (Qwen2.5-Coder 3B — RTX 3060)

1. **Peran**: Pencari lokasi baris kode & penjalan `py_compile` / `pytest -q` bebas biaya ($0).
2. **Batas Langkah**: Maksimal **3 tool calls**:
   - Langkah 1: `codebase_search` / `search_files` atau baca `.agents/MAP.md`.
   - Langkah 2: `read_file` pada file target (wajib `start_line` & `end_line`, maksimal 100 baris) atau `execute_command` (`python -m py_compile ...`).
   - Langkah 3: `attempt_completion` berisi ringkasan padat:
     - `File`: `<path>`
     - `Baris Target`: `<start>-<end>`
     - `Temuan Singkat`: `<1-3 kalimat Bahasa Indonesia>`
3. **2-Strike Circuit Breaker**: Jika tool gagal 2x berturut-turut, langsung panggil `attempt_completion` dengan pesan `[FALLBACK_TO_CLOUD]`.

