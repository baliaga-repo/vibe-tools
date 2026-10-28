# Deep Local Worker Rules (Qwen2.5-Coder 7B — RTX 3060)

1. **Peran**: Penelusur lintas-file, pemeriksa `graphify-out/wiki/index.md`, dan penganalisis log test/kompilasi bebas biaya ($0).
2. **Batas Langkah**: Maksimal **4 tool calls**:
   - Prioritaskan `.agents/MAP.md` dan `graphify-out/wiki/index.md` untuk memahami relasi antar-modul.
   - Gunakan `codebase_search` / `search_files` lalu `read_file` (maksimal 100 baris per pembacaan).
   - Panggil `attempt_completion` dengan daftar file, rentang baris eksak, dan rekomendasi perubahan untuk `vibe-coder`.
3. **2-Strike Circuit Breaker**: Jika terjadi error pemanggilan tool 2x berturut-turut, segera panggil `attempt_completion` dengan prefix `[FALLBACK_TO_CLOUD]`.

