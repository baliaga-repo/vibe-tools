# Panduan Kata Kunci AI & Pola Prompting (Antigravity IDE)

Dokumen ini berisi rangkuman kata kunci teknis, konsep arsitektur, dan contoh prompt praktis hasil diskusi optimasi *vibe coding* di Antigravity IDE. Gunakan dokumen ini sebagai referensi cepat agar proses koding di masa mendatang selalu **hemat token**, **rapih**, dan **minim risiko regresi (*zero-regression*)**.

---

## 🔑 Daftar Kata Kunci Penting, Deskripsi & Contoh Prompt

### 1. Kategori: Arsitektur & Refactoring Bersih

#### A. `Modular Refactor` / `Decompose Monolith`
* **Deskripsi**: Meminta AI memecah skrip berukuran besar (>300 baris atau *god file*) menjadi paket/sub-modul modular yang memiliki satu tanggung jawab spesifik (*Single Responsibility Principle*).
* **Kapan Digunakan**: Ketika sebuah file skrip Python mulai membengkak dan sulit dibaca (misal script ribuan baris).
* **Contoh Prompt**:
  > *"Gunakan skill modular-refactor untuk memecah fungsi koneksi DaVinci SDK dan ekspor audio dari `@cache_chat/davinci_auto_sfx_caption.py` ke sub-modul baru di `cache_chat/davinci_core/resolve_bridge.py`."*

#### B. `Zero-Regression` / `Facade Pattern`
* **Deskripsi**: Menjamin perubahan arsitektur tidak merusak skrip luar, shortcut aplikasi, atau batch file yang sudah ada. Skrip lama tetap mempertahankan antarmuka fungsi publik dengan cara mengimpor ulang fungsi dari modul baru.
* **Kapan Digunakan**: Setiap kali memindahkan fungsi/kelas dari file utama ke file pembantu.
* **Contoh Prompt**:
  > *"Refaktor modul ini dengan prinsip zero-regression menggunakan facade pattern. Pastikan skrip lama tetap bisa dipanggil langsung tanpa mengubah argumen atau menimbulkan ImportError."*

#### C. `Soft Limit 250 - 300 Baris`
* **Deskripsi**: Batasan panjang baris file Python agar context window AI tetap ringan saat membaca kode dan mencegah terciptanya *god file*.
* **Kapan Digunakan**: Saat menambahkan fitur baru ke skrip yang sudah mulai panjang.
* **Contoh Prompt**:
  > *"Periksa panjang file `@FormatMP4 - V3.py`. Karena sudah melebihi batas 300 baris, pisahkan logika Windows Power/Away Mode ke modul `utils/power_manager.py`."*

---

### 2. Kategori: Hemat Token & Kontrol Konteks

#### A. `Targeted Context Tagging` (`@file` & `@symbol`)
* **Deskripsi**: Menyebutkan nama file atau fungsi spesifik secara eksplisit di prompt alih-alih membiarkan AI melakukan pemindaian luas (*full-workspace scanning*) yang menghabiskan ribuan token.
* **Kapan Digunakan**: Setiap kali meminta AI membaca atau memodifikasi file.
* **Contoh Prompt**:
  > *"Fokus hanya pada `@cache_chat/davinci_core/resolve_bridge.py`. Tambahkan error handling saat DaVinci Resolve tidak merespons tanpa membaca file lain di workspace."*

#### B. `Progressive Disclosure`
* **Deskripsi**: Mekanisme bawaan Antigravity di mana detail instruksi (Skill) hanya dimuat saat dipanggil namanya, bukan dimuat terus-menerus di `AGENTS.md`.
* **Kapan Digunakan**: Saat mendesain aturan alur kerja kompleks agar prompt sistem tidak memakan kuota token Anda setiap giliran chat.
* **Contoh Prompt**:
  > *"Aktifkan skill modular-refactor untuk menganalisis ketergantungan modul ini."*

#### C. `Micro-Edits` / `Targeted Replacement`
* **Deskripsi**: Menginstruksikan AI hanya mengedit blok fungsi tertentu, bukan menulis ulang seluruh isi file dari baris pertama sampai terakhir.
* **Kapan Digunakan**: Saat mengubah logika fungsi kecil pada file yang berukuran sedang atau besar.
* **Contoh Prompt**:
  > *"Lakukan edit presisi hanya pada fungsi `find_timeline_audio_file` untuk menambahkan ekstensi `.m4a` sebagai fallback pencarian. Jangan menulis ulang bagian kode lainnya."*

