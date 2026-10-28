# 🦓 Panduan Lengkap & Tutorial Setup: Zoo Code Hybrid Dual-Cockpit

Panduan komprehensif pemasangan, konfigurasi, pemecahan masalah (*troubleshooting*), dan pengoperasian **Zoo Code** (penerus resmi aktif dari **Roo Code**) yang terintegrasi secara harmonis dengan **Antigravity IDE** dan **Ollama RTX 3060**.

---

## 🧭 Daftar Isi
1. [🌟 Mengapa Beralih dari Roo Code ke Zoo Code?](#-mengapa-beralih-dari-roo-code-ke-zoo-code)
2. [🛠️ Tutorial Pemasangan Anti-Gagal (Berdasarkan Solusi Kasus Nyata)](#️-tutorial-pemasangan-anti-gagal-berdasarkan-solusi-kasus-nyata)
3. [🎯 Langkah Awal: Membuka Panel & Wizard Pertama Kali](#-langkah-awal-membuka-panel--wizard-pertama-kali)
4. [⚙️ Cara Mengganti Model & Pengaturan API](#️-cara-mengganti-model--pengaturan-api)
5. [🎭 7 Custom Modes di Ekosistem Dual-Cockpit](#-7-custom-modes-di-ekosistem-dual-cockpit)
6. [💰 Rekomendasi Model Paling Irit Kuota & Biaya](#-rekomendasi-model-paling-irit-kuota--biaya)
7. [⌨️ Cheat-Sheet Shortcut Chat (Slash Commands)](#️-cheat-sheet-shortcut-chat-slash-commands)
8. [🛡️ Rambu Keamanan Token & Proteksi Berkas Proyek](#️-rambu-keamanan-token--proteksi-berkas-proyek)

---

## 🌟 Mengapa Beralih dari Roo Code ke Zoo Code?

Repositori resmi **Roo Code** telah diarsipkan (*read-only*) oleh tim pembuat aslinya. Komunitas pengembang dan kontributor utamanya melanjutkan pengembangan aktif melalui **Zoo Code** ([Zoo-Code-Org/Zoo-Code](https://github.com/Zoo-Code-Org/Zoo-Code)).

**Kabar Baik untuk Proyek Kita:**
Zoo Code dirancang dengan **100% Backward Compatibility**:
- File konfigurasi [`.roomodes`](file:///d:/mobog/Videos/Youtube%20Download/.roomodes) dan [`.zoomodes`](file:///d:/mobog/Videos/Youtube%20Download/.zoomodes) langsung dikenali secara otomatis.
- Folder aturan [`.roo/`](file:///d:/mobog/Videos/Youtube%20Download/.roo) dan [`.zoo/`](file:///d:/mobog/Videos/Youtube%20Download/.zoo) (termasuk MCP dan commands) bekerja mulus tanpa perlu migrasi manual.

---

## 🛠️ Tutorial Pemasangan Anti-Gagal (Berdasarkan Solusi Kasus Nyata)

### ⚠️ Masalah Umum: Error `Failed to fetch` di Marketplace VS Code
Saat mencoba menginstall Zoo Code atau Roo Code langsung dari tab Extensions VS Code, sering muncul pesan error:
```text
[Network] ... gallerycdn.vsassets.io/... - error GET Failed to fetch
TypeError: Failed to fetch
```
**Penyebab:** DNS ISP (seperti Indihome/Telkom/FirstMedia) sering memblokir atau mengalami *timeout* saat mengunduh paket dari CDN Microsoft Marketplace.

### ✅ Solusi Pasti: Pasang Manual via File `.vsix` dari GitHub Releases
1. Buka browser Anda dan kunjungi halaman rilis resmi:  
   🔗 **[GitHub Releases Zoo Code](https://github.com/Zoo-Code-Org/Zoo-Code/releases)**
2. Pada rilis terbaru (misal `v3.92.0`), klik bagian **Assets** dan unduh file:  
   📄 **`zoo-code-3.92.0.vsix`**
3. Buka **VS Code**.
4. Masuk ke menu **Extensions** (`Ctrl + Shift + X`).
5. Klik ikon **titik tiga (`...`)** di pojok kanan atas bilah Extensions.
6. Pilih **"Install from VSIX..."** (*Pasang dari VSIX...*).
7. Pilih file `zoo-code-*.vsix` yang baru Anda unduh. Instalasi akan selesai dalam 2 detik!

---

## 🎯 Langkah Awal: Membuka Panel & Wizard Pertama Kali

### ⚠️ Jangan Tertukar dengan Chat Bawaan IDE!
Pada layar VS Code Anda:
- Panel chat di sebelah kanan atas bertuliskan `CHAT / SESSIONS` adalah **Chat Bawaan Antigravity / Copilot**, bukan Zoo Code.

### Cara Membuka Zoo Code yang Benar:
- **Cara 1 (Paling Cepat):** Tekan `Ctrl + Shift + P` di keyboard, ketik:
  ```text
  Zoo Code: Open In New Tab
  ```
  lalu tekan **Enter**.
- **Cara 2 (Lewat Bilah Samping):** Lihat bilah paling kiri (**Activity Bar**), klik **Ikon Kepala Zebra 🦓**.

### Menyelesaikan Wizard Awal (*Choose your provider*):
Ketika panel Zoo Code pertama kali terbuka, Anda akan melihat halaman selamat datang:
1. **API Provider:** Pilih `OpenRouter`.
2. **OpenRouter API Key:** Biasanya otomatis terisi dari konfigurasi IDE, atau tempelkan key Anda dari `~/.gemini/openrouter_key.txt`.
3. **Model:** Default `anthropic/claude-sonnet-4.5` (bisa diubah nanti).
4. Klik tombol biru **`Finish →`** di bagian bawah. Selesai!

---

## ⚙️ Cara Mengganti Model & Pengaturan API

Ada **2 cara cepat** untuk mengganti model di Zoo Code:

### 1. Cara 1 Klik (Paling Cepat di Bawah Chat)
Tepat di bawah kotak tempat Anda mengetik (*"Type your task here..."*), ada tombol pill nama model (misal `nvidia/nemotron...` atau `anthropic/claude...`).
👉 **Klik langsung tombol nama model tersebut**, lalu pilih model hemat yang Anda inginkan dari dropdown!

### 2. Cara Ikon Gerigi (⚙️ Settings)
Di **pojok kanan atas tab Zoo Code** (di baris tab atas), ada **Ikon Gerigi (⚙️ Settings)**. Klik ikon tersebut untuk membuka pengaturan penyedia API, API Key, dan model secara penuh.

---

## 🎭 7 Custom Modes di Ekosistem Dual-Cockpit

Di bagian bawah chat, klik dropdown mode untuk memilih peran AI:

| Nama Mode | Ikon | Peran & Tugas Utama | Rekomendasi Model |
| :--- | :---: | :--- | :--- |
| **`Orchestrator (Selector)`** | 🪃 | **Pintu masuk utama (Default).** Memetakan arsitektur, merutekan tugas, dan menanyakan metode eksekusi terbaik. | `google/gemini-2.0-flash-001` atau `deepseek/deepseek-chat` |
| **`Local Scout 3B (Fast $0)`** | 🏎️ | Pekerja kasar cepat offline di GPU RTX 3060 ($0). Menemukan letak file dan baris kode. | Ollama `qwen2.5-coder:3b-instruct` |
| **`Local Scout 7B (Deep $0)`** | 🚜 | Analisis alur logika mendalam & relasi file offline ($0). | Ollama `qwen2.5-coder:7b-instruct-q4_K_M` |
| **`Vibe Coder (Cloud Exec)`** | 💻 | Eksekusi koding presisi, bersih, modular (<300 baris), dan auto-verifikasi sintaks `py_compile`. | `deepseek/deepseek-chat` atau `google/gemini-2.0-flash-001` |
| **`Grill-Me & Spec (Architect)`** | 🔥 | Wawancara arsitektur fitur baru. **Terkunci hanya boleh mengedit berkas di dalam `docs/`**. | `deepseek/deepseek-r1` |
| **`Bug Hunter (Diagnose)`** | 🔍 | Investigasi akar masalah crash dan error log secara ilmiah sebelum perbaikan. | `deepseek/deepseek-r1` |
| **`Code Reviewer (Audit)`** | 🛡️ | Audit modularitas kode, type hinting, dan docstring Bahasa Indonesia tanpa mengubah kode. | `deepseek/deepseek-chat` |

---

## 💰 Rekomendasi Model Paling Irit Kuota & Biaya

| Peringkat | Model ID | Tipe | Biaya per 1 Juta Token | Keunggulan Utama |
| :---: | :--- | :---: | :---: | :--- |
| 🥇 | **Ollama Local (3B / 7B)** | Lokal GPU | **$0.00 (Gratis)** | 100% offline di RTX 3060 Anda, tanpa kuota/internet. |
| 🥈 | **`google/gemini-2.0-flash-001`** | Cloud | **~$0.10** (~Rp 1.500) | Sangat cepat, membaca file besar dengan biaya termurah. |
| 🥉 | **`deepseek/deepseek-chat` (V3)** | Cloud | **~$0.14** (~Rp 2.200) | Kualitas koding setara GPT-4/Claude dengan harga sangat murah. |
| 🧠 | **`deepseek/deepseek-r1`** | Cloud (Reasoning) | **~$0.55** (~Rp 8.500) | Penalaran logika arsitektur mendalam (6x lebih murah dari Claude). |

---

## ⌨️ Cheat-Sheet Shortcut Chat (Slash Commands)

Ketik perintah shortcut ini di awal prompt untuk menghemat waktu:

### 1. Navigasi Metode Eksekusi:
- **/pakai-rag**   : Gunakan context codebase standar.
- **/pakai-3b**    : Cari lokasi fungsi pakai model lokal 3B di GPU ($0).
- **/pakai-7b**    : Analisis alur kode pakai model lokal 7B di GPU ($0).
- **/adu-metode**  : Bandingkan hasil penelusuran model lokal vs cloud.

### 2. Siklus Pembangunan Fitur Baru:
```text
/grill-me  ──>  /to-spec  ──>  /to-tickets  ──>  /implement
```
- **/grill-me** : Wawancara interaktif pertanyaan-demi-pertanyaan sebelum menulis kode.
- **/to-spec** : Menyusun dokumen spesifikasi formal ke `docs/specs/`.
- **/to-tickets**: Memecah spesifikasi menjadi tiket modular terurut di `docs/tickets/`.
- **/implement**: Mengeksekusi tiket secara mandiri dan disiplin.

---

## 🛡️ Rambu Keamanan Token & Proteksi Berkas Proyek

1. **Aturan Khusus Proyek Anda 100% Aman:**  
   Tambahkan aturan unik proyek di [`.zoo/rules/99-project-custom.md`](file:///d:/mobog/Videos/Youtube%20Download/.zoo/rules/99-project-custom.md) (atau `.roo/`). Berkas ini memiliki proteksi ketat dan tidak akan pernah tertimpa saat update ekosistem.
2. **Matikan REA MCP Saat Tidak Digunakan:**  
   Server REA menyedot ~25.000 token per pesan. Pastikan selalu nonaktif via terminal:
   ```powershell
   python vibe_tools/rea_tool.py --status   # Cek kondisi
   python vibe_tools/rea_tool.py --disable  # Matikan (Hemat ~25K token)
   ```
3. **Pembaruan Lintas-Proyek Otomatis:**  
   Jika ada rilis baru, cukup jalankan updater universal:
   ```powershell
   python vibe_tools/update_ecosystem.py --check
   python vibe_tools/update_ecosystem.py
   ```

