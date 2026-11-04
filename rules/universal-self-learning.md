---
trigger: always_on
description: Long-term self-learning memory, 3-stage vibe coding workflow, Ponytail threshold, and Antigravity YAML frontmatter guardrails.
---

# Universal Self-Learning & Best Practices Ekosistem Vibe Coding

Dokumen aturan ini merupakan akumulasi memori jangka panjang (*long-term self-learning memory*) yang dipelajari dan disinkronisasikan oleh AI Agent (Hermes, Antigravity IDE, Zoo Code) agar dapat diterapkan secara konsisten di semua proyek dan perangkat.

***

## 1. Alur Emas 3-Tahap Prompting & Vibe Coding

Setiap pengembangan fitur atau refaktor besar wajib mengikuti 3 tahap berurutan berikut:

1. **Tahap 1: Konsultasi & Brainstorming Murni (Read-Only Mode)**:
   - Gunakan sesi interaktif `/grill-me` (ajukan pertanyaan satu per satu via `ask_question`).
   - Bedah kebutuhan, bandingkan 2–3 opsi arsitektur beserta kelebihan/kekurangannya.
   - Kumpulkan hasil diskusi dalam bentuk **DRAF SPESIFIKASI (`.md`)**.
   - **Rem Pengaman**: Dilarang membuat/mengedit file kodingan (`.py`) pada tahap ini sampai user menyetujui.

2. **Tahap 2: Formalisasi Spesifikasi & Tiket Eksekusi (1 Langkah Simultan)**:
   - Jalankan `/to-spec` untuk membuat spesifikasi teknis formal di `docs/specs/`.
   - Jalankan `/to-tickets` dalam giliran yang sama untuk memecah spesifikasi menjadi tiket mandiri berurutan dependensi di `docs/tickets/`.
   - Wajib patuhi prinsip `/ponytail` (anti over-engineering, stdlib-first, tahan < 250 baris).

3. **Tahap 3: Eksekusi Otonom Penuh (`/implement`)**:
   - Eksekusi seluruh tiket secara sekuensial (Tiket 1 -> Tiket 2 -> dst) sampai tuntas tanpa meminta konfirmasi antar-tiket.
   - Jalankan *silent syntax gate* (`python -m py_compile <file>`) setelah setiap modifikasi file.
   - Jalankan unit test terkait dan berikan rangkuman akhir dalam 1 pesan padat setelah semua tiket rampung.

***

## 2. Standar Ambang Batas 250 Baris (Ponytail vs Clean Architecture)

- **Zona Anti-Overengineering (< 250 Baris)**:
  - Dilarang memecah file secara prematur, membuat kelas sekali-pakai, atau menambah lapisan wrapper abstraction.
  - Wajib utamakan pustaka bawaan Python (*stdlib-first*): gunakan `urllib.request` daripada `requests`, `json`, `shutil`, dan plain functions.
- **Zona Refaktor Modular (250–300 Baris)**:
  - Ketika sebuah modul mendekati atau melampaui 250 baris, pecah sub-logika ke sub-modul terpisah.
  - **Wajib gunakan Facade Pattern**: Impor dan re-ekspor simbol-simbol lama di file asli agar kode pemanggil tidak rusak (*zero regression*).
- **Docstring & Komentar**:
  - Seluruh docstring fungsi, kelas, dan komentar teknis wajib ditulis dalam **Bahasa Indonesia** yang ringkas dan jelas.

***

## 3. Higienitas Repositori Publik / Shared Ecosystem

- Repositori bersama seperti `vibe_tools` berstatus publik dan dibagikan secara global:
  - Dilarang keras menyertakan path absolut lokal mesin (`C:\path\to\user\...`), token API, atau nama proyek privat internal.
  - Gunakan path generik (`docs/specs`, `docs/tickets`, `src/app.py`) dan URL dummy publik (`https://github.com/vibe-ecosystem/vibe-tools`).
  - Skrip operasional spesifik proyek pribadi wajib diletakkan di root workspace proyek terkait, bukan di dalam direktori `vibe_tools`.

***

## 4. Sinkronisasi Git Multi-Perangkat (PC ⇄ Laptop Anti-Bentrok)

- **Sebelum Berpindah Perangkat**:
  - Selalu jalankan `python vibe_tools/push_vibe_tools.py` untuk mengamankan perubahan ke remote.
- **Di Perangkat Penerima**:
  - Jika kedua perangkat memiliki commit atau modifikasi lokal yang belum tersinkron, jalankan:
    ```powershell
    git -C vibe_tools pull --rebase --autostash origin main
    ```
  - Perintah ini secara cerdas menyimpan perubahan lokal sementara (*autostash*), menarik commit terbaru dari remote, dan menempelkan kembali perubahan lokal di atasnya tanpa menimbulkan merge commit yang membingungkan.

***

## 5. Standar Skema YAML Frontmatter Rules Antigravity (Anti-Unmarshal Error)

- **Wajib Scalar String pada `globs`**:
  - Parser Go di Antigravity IDE melakukan unmarshal field `globs` ke tipe `string` tunggal, **BUKAN** array/list (`[]string` / YAML `!!seq`).
  - **BENAR**: `globs: "*.py"` atau `globs: "*.py, *.pyw"`
  - **SALAH (Menyebabkan Crash Unmarshal)**: `globs: ["*.py"]` (`yaml: unmarshal errors: cannot unmarshal !!seq into string`)
