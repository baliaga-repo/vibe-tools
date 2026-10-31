# 📚 Panduan Lengkap Ekosistem Vibe Tools

Dokumentasi komprehensif yang mengkonsolidasikan seluruh tutorial, panduan, dan best practice ekosistem vibe_tools dalam satu sumber terpadu.

---

## 📑 Daftar Isi

1. [Panduan Strategi & Prompt Siap Pakai (Antigravity IDE, Zoo Code, & Ponytail)](#1-panduan-strategi--prompt-siap-pakai-antigravity-ide-zoo-code--ponytail)
   * 1.1 [Contekan Cepat: Pilih Model & Cockpit Sesuai Tahap](#11-contekan-cepat-pilih-model--cockpit-sesuai-tahap)
   * 1.2 [Alur Utama Pembangunan & Perombakan Fitur (3 Tahap Terpadu)](#12-alur-utama-pembangunan--perombakan-fitur-3-tahap-terpadu)
   * 1.3 [Dua Prompt Spesialis Ringkas (Atasi Bug & Rapikan Kode /ponytail)](#13-dua-prompt-spesialis-ringkas-di-luar-bikin-fitur-baru)
   * 1.4 [Tiga "Golden Rules" Anti-Blunder](#14-tiga-golden-rules-anti-blunder)
2. [Docstring Translator Bilingual](#2-docstring-translator-bilingual)
3. [Sinkronisasi Git vibe_tools (Pindah PC ⇄ Laptop, Pengguna Publik, & Fork Global)](#3-sinkronisasi-git-vibe_tools-pindah-pc--laptop-pengguna-publik--fork-global)
   * 3.1 [Skenario Pindah PC ⇄ Laptop Anti-Bentrok](#31-skenario-pindah-pc--laptop-anti-bentrok)
   * 3.2 [Panduan Cepat untuk Pengguna Publik Baru (1 Menit)](#32-panduan-cepat-untuk-pengguna-publik-baru-1-menit)
   * 3.3 [Panduan Fork & Pull Request untuk Kontributor Global](#33-panduan-fork--pull-request-untuk-kontributor-global)
4. [REA MCP: Reverse Engineer Anything](#4-rea-mcp-reverse-engineer-anything)
5. [Hermes Agent x Antigravity IDE x Zoo Code & Self-Learning Universal](#5-hermes-agent-x-antigravity-ide-x-zoo-code--self-learning-universal)
   * 5.1 [Sinergi 3 Cockpit: Antigravity, Zoo Code, & Hermes Agent](#51-sinergi-3-cockpit-antigravity-zoo-code--hermes-agent)
   * 5.2 [Metode Pemasangan Cepat Mandiri (1 Menit)](#52-metode-pemasangan-cepat-mandiri-1-menit)
   * 5.3 [Pemasangan Manual Langkah Demi Langkah](#53-pemasangan-manual-langkah-demi-langkah)
   * 5.4 [🧠 Self-Learning Universal Lintas-Proyek](#54-self-learning-universal-lintas-proyek)
6. [Tutorial Setup PC/Laptop Baru dari Nol (Fresh Install Windows 10/11) & OpenRouter MCP](#6-tutorial-setup-pclaptop-baru-dari-nol-fresh-install-windows-1011--openrouter-mcp)
   * 6.1 [Tahap 1: Persiapan Dasar Windows 10/11 Baru](#61-tahap-1-persiapan-dasar-windows-1011-baru)
   * 6.2 [Tahap 2: Persiapan Akun & Saldo AI](#62-tahap-2-persiapan-akun--saldo-ai)
   * 6.3 [Tahap 3: Instalasi IDE & Setting Auto-Approve Otonom](#63-tahap-3-instalasi-ide--setting-auto-approve-otonom)
   * 6.4 [Tahap 4: Prompt Setup Mandiri & Alternatif Manual](#64-tahap-4-prompt-setup-mandiri--alternatif-manual)
   * 6.5 [Tahap 5: Verifikasi & Uji Koneksi](#65-tahap-5-verifikasi--uji-koneksi)
   * 6.6 [Tahap 6: Katalog Model Pilihan & Update Otomatis](#66-tahap-6-katalog-model-pilihan--update-otomatis)
7. [Katalog 15 Skill Universal & Panduan Penggunaan](#7-katalog-15-skill-universal--panduan-penggunaan)
8. [Arsitektur Hybrid Dual-Cockpit (Antigravity + VS Code Zoo Code + Ollama RTX 3060)](#8-arsitektur-hybrid-dual-cockpit-antigravity--vs-code-zoo-code--ollama-rtx-3060)
9. [Otomasi Pemeliharaan, Sinkronisasi Database, & Universal Updater Lintas-Proyek](#9-otomasi-pemeliharaan-sinkronisasi-database--universal-updater-lintas-proyek)

---

## 1. Panduan Strategi & Prompt Siap Pakai (Antigravity IDE, Zoo Code, & Ponytail)

Panduan praktis satu pintu untuk merancang, merombak, dan mengeksekusi kodingan secara terstruktur tanpa *over-engineering* (berkat **`/ponytail`**) baik di **Antigravity IDE** maupun **VS Code Zoo Code**.

<a id="11-contekan-cepat-pilih-model--cockpit-sesuai-tahap"></a>
### 🧠 1.1 Contekan Cepat: Pilih Model & Cockpit Sesuai Tahap

| Tahap Kerja | Tujuan Utama | ✈️ Di Antigravity IDE | 🦓 Di VS Code Zoo Code |
| :--- | :--- | :--- | :--- |
| **Tahap 1: Brainstorming & `/grill-me`** | Memahami masalah dengan bahasa sederhana, opsi solusi, & draf awal | **Gemini 4 Argon (High)** *(atau minta opini `openrouter` R1/Claude)* | Mode **`🔥 Grill-Me & Spec`** *(Model: `deepseek/deepseek-r1`)* |
| **Tahap 2: Spec (`docs/specs`) & Tiket (`docs/tickets`)** | Merombak/mematangkan rancangan ke `.md` resmi & memecah tiket kerja | **Gemini 4 Argon (High)** | Mode **`🔥 Grill-Me & Spec`** *(Otomatis terkunci hanya edit `docs/`)* |
| **Tahap 3: Eksekusi Tiket Koding (`/implement`)** | Mengerjakan semua tiket sampai lulus `py_compile` dengan hemat kode (`/ponytail`) | **Gemini 3.8 Flash (High)** *(Cepat, konteks besar, 100% Gratis)* | Mode **`💻 Vibe Coder`** atau **`🪃 Orchestrator`** *(awalan `/pakai-rag` atau `/pakai-3b`)* |
| **Kasus Khusus: Cari Bug / Rapikan Kode** | Lacak akar error runtime atau pangkas kode bertele-tele & *dead code* | **Argon / Flash** + MCP `openrouter` (`deepseek-r1`) | Mode **`🔍 Bug Hunter`** atau **`🛡️ Code Reviewer`** |

---

<a id="12-alur-utama-pembangunan--perombakan-fitur-3-tahap-terpadu"></a>
### 🚀 1.2 Alur Utama Pembangunan & Perombakan Fitur (3 Tahap Terpadu)

> **Alur Emas:** **Tahap 1 (Brainstorming & Paham Dulu -> Draf)** ➔ **Tahap 2 (Rombak/Resmikan ke `docs/specs` + Buat Tiket di `docs/tickets`)** ➔ **Tahap 3 (Eksekusi `/implement`)**.

<a id="tahap-1-brainstorming-detail--tanya-jawab-grill-me---masuk-ke-draf-awal"></a>
#### 🔹 Tahap 1: Brainstorming Detail & Tanya-Jawab (`/grill-me`) -> Masuk ke Draf Awal
> 💡 **Rekomendasi Model:** ✈️ Antigravity: `Gemini 4 Argon (High)` *(otomatis dapat memanggil opini kedua dari `hermes` self-learning & `openrouter` R1/Claude bila diperlukan)* | 🦓 Zoo Code: Mode `🔥 Grill-Me & Spec`

```markdown
MODE KONSULTASI & BRAINSTORMING MURNI.

Kondisi: [Jelaskan fitur yang ingin dibuat / masalah yang ingin diselesaikan / bagian yang masih bingung].

Tolong bantu saya dengan bahasa yang sederhana dan mudah dipahami:
1. Jelaskan duduk perkaranya secara detail dan berikan 2-3 opsi pendekatan terbaik (beserta kelebihan & kekurangannya) agar saya paham betul arah solusinya.
2. Jika diperlukan analisis mendalam atau sudut pandang tambahan, gunakan opini dari Hermes (yang memiliki fitur self-learning/memori) serta OpenRouter (DeepSeek-R1 / Claude).
3. Jalankan sesi /grill-me secara interaktif (ajukan pertanyaan satu per satu menggunakan ask_question) untuk membedah kebutuhan saya sampai tuntas.

REM PENGAMAN (STRICT):
- DILARANG KERAS membuat, mengedit, atau menyentuh file kodingan apa pun (.py).
- Setelah sesi tanya jawab selesai, kumpulkan hasilnya dalam bentuk DRAF SPESIFIKASI (.md).
- JANGAN sekali-kali memulai eksekusi koding sebelum saya mengetik kalimat: "SETUJU, SILAKAN EKSEKUSI".
```

<details>
<summary>🔄 <b>(Opsional) Kotak Revisi Draf Awal — Gunakan jika masih ada bagian draf yang ingin diubah/ditanyakan sebelum lanjut ke Tahap 2</b></summary>

```markdown
REM PENGAMAN AKTIF: DILARANG MENYENTUH ATAU MENGUBAH FILE KODE (.py).

Terkait draf spesifikasi tadi, saya ingin merevisi/menanyakan bagian berikut:
1. [Bagian yang belum pas / ingin diubah]: Tolong ubah menjadi [keinginan baru].
2. [Bagian yang masih bingung]: Tolong jelaskan lebih sederhana maksud dari [istilah/poin X].

Perbarui DRAF SPESIFIKASI (.md) saja dan jangan menyentuh kodingan dulu!
```
</details>

---

<a id="tahap-2-matangkanrombak-rancangan-ke-docsspecs--buat-tiket-ke-docstickets-1x-jalan"></a>
#### 🔹 Tahap 2: Matangkan/Rombak Rancangan ke `docs/specs` + Buat Tiket ke `docs/tickets` (1x Jalan)
*Gunakan setelah Anda paham dan cocok dengan arah Draf di Tahap 1. Anda bisa sekaligus menambahkan/merombak poin rancangan di dalam kotak ini:*
> 💡 **Rekomendasi Model:** ✈️ Antigravity: `Gemini 4 Argon (High)` | 🦓 Zoo Code: Mode `🔥 Grill-Me & Spec`

```markdown
/to-spec Tolong buatkan rancangan spesifikasi teknis formal ke dalam @[docs/specs] berdasarkan @[DRAF_SPESIFIKASI] tadi.

TAMBAHAN / MODIFIKASI / PEROMBAKAN RANCANGAN (JIKA ADA):
1. [Tulis tambahan/perubahan rancangan di sini, atau hapus baris ini jika draf tadi sudah 100% pas]

ATURAN KETAT:
- JANGAN menyentuh atau mengedit file kodingan sekarang (READ-ONLY PLANNING).
- Wajib patuhi aturan /ponytail (anti over-engineering, utamakan bawaan Python, tahan di file yang sama jika < 250 baris, dan gunakan Facade Pattern jika memecah file > 250-300 baris).
- Pecah rencana ini menjadi tiket-tiket kecil (/to-tickets) dengan urutan dependensi yang jelas ke dalam @[docs/tickets].
- Buatkan daftar tiket terurut untuk saya tinjau.
```

---

<a id="tahap-3-eksekusi-tiket-koding-implement--ponytail"></a>
#### 🔹 Tahap 3: Eksekusi Tiket Koding (`/implement` + `/ponytail`)
*Pilih salah satu cara eksekusi di bawah ini setelah daftar tiket di Tahap 2 Anda setujui:*
> 💡 **Rekomendasi Model:** ✈️ Antigravity: Ganti ke **`Gemini 3.8 Flash (High)`** *(Gratis & Cepat)* | 🦓 Zoo Code: Mode **`💻 Vibe Coder`** *(tambahkan `/pakai-rag` atau `/pakai-3b` di baris paling atas jika ingin hemat kuota)*

* **Opsi A: Eksekusi Otomatis Penuh 1x Jalan (Rekomendasi Utama / Bisa Ditinggal AFK)**
  ```markdown
  /implement Tiket 1 sampai [X] sudah saya setujui.

  INSTRUKSI EKSEKUSI PENUH OTOMATIS:
  1. Eksekusi SEMUA tiket secara berurutan (dari Tiket 1 -> Tiket 2 -> dst) sampai SELESAI semuanya.
  2. DILARANG berhenti di tengah jalan untuk meminta konfirmasi antar-tiket.
  3. Patuhi aturan /ponytail full (kode seringkas mungkin, stdlib-first, komentar/docstring Bahasa Indonesia).
  4. Setelah setiap tiket selesai:
     - Jalankan silent syntax gate (python -m py_compile <file_yang_diubah>).
     - Langsung lanjut otomatis ke tiket berikutnya tanpa jeda.
  5. Hanya berhenti jika menemukan error fatal yang memblokir jalannya kode.
  6. Ketika SEMUA tiket selesai, buat rangkuman final dalam 1 pesan saja.
  ```

* **Opsi B: Eksekusi Manual Satu per Satu (Jika Ingin Mengecek Tiap Tiket)**
  ```markdown
  /implement Silakan kerjakan Tiket 1 dulu dari @[docs/tickets] sesuai aturan /ponytail. Jalankan syntax gate (python -m py_compile), lalu tunggu konfirmasi saya sebelum lanjut ke Tiket 2.
  ```

---

<a id="13-dua-prompt-spesialis-ringkas-di-luar-bikin-fitur-baru"></a>
### 🛠️ 1.3 Dua Prompt Spesialis Ringkas (Di Luar Bikin Fitur Baru)

#### 🐞 Kasus A: Mengatasi Error Run / Bug Saat Aplikasi Dijalankan
> 💡 **Rekomendasi Model:** ✈️ Antigravity: `Argon / Flash` + MCP `openrouter` (`deepseek-r1`) | 🦓 Zoo Code: Mode `🔍 Bug Hunter`

```markdown
/diagnosing-bugs Aplikasi mengalami crash/error saat dijalankan:

[PASTE PESAN ERROR / TRACEBACK DI SINI]

INSTRUKSI INVESTIGASI:
1. Jangan langsung mengubah kode produksi.
2. Analisis Root Cause (akar masalah) secara mendalam (gunakan MCP openrouter deepseek-r1 jika diperlukan).
3. Tunjukkan lokasi file:baris penyebab masalah dan jelaskan solusinya dengan bahasa sederhana.
4. Tunggu konfirmasi saya sebelum menerapkan perbaikan.
```

#### ✂️ Kasus B: Menyederhanakan Kode Ribet (`/ponytail`) & Hapus Fungsi Mati (*Dead Code*)
> 💡 **Rekomendasi Model:** ✈️ Antigravity: `Gemini 4 Argon (High)` | 🦓 Zoo Code: Mode `🛡️ Code Reviewer`

```markdown
/code-review Tolong audit @[file_target.py] menggunakan aturan /ponytail ultra dan graphify:
1. Cari fungsi mati (dead code) yang memiliki 0 pemanggil (zero callers) di seluruh proyek.
2. Cari kode yang terlalu bertele-tele (over-engineered) yang bisa dipangkas dengan bawaan Python (stdlib).
3. Tampilkan tabel temuan untuk saya konfirmasi (JANGAN hapus/ubah kode sebelum saya setujui).
```

---

<a id="14-tiga-golden-rules-anti-blunder"></a>
### 🛡️ 1.4 Tiga "Golden Rules" Anti-Blunder

1. **Paham Dulu Baru Spec & Tiket**: Selalu mulai dari **Tahap 1 (Brainstorming & `/grill-me`)** dengan rem pengaman aktif sampai Anda benar-benar paham arah solusinya.
2. **Aturan Ambang 250 Baris (`/ponytail` vs Clean Architecture)**: Selama file masih **< 250 baris**, AI wajib menulis kode sesingkat mungkin di file yang ada tanpa bikin class/file baru. Pemecahan file (`/modular-refactor` + *Facade Pattern*) baru dilakukan jika ukuran file menyentuh **250–300 baris**.
3. **Ganti Model Sesuai Beban**: Gunakan **Argon / DeepSeek-R1** saat memikirkan arsitektur (Tahap 1 & 2), lalu pindah ke **Flash (Gratis) / Zoo Code Local Scout ($0)** saat mengeksekusi tiket koding (Tahap 3).

---

## 2. Docstring Translator Bilingual

Modul `docstring_translator.py` membaca berkas Python secara otomatis menggunakan **Python AST (Abstract Syntax Tree)** untuk menerjemahkan penjelasan alur fungsi dan logika dari Bahasa Indonesia (`[ID]`) ke padanan Bahasa Inggris (`[EN]`) tanpa mengubah indentasi atau logika kode asli.

Modul ini **100% menggunakan pustaka standar Python (`urllib.request`)** sehingga tidak memerlukan instalasi dependensi luar (`requests`).

### 🚀 Perintah CLI Cepat:
```powershell
# Terjemahkan seluruh berkas .py di proyek saat ini (otomatis fallback Gemini -> OpenRouter)
python vibe_tools/docstring_translator.py .

# Pratinjau tanpa mengubah berkas fisik
python vibe_tools/docstring_translator.py --dry-run .
```

### 🤖 Otomasi Otomatis via GitHub Actions:
Workflow `.github/workflows/bilingual_sync.yml` sudah tersedia di dalam repositori. Cukup tambahkan `GEMINI_API_KEY` pada **Settings > Secrets and variables > Actions** di GitHub. Setiap kali ada commit baru, docstring baru otomatis diterjemahkan.

---

## 3. Sinkronisasi Git vibe_tools (Pindah PC ⇄ Laptop, Pengguna Publik, & Fork Global)

Direktori `vibe_tools/` dirancang sebagai modul universal portabel yang dapat dipakai di berbagai proyek dan sinkron lintas komputer.

<a id="31-skenario-pindah-pc--laptop-anti-bentrok"></a>
### 🔄 3.1 Skenario Pindah PC ⇄ Laptop Anti-Bentrok

Jika Anda sering berpindah antara PC utama dan Laptop, gunakan langkah berikut agar perubahan lokal di kedua perangkat **tidak saling menimpa atau hilang**:

1. **Di Perangkat Pertama (Sebelum Berpindah)**:
   Dorong pembaruan lokal Anda ke repositori GitHub:
   ```powershell
   python vibe_tools/push_to_github.py
   ```
2. **Di Perangkat Kedua (Saat Membuka Proyek)**:
   Jika perangkat kedua juga memiliki editan lokal, gunakan perintah *rebase with autostash*:
   ```powershell
   git -C vibe_tools pull --rebase --autostash origin main
   ```
   > [!TIP]
   > Flag `--autostash` otomatis mengamankan perubahan lokal Anda ke memori sementara, menarik pembaruan terbaru dari GitHub, lalu mengembalikan editan lokal Anda di atasnya secara rapi tanpa konflik!

3. **Kunci Pointer di Repositori Utama**:
   ```powershell
   git add vibe_tools
   git commit -m "chore: perbarui pointer commit vibe_tools lintas perangkat"
   ```

<a id="32-panduan-cepat-untuk-pengguna-publik-baru-1-menit"></a>
### 📦 3.2 Panduan Cepat untuk Pengguna Publik Baru (1 Menit)

Untuk menggunakan `vibe_tools` di proyek Python baru (`my-awesome-app`):
```powershell
# 1. Masuk ke folder proyek Anda
cd my-awesome-app

# 2. Tambahkan vibe_tools sebagai Git Submodule
git submodule add https://github.com/vibe-ecosystem/vibe-tools.git vibe_tools

# 3. Jalankan setup otomatis satu klik
python vibe_tools/setup_vibe_ecosystem.py
```
Seluruh aturan `.agents`, skills universal, dan mode Zoo Code langsung aktif seketika!

<a id="33-panduan-fork--pull-request-untuk-kontributor-global"></a>
### 🤝 3.3 Panduan Fork & Pull Request untuk Kontributor Global

Bagi pengembang global yang ingin berkontribusi menyempurnakan `vibe_tools`:
1. Klik tombol **Fork** di pojok kanan atas repositori [https://github.com/vibe-ecosystem/vibe-tools](https://github.com/vibe-ecosystem/vibe-tools).
2. Clone fork ke komputer Anda:
   ```bash
   git clone https://github.com/username-anda/vibe-tools.git
   cd vibe-tools
   git checkout -b feat/fitur-baru-keren
   ```
3. Lakukan modifikasi, pastikan kode mematuhi batas `< 250 baris`, lulus verifikasi sintaks:
   ```powershell
   python -m py_compile <file_yang_diubah>
   ```
4. Push dan buat **Pull Request**:
   ```bash
   git add .
   git commit -m "feat: tambahkan fitur xyz"
   git push origin feat/fitur-baru-keren
   ```

---

## 4. REA MCP: Reverse Engineer Anything

REA (*Reverse Engineer Anything*) adalah MCP server berbasis Node.js yang memberikan kemampuan **analisis binary mendalam** (PE, ELF, APK, Mach-O, firmware, dan web bundles).

### ⚡ Instalasi Cepat:
```powershell
# Status saklar MCP (Dual-Cockpit)
python vibe_tools/rea_tool.py --status

# Nonaktifkan REA MCP (DEFAULT - Menghemat ~25.000 token per pesan)
python vibe_tools/rea_tool.py --disable

# Aktifkan hanya saat butuh reverse engineering biner
python vibe_tools/rea_tool.py --enable
```

---

## 5. Hermes Agent x Antigravity IDE x Zoo Code & Self-Learning Universal

<a id="51-sinergi-3-cockpit-antigravity-zoo-code--hermes-agent"></a>
### 🌐 5.1 Sinergi 3 Cockpit: Antigravity, Zoo Code, & Hermes Agent

Ekosistem menggabungkan kekuatan tiga pilar AI:
1. **Antigravity IDE**: Arsitek sistem dengan jendela konteks raksasa (1M–2M token) untuk perencanaan besar, perancangan spesifikasi, dan audit.
2. **VS Code Zoo Code**: Kokpit kerja taktis modular dengan 7 Custom Modes dan dukungan model offline GPU Lokal RTX 3060 ($0).
3. **Hermes Agent**: Background worker mandiri otonom berbasis CLI yang menangani investigasi mendalam dan menyimpan memori jangka panjang.

<a id="52-metode-pemasangan-cepat-mandiri-1-menit"></a>
### 🚀 5.2 Metode Pemasangan Cepat Mandiri (1 Menit)

Jalankan installer otomatis yang telah dirampingkan:
```powershell
python vibe_tools/install_hermes_antigravity.py
```
Skrip akan mengunduh Hermes Agent, memasang dependensi, menyalin bridge `hermes_mcp.py` ke `~/.gemini/`, dan mendaftarkannya ke `mcp_config.json`.

<a id="53-pemasangan-manual-langkah-demi-langkah"></a>
### 🛠️ 5.3 Pemasangan Manual Langkah Demi Langkah
1. Clone repositori: `git clone https://github.com/NousResearch/hermes-agent.git C:/hermes_env/hermes-agent`
2. Install paket: `pip install -e C:/hermes_env/hermes-agent`
3. Atur model default di terminal:
   ```cmd
   hermes config set model "deepseek/deepseek-chat"
   ```
4. Salin `vibe_tools/hermes_mcp.py` ke `%USERPROFILE%/.gemini/hermes_mcp.py`.
5. Daftarkan di `%USERPROFILE%/.gemini/config/mcp_config.json`.

<a id="54-self-learning-universal-lintas-proyek"></a>
### 🧠 5.4 Self-Learning Universal Lintas-Proyek

Hermes Agent memiliki keunggulan **Self-Learning** yang dapat mengingat pelajaran arsitektur dan kesalahan koding secara permanen di `%USERPROFILE%/.hermes/memories/MEMORY.md`.

Setiap kali Anda menyelesaikan sesi diskusi atau refaktor besar, perintahkan AI untuk menyimpannya ke memori universal:

```markdown
Tolong delegasikan ke Hermes Agent:
"Pelajari hasil percakapan dan konsensus arsitektur hari ini. Catat aturan, batasan Ponytail, dan pola terbaik ke memori jangka panjang universal (~/.hermes/memories/MEMORY.md) agar otomatis aktif dan diingat pada seluruh sesi vibe coding di proyek mana pun."
```
Dengan cara ini, ilmu dan best-practice yang dipelajari pada satu proyek otomatis diterapkan di proyek-proyek Anda berikutnya!

---

## 6. Tutorial Setup PC/Laptop Baru dari Nol (Fresh Install Windows 10/11) & OpenRouter MCP

<a id="61-tahap-1-persiapan-dasar-windows-1011-baru"></a>
### 💻 6.1 Tahap 1: Persiapan Dasar Windows 10/11 Baru
1. Pasang **Git for Windows** dari [git-scm.com](https://git-scm.com).
2. Pasang **Python 3.11+** dari [python.org](https://python.org).
   > [!IMPORTANT]
   > Pada layar pertama installer Python, **WAJIB CENTANG kotak "Add python.exe to PATH"**!

<a id="62-tahap-2-persiapan-akun--saldo-ai"></a>
### 💳 6.2 Tahap 2: Persiapan Akun & Saldo AI
1. **Google AI Studio / Gemini Plus / Advanced**: Siapkan akun Google Anda.
2. **OpenRouter**: Daftar di [openrouter.ai](https://openrouter.ai), buat API Key di menu *Keys*, lalu lakukan top-up saldo minimal **\$5.00** (cukup untuk ribuan sesi koding hemat).

<a id="63-tahap-3-instalasi-ide--setting-auto-approve-otonom"></a>
### ⚙️ 6.3 Tahap 3: Instalasi IDE & Setting Auto-Approve Otonom
Agar AI dapat mengeksekusi rangkaian tiket secara mandiri tanpa harus meminta persetujuan manual Enter setiap saat:
* **Antigravity IDE**: Masuk ke Settings / Preferences -> Cari "Terminal Approval" -> Setel ke Auto-Approve untuk sandboxed commands.
* **VS Code Zoo Code**:
  1. Unduh file `.vsix` rilis terbaru dari [Zoo-Code GitHub Releases](https://github.com/Zoo-Code-Org/Zoo-Code/releases).
  2. Buka VS Code -> Extensions (`Ctrl+Shift+X`) -> Klik `...` di kanan atas -> **Install from VSIX...**
  3. Buka tab Zoo Code -> Klik ikon **⚙️ Settings** di kanan atas -> Centang:
     - ✅ **Always approve read-only actions**
     - ✅ **Always approve write actions**
     - ✅ **Always approve execute actions**
     - ✅ **Always approve MCP server actions**

<a id="64-tahap-4-prompt-setup-mandiri--alternatif-manual"></a>
### 🚀 6.4 Tahap 4: Prompt Setup Mandiri & Alternatif Manual

#### Opsi 1: Satu Prompt Otomatis di Chat Antigravity
Salin prompt berikut dan kirim ke chat Antigravity IDE:
```markdown
Halo Antigravity, tolong bantu pasang dan konfigurasikan OpenRouter MCP Server di laptop ini secara global:
1. Pastikan folder ~/.gemini dan ~/.gemini/config/ sudah ada.
2. Pasang dependensi: python -m pip install -q mcp.
3. Salin vibe_tools/openrouter_mcp.py ke ~/.gemini/openrouter_mcp.py.
4. Buat ~/.gemini/openrouter_key.txt dan masukkan OpenRouter API Key saya.
5. Daftarkan server openrouter ke ~/.gemini/config/mcp_config.json.
```

#### Opsi 2: Eksekusi Skrip Mandiri via Terminal
```powershell
python vibe_tools/install_openrouter_mcp.py
```

<a id="65-tahap-5-verifikasi--uji-koneksi"></a>
### 🔍 6.5 Tahap 5: Verifikasi & Uji Koneksi
Ketikkan di chat:
> *"Tolong jalankan tool `cek_koneksi_openrouter` untuk memvalidasi API Key dan saldo OpenRouter saya."*

<a id="66-tahap-6-katalog-model-pilihan--update-otomatis"></a>
### 🏆 6.6 Tahap 6: Katalog Model Pilihan & Update Otomatis

Server MCP OpenRouter mendukung **Sistem Alias Cerdas**:

| Kategori | Alias Cepat | Model ID Terpilih | Biaya per 1M Token |
| :--- | :---: | :--- | :---: |
| 🧠 **Penalaran Super (Reasoning)** | **`r1`** | `deepseek/deepseek-r1-0528` | $0.55 / $2.19 |
| 💻 **Standar Emas Coding** | **`claude`** / **`sonnet`** | `anthropic/claude-sonnet-4.5` | $3.00 / $15.00 |
| ⚡ **Harian Gesit & Super Hemat** | **`deepseek`** / **`v3`** | `deepseek/deepseek-chat` | $0.14 / $0.28 |
| 💻 **Spesialis Coding Cepat** | **`qwen`** / **`qwen-coder`** | `qwen/qwen-2.5-coder-32b-instruct` | $0.07 / $1.00 |
| 🆓 **100% Gratis** | **`free`** | `google/gemma-4-31b-it:free` | $0.00 |

> [!TIP]
> Untuk mengecek daftar model dan harga terbaru langsung dari OpenRouter secara otomatis, ketik:  
> *"Panggil tool `daftar_model_rekomendasi`."*

---

## 7. Katalog 15 Skill Universal & Panduan Penggunaan

Folder `vibe_tools/skills` terhubung secara global ke `~/.gemini/config/skills` melalui Windows NTFS Junction (`sync_universal.py`).

| Perintah | Deskripsi Singkat | Contoh Prompt Universal |
| :--- | :--- | :--- |
| **`/ask-matt`** | Router penunjuk jalan rekayasa perangkat lunak | `"/ask-matt apa langkah terbaik untuk fitur ini?"` |
| **`/grill-me`** | Interview arsitektur interaktif satu per satu | `"/grill-me interogasi rancangan modul data cache"` |
| **`/grill-with-docs`** | Domain glossary & Architectural Decision Records (ADR) | `"/grill-with-docs buat ADR untuk pemilihan database"` |
| **`/to-spec`** | Formalisasi spesifikasi teknis modular (< 300 baris) | `"/to-spec buat spec teknis modul auth"` |
| **`/to-tickets`** | Pemecah spesifikasi jadi tiket terurut | `"/to-tickets pecah spec menjadi tiket terurut"` |
| **`/implement`** | Eksekusi tiket disiplin berurutan | `"/implement kerjakan tiket nomor 1"` |
| **`/tdd`** | Siklus Red-Green-Refactor berbasis pytest | `"/tdd buat fungsi hitung durasi dengan pytest"` |
| **`/diagnosing-bugs`**| Pelacak bug via reproduksi tes gagal terlebih dahulu | `"/diagnosing-bugs telusuri penyebab KeyError di line 40"` |
| **`/code-review`** | Audit kepatuhan 3-sumbu (<300 baris, tiket, & Ponytail) | `"/code-review audit perubahan pada src/app.py"` |
| **`/ponytail`** | Anti-over-engineering 7 tangga & stdlib-first (lite/full/ultra) | `"/ponytail sederhanakan kode agar pakai stdlib Python"` |
| **`/modular-refactor`**| Pemecah script monolitik (>300 baris) tanpa regresi | `"/modular-refactor pecah src/processor.py"` |
| **`/unit-test-generator`**| Generator tes isolasi mock fixtures | `"/unit-test-generator buat tes untuk src/api_client.py"` |
| **`/graphify`** | Peta dependensi kode AST & GraphRAG lokal | `"/graphify petakan dependensi fungsi di folder src"` |
| **`/handoff`** | Kompresi konteks percakapan untuk ganti chat/model | `"/handoff rangkum sesi kerja ini ke dokumen handoff"` |
| **`/retro`** | Retrospeksi & penyempurnaan rules guardrails | `"/retro evaluasi proses pengerjaan fitur tadi"` |

📖 Panduan detail setiap skill tersedia di: [**`vibe_tools/skills/README.md`**](skills/README.md).

---

## 8. Arsitektur Hybrid Dual-Cockpit (Antigravity + VS Code Zoo Code + Ollama RTX 3060)

Arsitektur **Dual-Cockpit** menyinergikan dua lingkungan pengembangan AI secara harmonis:
- **Cockpit 1 (Antigravity IDE)**: Perencanaan arsitektur, wawancara `/grill-me`, `/to-spec`, dan audit skala besar.
- **Cockpit 2 (VS Code Zoo Code)**: Eksekusi tiket tugas modular, tool use granular, dan model lokal Ollama (RTX 3060) untuk penelusuran kode 100% offline ($0).

### 🎭 7 Custom Modes di `.roomodes` / `.zoomodes`:
| Mode ID | Peran Utama | Rekomendasi Profil Model |
| :--- | :--- | :--- |
| `orchestrator` | Pintu masuk utama & pengarah tiket task | `google/gemini-2.0-flash-001` atau `deepseek/deepseek-chat` |
| `local-scout-3b` | Grepping kode cepat offline ($0 GPU) | Ollama `qwen2.5-coder:3b-instruct` |
| `local-scout-7b` | Analisis logika mendalam offline ($0 GPU) | Ollama `qwen2.5-coder:7b-instruct-q4_K_M` |
| `vibe-coder` | Eksekusi koding presisi & modular (<300 baris) | `deepseek/deepseek-chat` atau `google/gemini-2.0-flash-001` |
| `grill-me-spec` | Wawancara arsitektur (terkunci hanya edit `docs/`) | `deepseek/deepseek-r1` |
| `bug-hunter` | Investigasi crash & traceback error | `deepseek/deepseek-r1` |
| `code-reviewer` | Audit 3-sumbu mutu kode & Ponytail | `deepseek/deepseek-chat` |

---

## 9. Otomasi Pemeliharaan, Sinkronisasi Database, & Universal Updater Lintas-Proyek

Ekosistem menyediakan perangkat otomatis untuk sinkronisasi pembaruan, ekstraksi riwayat database percakapan, dan saklar hemat token.

### 🚀 9.1 Universal Updater Lintas-Proyek (`update_ecosystem.py`)
```powershell
# Cek perbedaan berkas tanpa mengubah disk (Dry-Run)
python vibe_tools/update_ecosystem.py --check

# Dorong ekosistem dari master lokal ke proyek lain (< 2 detik, offline)
python vibe_tools/update_ecosystem.py --target "D:/Path/Ke/ProjectLain"

# Pulihkan kondisi ke sebelum update jika diperlukan (Rollback)
python vibe_tools/update_ecosystem.py --rollback
```

### 🧠 9.2 Ekstraksi Riwayat Percakapan Database (`doc_db_extractor.py`)
Mengekstrak intisari percakapan nyata dari database Antigravity IDE (`monitor/monitor_cache.db`):
```powershell
# Ekstrak percakapan 2 hari terakhir (kemarin & hari ini) ke scratch/recent_db_knowledge.md
python vibe_tools/doc_db_extractor.py 2
```

### 🔧 9.3 Saklar Toggle REA MCP (`rea_tool.py`)
```powershell
# Nonaktifkan REA MCP (DEFAULT - Menghemat ~25.000 token per pesan)
python vibe_tools/rea_tool.py --disable

# Aktifkan hanya saat butuh reverse engineering biner
python vibe_tools/rea_tool.py --enable
```
