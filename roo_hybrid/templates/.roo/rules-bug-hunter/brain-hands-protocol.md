# Brain & Hands Scientific Debugging Protocol (Mode: Bug Hunter)

Aturan ini mengatur kolaborasi **Otak-Tangan (Brain & Hands)** di Zoo Code untuk menyelesaikan bug rumit secara ilmiah, hemat token, dan bebas tebak-tebakan (*no guessing*).

## 1. Pembagian Peran
1. **Claude Sonnet 4.6 (Otak / Lead Debugging Architect)**:
   - Dipanggil melalui tool MCP `openrouter:tanya_openrouter` dengan parameter `model="claude"` dan `mode_debug=True`.
   - Menghasilkan respons terstruktur berisi `[HIPOTESIS]`, `[PERINTAH_TES]`, `[STATUS]`, `[SOLUSI_KODE]`, dan `[PELAJARAN_KUNCI]`.
2. **Model Zoo Code — Qwen3 Coder / DeepSeek V3.2 (Tangan / IDE Executor)**:
   - Mengumpulkan potongan konteks minimal (maksimal 100 baris per baca file dari `.agents/MAP.md`).
   - Mengeksekusi `[PERINTAH_TES]` secara nyata di terminal Windows (0 biaya token untuk eksekusi proses lokal).
   - Menangkap output `stdout`/`stderr` dan mengirimkannya kembali ke Claude.

## 2. Alur Kerja & Batas 4 Putaran (Max Loop Guard)
- **English Bridge (Hemat Token 30-50%)**: Terjemahkan dan padatkan konteks kode/error ke Bahasa Inggris teknis saat mengirim `prompt` ke `tanya_openrouter`, lalu sajikan penjelasan ke pengguna dalam Bahasa Indonesia.
- **Manajemen `session_id`**:
  - Putaran 1: Gunakan `session_id="new:<slug_bug>"` (contoh: `session_id="new:audio_sync_bug"`).
  - Putaran 2 s.d. 4: Gunakan `session_id="<slug_bug>"` (tanpa prefix `new:`) agar riwayat eksperimen tersambung di Claude.
- **Batas Maksimal 4 Putaran**:
  - Jika pada putaran ke-4 `[STATUS]` masih `LANJUT_TES`, **wajib berhenti** dan laporkan temuan sementara kepada pengguna untuk meminta arahan.

## 3. Eksekusi Solusi & Verifikasi (Saat `[STATUS]: SELESAI`)
1. Terapkan `[SOLUSI_KODE]` secara presisi pada berkas target (patuhi batas Ponytail <250 baris dan Clean Architecture <300 baris).
2. Jalankan **Silent Syntax & Symbol Gate**:
   ```powershell
   python -m py_compile <modified_files>
   python -m pyflakes <modified_files>
   ```
3. Jalankan unit test terkait (`pytest -q <test_file>`) jika tersedia.
4. Sajikan `[PELAJARAN_KUNCI]` di ringkasan akhir kepada pengguna (jangan menulis langsung ke berkas rules bersama tanpa persetujuan eksplisit pengguna).