- **Kewajiban Header Frontmatter & Larangan `---` di Body**:
  - Setiap file rule di `.agents/rules/*.md` dan `vibe_tools/rules/*.md` wajib diawali blok frontmatter `---` pada baris 1 yang memuat minimal `trigger: always_on` dan `description: ...`.
  - Gunakan `***` (bukan `---`) untuk garis pemisah horizontal di dalam isi dokumen agar tidak membingungkan parser frontmatter.
- **Deduplikasi & Sinkronisasi `.agents/rules` vs `vibe_tools/rules`**:
  - Saat memperbarui rule di `vibe_tools/rules/` (yang terhubung ke `~/.gemini/config/rules` via NTFS Junction), pastikan salinan lokal di `.agents/rules/` juga disinkronkan atau disanitasi otomatis melalui `vibe_tools/sync_universal.py`.

***

## 6. Pola Arsitektur Data Besar (SQLite Streaming ETL) & Pencegahan Bug Klasik

1. **SQLite Streaming & Native DDL (`CREATE TABLE AS SELECT`) vs Loop Python**:
   - Untuk pemrosesan tabel besar (>100.000 baris dari PDF/Excel/CSV), hindari menumpuk seluruh data di RAM (list/DataFrame raksasa) atau melakukan iterasi transformasi baris-per-baris di Python.
   - Gunakan SQLite berbasis disk dengan mode `PRAGMA journal_mode = WAL;` dan delegasikan transformasi kolom via perintah DDL native `CREATE TABLE [tabel_bersih] AS SELECT ... FROM [tabel_mentah];`.
2. **Single SQL Query & Referensi Nama Header `[NAMA_KOLOM]` vs Urutan Huruf Kolom (`A, B, C`)**:
   - Jangan gunakan indeks posisi huruf kolom statis (`A, B, C`) untuk konfigurasi insert/delete/formula kolom karena posisi acuan pasti bergeser saat ada kolom yang disisipkan atau dihapus.
   - Gunakan **1 Text Box Query SQLite utuh** dengan referensi nama header asli yang dibungkus kurung siku (`[IDPEL]`, `[NO METER]`).
3. **Jebakan SQL `TRIM()` vs UDF `BERSIHKAN_SPASI()` pada Teks/Angka Ekstraksi PDF**:
   - Ekstraksi tabel PDF sering memotong teks atau angka panjang (seperti koordinat atau nomor seri) menjadi dua baris sehingga menghasilkan spasi di tengah string (contoh: `'115.2484562 2479914'` atau `'- 8.683833075 056866'`).
   - Fungsi bawaan SQL `TRIM()` hanya menghapus spasi di ujung kiri dan kanan, **bukan** spasi di tengah. Wajib gunakan UDF Python `BERSIHKAN_SPASI()` untuk kolom ID, kode, nomor meter, dan koordinat.
4. **Normalisasi Kata Terputus PDF via Python UDF Dinamis, Bukan `CASE WHEN` Kaku**:
   - Hindari menulis blok `CASE WHEN` yang panjang di dalam query SQL untuk memperbaiki kata-kata yang terpecah spasi akibat lebar kolom PDF (misal `'Norm al'` -> `'Normal'`).
   - Daftarkan fungsi Python berbasis kamus normalisasi *case-insensitive* ke koneksi SQLite via `conn.create_function("RAPIKAN_LCD", 1, fn_normalisasi)` sehingga query SQL tetap ringkas 1 baris.
5. **Protokol Anti-Crash File Output Terkunci (`[Errno 13] Permission denied`)**:
   - Sebelum memulai proses transformasi berat dan sebelum menyimpan file output Excel (`.xlsx`/`.xls`), selalu lakukan *Early File Lock Check* (coba buka file dengan mode `"a+b"`).
   - Jika file sedang dibuka di Microsoft Excel, tampilkan dialog interaktif *Retry/Cancel* (`messagebox.askretrycancel`) agar pengguna cukup menutup Excel lalu melanjutkan proses tanpa harus mengulang dari awal.
6. **Manajemen Lock SQLite Windows (`[WinError 32]`) & Sanitasi Path JSON**:
   - Selalu tutup `cursor` dan `conn` di dalam blok `finally` sebelum melakukan `os.rename()` atau `os.remove()` pada file database `.db` di Windows.
   - Selalu normalisasi path direktori Windows menggunakan *forward slash* (`/`) sebelum disimpan ke file konfigurasi `.json` untuk mencegah `JSONDecodeError: Invalid \escape`.
7. **Silent Syntax & Undefined Symbol Gate (`py_compile` + `pyflakes`)**:
   - `python -m py_compile` hanya memvalidasi sintaks AST dan **tidak mendeteksi `NameError`** (seperti lupa mengimpor `Path` atau `Union` yang dipanggil di dalam fungsi).
   - Setelah memodifikasi file `.py`, wajib jalankan `python -m py_compile <file>` **DAN** `python -m pyflakes <file>` untuk memastikan nol *undefined name* sebelum menyerahkan hasil ke pengguna.