#### D. `Repomix` / `Pack Codebase Skeleton`
* **Deskripsi**: Alat pengemas codebase menjadi 1 file teks padat (*single context file*) dengan kompresi AST Tree-sitter (membuang isi fungsi/komentar, hanya menyisakan antarmuka/signature). Sangat hemat token saat ingin membagikan konteks proyek ke LLM eksternal (Google AI Studio, Claude Web, dsb.).
* **Kapan Digunakan**: Saat ingin menganalisis banyak file sekaligus di luar IDE atau membuat rangkuman arsitektur global tanpa memakan ratusan ribu token.
* **Kata Kunci Sakti / Perintah CLI**:
  - `npx repomix --compress` : Mengemas repo dengan kompresi Tree-sitter (hanya skeleton/signature).
  - `npx repomix --remove-comments --remove-empty-lines` : Mengemas tanpa komentar dan baris kosong.
  - `npx repomix --include "gui/**/*.py"` : Hanya mengemas folder/modul tertentu.
* **Contoh Prompt ke AI**:
  > *"Jalankan perintah `npx repomix --compress --include 'cache_chat/davinci_core/**/*.py'` untuk mengemas modul core menjadi satu file skeleton ringkas sebelum kita review arsitekturnya."*

#### E. `Bilingual Token Optimization` (English Bridge Pipeline)
* **Deskripsi**: Memanfaatkan efisiensi tokenisasi BPE bahasa Inggris saat memanggil model berbayar eksternal (Claude Sonnet / DeepSeek-R1 di OpenRouter). Gemini IDE menerjemahkan konteks masalah ke Bahasa Inggris teknis padat di balik layar (hemat saldo 30% - 50%), lalu menyajikan hasil akhirnya kembali ke pengguna dalam Bahasa Indonesia secara gratis.
* **Kapan Digunakan**: Setiap kali mengeksekusi penalaran arsitektur, kalkulasi algoritma, atau investigasi mendalam via OpenRouter.
* **Contoh Prompt ke AI**:
  > *"Analisis arsitektur locking protocol ini menggunakan Claude Sonnet dengan pipeline bilingual agar hemat token OpenRouter, lalu jelaskan hasilnya ke saya dalam Bahasa Indonesia."*

---

### 3. Kategori: Pengujian & Kualitas Kode

#### A. `Dependency Mocking` / `Mock SDK`
* **Deskripsi**: Memalsukan (*mock*) objek atau aplikasi eksternal (seperti SDK DaVinci Resolve Studio atau FFmpeg) menggunakan `unittest.mock` agar pengujian unit dapat berjalan instan tanpa perlu menjalankan aplikasi berat.
* **Kapan Digunakan**: Saat membuat pengujian otomatis (*unit testing*) untuk modul bridge atau subprocess.
* **Contoh Prompt**:
  > *"Buatkan pengujian unit untuk `@resolve_bridge.py` dengan mock objek `DaVinciResolveScript.scriptapp('Resolve')` agar tes bisa berjalan mandiri di terminal tanpa membuka DaVinci Resolve."*

#### B. `Pure Functions` (Fungsi Murni)
* **Deskripsi**: Logika komputasi yang tidak memiliki efek samping ke disk/sistem/jaringan (misalnya perhitungan offset milidetik subtitle, parsing regex teks emosi).
* **Kapan Digunakan**: Saat memisahkan logika kalkulasi agar mudah diuji secara independen.
* **Contoh Prompt**:
  > *"Pisahkan logika regex pembersihan timestamp SRT dari kode I/O disk menjadi fungsi murni `parse_srt_timestamp(raw_text)`."*

---

### 4. Kategori: Kontrol Alur Kerja & Slash Commands

