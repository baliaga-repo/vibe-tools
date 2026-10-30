# Universal Self-Learning & Best Practices Ekosistem Vibe Coding

Dokumen aturan ini merupakan akumulasi memori jangka panjang (*long-term self-learning memory*) yang dipelajari dan disinkronisasikan oleh AI Agent (Hermes, Antigravity IDE, Zoo Code) agar dapat diterapkan secara konsisten di semua proyek dan perangkat.

---

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

---

## 2. Standar Ambang Batas 250 Baris (Ponytail vs Clean Architecture)

- **Zona Anti-Overengineering (< 250 Baris)**:
  - Dilarang memecah file secara prematur, membuat kelas sekali-pakai, atau menambah lapisan wrapper abstraction.
  - Wajib utamakan pustaka bawaan Python (*stdlib-first*): gunakan `urllib.request` daripada `requests`, `json`, `shutil`, dan plain functions.
- **Zona Refaktor Modular (250–300 Baris)**:
  - Ketika sebuah modul mendekati atau melampaui 250 baris, pecah sub-logika ke sub-modul terpisah.
  - **Wajib gunakan Facade Pattern**: Impor dan re-ekspor simbol-simbol lama di file asli agar kode pemanggil tidak rusak (*zero regression*).
- **Docstring & Komentar**:
  - Seluruh docstring fungsi, kelas, dan komentar teknis wajib ditulis dalam **Bahasa Indonesia** yang ringkas dan jelas.

---

## 3. Higienitas Repositori Publik / Shared Ecosystem

- Repositori bersama seperti `vibe_tools` berstatus publik dan dibagikan secara global:
  - Dilarang keras menyertakan path absolut lokal mesin (`C:\Users\...`, `d:\mobog\...`), token API, atau nama proyek privat (`Scrapper_new_acmt`, dll).
  - Gunakan path generik (`docs/specs`, `docs/tickets`, `src/app.py`) dan URL dummy publik (`https://github.com/vibe-ecosystem/vibe-tools`).
  - Skrip operasional spesifik proyek pribadi wajib diletakkan di root workspace proyek terkait, bukan di dalam direktori `vibe_tools`.

---

## 4. Sinkronisasi Git Multi-Perangkat (PC ⇄ Laptop Anti-Bentrok)

- **Sebelum Berpindah Perangkat**:
  - Selalu jalankan `python vibe_tools/push_to_github.py` untuk mengamankan perubahan ke remote.
- **Di Perangkat Penerima**:
  - Jika kedua perangkat memiliki commit atau modifikasi lokal yang belum tersinkron, jalankan:
    ```powershell
    git -C vibe_tools pull --rebase --autostash origin main
    ```
  - Perintah ini secara cerdas menyimpan perubahan lokal sementara (*autostash*), menarik commit terbaru dari remote, dan menempelkan kembali perubahan lokal di atasnya tanpa menimbulkan merge commit yang membingungkan.