| Perintah | Deskripsi Singkat | Contoh Pemakaian |
| :--- | :--- | :--- |
| **/plan** | Memaksa AI merancang rencana kerja langkah demi langkah sebelum menulis kode. Sangat hemat token karena mencegah salah arah eksekusi. | `"/plan Rancang pemecahan modul audio transkripsi dari translate_id_en_jp.py"` |
| **/learn** | Memerintahkan AI menyimpan koreksi atau pola spesifik ke memori/knowledge items agar diingat seterusnya. | `"/learn Jika membuat script DaVinci baru, selalu gunakan mock imp Python 3.12 dari resolve_bridge"` |
| **/grill-me** | AI akan mewawancarai Anda secara interaktif untuk memperjelas keputusan arsitektur sebelum coding dimulai. | `"/grill-me Tanyakan preferensi format output sebelum kita membuat converter audio baru"` |
| **/goal** | Menjalankan task panjang/kompleks secara tuntas tanpa berhenti di tengah jalan. | `"/goal Bersihkan semua linter error dan dead code di folder cache_chat/davinci_core/"` |

---

## 📋 Formula Template Prompt Siap Pakai

### Template 1: Refactoring Modular Skrip Monolitik
```text
Tolong pecahkan file @[nama_file_lama.py] menggunakan skill modular-refactor:
1. Analisis ketergantungan fungsi terkait [nama_fitur_target].
2. Pindahkan logika tersebut ke modul baru @[path/ke/modul_baru.py] dengan docstring Bahasa Indonesia dan type hints lengkap.
3. Terapkan facade import di file lama agar kompatibilitas fungsi tetap terjaga (zero-regression).
4. Validasi sintaks dengan py_compile dan sinkronkan graphify.
```

### Template 2: Pembuatan Unit Test Terisolasi
```text
Gunakan skill unit-test-generator untuk membuat test suite pada @[nama_modul.py]:
1. Buat file pengujian di tests/test_[nama_modul].py.
2. Lakukan mocking pada dependensi eksternal ([DaVinci SDK / FFmpeg subprocess / Requests API]).
3. Uji skenario input valid (happy path), input kosong/None, dan penanganan error.
4. Tulis pesan asersi dan docstring dalam Bahasa Indonesia.
```

### Template 3: Debugging / Penambahan Fitur Presisi (Hemat Token)
```text
Fokus hanya pada fungsi [nama_fungsi] di file @[nama_file.py]:
- Masalah/Kebutuhan: [Jelaskan error atau parameter baru yang ingin ditambahkan].
- Batasan: Lakukan penggantian baris terarah (micro-edit). Jangan scan atau modifikasi modul lain yang tidak relevan.
```

### Template 4: Migrasi Remote Git & Username GitHub ke Akun Baru
```text
Tolong periksa dan perbarui remote Git di proyek ini karena saya telah mengganti username GitHub menjadi "baliaga-repo":
1. Cek git remote origin saat ini, lalu ubah URL-nya agar mengarah ke username baru "baliaga-repo" (misal: https://github.com/baliaga-repo/<nama-repo-ini>.git).
2. Jika proyek ini memiliki submodule (.gitmodules), perbarui juga URL submodule ke "baliaga-repo" dan jalankan `git submodule sync`.
3. Cari apakah ada teks atau dokumentasi (seperti README.md, package.json, atau file markdown lainnya) yang masih mencantumkan username lama "mobogemuichi-creator", lalu ubah ke "baliaga-repo".
4. Verifikasi hasilnya dengan `git remote -v` dan tampilkan status perubahannya.
(Catatan: Jangan lakukan commit atau push otomatis sebelum meminta konfirmasi dari saya).
```

### Template 5: Migrasi Username Sekaligus Memasang Submodule `vibe_tools`
```text
Tolong bantu saya melakukan dua hal pada proyek ini:
1. Perbarui remote Git proyek ini ke username baru saya "baliaga-repo" (https://github.com/baliaga-repo/<nama-repo-ini>.git).
2. Pasang submodule vibe-tools dari repositori baru saya dengan menjalankan:
   `git submodule add https://github.com/baliaga-repo/vibe-tools.git vibe_tools`
3. Jalankan skrip installer ekosistemnya:
   `python vibe_tools/setup_vibe_ecosystem.py`
4. Cek dan pastikan tidak ada teks username lama "mobogemuichi-creator" di berkas proyek ini.
(Catatan: Jangan lakukan commit atau push otomatis sebelum meminta konfirmasi dari saya).
```

