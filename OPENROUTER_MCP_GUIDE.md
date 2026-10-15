# 🧭 Panduan Lengkap OpenRouter MCP & Katalog Model AI

Dokumen ini berisi panduan komprehensif integrasi **OpenRouter MCP Server** di Antigravity IDE, mulai dari **prompt pemasangan mandiri di laptop/PC baru**, langkah instalasi manual, panduan penggunaan alias cerdas, hingga katalog lengkap model AI terbaik untuk *vibe coding*.

---

## 📋 Daftar Isi
1. [🚀 Pemasangan Cepat Mandiri di Laptop Baru (Prompt Siap Pakai)](#-pemasangan-cepat-mandiri-di-laptop-baru-prompt-siap-pakai)
2. [🛠️ Panduan Pemasangan Manual (Metode Alternatif)](#️-panduan-pemasangan-manual-metode-alternatif)
3. [🔍 Cara Verifikasi & Uji Koneksi](#-cara-verifikasi--uji-koneksi)
4. [🏆 Katalog Model Pilihan Berdasarkan Kategori](#-katalog-model-pilihan-berdasarkan-kategori)
5. [💡 Contoh Cara Meminta di Chat Antigravity](#-contoh-cara-meminta-di-chat-antigravity)
6. [📊 Predictive Token Budgeting & Pemilih Model Cerdas (cost_estimator.py)](#-predictive-token-budgeting--pemilih-model-cerdas-cost_estimatorpy)
7. [🌐 Bilingual Token Optimization (English Bridge Pipeline)](#-bilingual-token-optimization-english-bridge-pipeline)
8. [⚙️ Lokasi Berkas & Troubleshooting](#️-lokasi-berkas--troubleshooting)

---

## 🚀 Pemasangan Cepat Mandiri di Laptop Baru (Prompt Siap Pakai)

Ketika Anda membuka Antigravity IDE di laptop atau perangkat baru, Anda **tidak perlu mengonfigurasi satu per satu secara manual**. Cukup salin teks prompt di bawah ini, lalu tempelkan (*paste*) langsung ke chat Antigravity IDE di laptop Anda:

```markdown
Halo Antigravity, tolong bantu pasang dan konfigurasikan OpenRouter MCP Server di laptop ini secara global:

1. Buat folder konfigurasi jika belum ada:
   - Folder konfigurasi global: ~/.gemini/config/
   - Folder skrip MCP: ~/.gemini/

2. Instal dependensi Python yang dibutuhkan:
   - Jalankan terminal: python -m pip install mcp requests

3. Siapkan skrip MCP Server (~/.gemini/openrouter_mcp.py):
   - Jika di workspace saat ini ada file `openrouter_mcp.py`, salin ke ~/.gemini/openrouter_mcp.py.
   - Jika tidak ada, buatkan skrip MCP Server OpenRouter berbasis FastMCP/MCPServer dengan 3 tool utama:
     a. `tanya_openrouter(prompt, model, system_prompt)` dengan alias cerdas (r1, claude, sonnet, deepseek, v3, gpt4o, qwen, free, dll).
     b. `daftar_model_rekomendasi()` untuk menampilkan daftar model unggulan.
     c. `cek_koneksi_openrouter()` untuk mengecek validitas API Key dan saldo/limit.

4. Siapkan berkas API Key:
   - Buat file ~/.gemini/openrouter_key.txt (jika belum ada).
   - Minta saya memasukkan API Key OpenRouter jika file masih kosong.

5. Konfigurasikan ~/.gemini/config/mcp_config.json:
   - Tambahkan server "openrouter" dengan executable python, path absolut ke openrouter_mcp.py laptop ini, dan env OPENROUTER_API_KEY.

6. Uji skrip dengan menjalankan `python ~/.gemini/openrouter_mcp.py --help` atau cek impor Python untuk memastikan tidak ada error sintaks.
```

> [!TIP]
> Antigravity di laptop Anda akan otomatis mendeteksi path username lokal laptop Anda (misalnya `C:/Users/NamaUser/.gemini/...`), menginstal pustaka yang dibutuhkan, dan menyusun `mcp_config.json` dengan path absolut yang tepat.

---

## 🛠️ Panduan Pemasangan Manual (Metode Alternatif)

Jika Anda ingin melakukan pemasangan secara manual tanpa prompt otomatis, ikuti 4 langkah mudah berikut:

### Langkah 1: Instal Dependensi Python
Buka PowerShell / Terminal di laptop Anda, lalu jalankan:
```powershell
python -m pip install mcp requests
```

### Langkah 2: Tempatkan Skrip `openrouter_mcp.py`
Salin file [openrouter_mcp.py](file:///c:/Users/BaliAga/.gemini/openrouter_mcp.py) ke direktori pengguna laptop Anda:
- Lokasi target: `C:\Users\<Username_Laptop>\.gemini\openrouter_mcp.py`

### Langkah 3: Buat Berkas API Key
Buat file teks bernama `openrouter_key.txt` pada folder yang sama:
- Lokasi: `C:\Users\<Username_Laptop>\.gemini\openrouter_key.txt`
- Isi: Tempelkan API Key OpenRouter Anda (misal `sk-or-v1-xxxxxxxx...`) langsung tanpa spasi atau baris baru berlebih.

### Langkah 4: Daftarkan di `mcp_config.json`
Buka atau buat berkas konfigurasi MCP global Antigravity di:
- Lokasi: `C:\Users\<Username_Laptop>\.gemini\config\mcp_config.json`

Isi konfigurasinya sebagai berikut (ganti `<Username_Laptop>` sesuai folder pengguna Anda):
```json
{
  "mcpServers": {
    "openrouter": {
      "command": "python",
      "args": [
        "C:/Users/<Username_Laptop>/.gemini/openrouter_mcp.py"
      ],
      "env": {
        "OPENROUTER_API_KEY": "TEMPEL_API_KEY_DISINI"
      }
    }
  }
}
```

> [!NOTE]
> Gunakan garis miring kanan (`/`) pada path berkas di file JSON konfigurasi untuk menghindari error *escape character* Windows.

---

## 🔍 Cara Verifikasi & Uji Koneksi

Setelah pemasangan selesai (baik via prompt maupun manual):
1. Mulai sesi percakapan baru di Antigravity IDE (atau *restart* Antigravity IDE).
2. Periksa apakah tool `openrouter` terdaftar di bawah menu **MCP Servers** di IDE.
3. Ketikkan prompt uji coba di chat:
   > *"Tolong jalankan tool `cek_koneksi_openrouter` untuk memastikan API key dan saldo OpenRouter saya sudah aktif."*
4. Jika koneksi sukses, Antigravity akan menampilkan status saldo, label akun, dan batas pemakaian Anda.

---

## 🏆 Katalog Model Pilihan Berdasarkan Kategori

Server MCP OpenRouter telah dilengkapi dengan **Sistem Alias Cerdas**. Anda **tidak perlu** mengetik ID model yang panjang; cukup sebutkan **Nama Panggilan (Alias)** dalam prompt Anda!

| Kategori & Kegunaan | Nama Panggilan (Alias) | Model ID Lengkap | Biaya per 1 Juta Token (Input / Output) | Kapan Harus Digunakan? |
| :--- | :---: | :--- | :---: | :--- |
| 🧠 **Penalaran Super (Reasoning)** | **`r1`** | `deepseek/deepseek-r1` | $0.55 / $2.19 | Algoritma matematika, logika regex rumit, pelacakan bug misterius, pemikiran mendalam (CoT). |
| 🧠 **Penalaran Cepat** | **`o3-mini`** | `openai/o3-mini` | $1.10 / $4.40 | Masalah sains/coding yang butuh penalaran logis ala OpenAI. |
| 💻 **Standar Emas Coding** | **`claude`** atau **`sonnet`** | `anthropic/claude-sonnet-4.5` | $3.00 / $15.00 | Refactoring arsitektur besar, pembuatan kode modular bersih, zero halusinasi sintaks. |
| 💻 **Spesialis Coding Super Cepat** | **`qwen`**, **`qwen-coder`**, **`qwen-2.5-coder`** | `qwen/qwen-2.5-coder-32b-instruct` | **$0.07 / $1.00** | Model spesialis coding terbaik di kelasnya: super murah, kilat, dan akurat untuk Python, JS, Regex. |
| 💻 **Spesialis Autocomplete & Patching** | **`codestral`** | `mistralai/codestral-2501` | $0.30 / $0.90 | Fitur FIM (Fill-in-the-Middle) untuk melengkapi potongan fungsi kode dan modifikasi baris. |
| ⚡ **Harian Gesit & Super Hemat** | **`deepseek`** atau **`v3`** | `deepseek/deepseek-chat` | **$0.14 / $0.28** | Pekerjaan harian serbaguna, pembuatan skrip cepat, penjelasan kode, penulisan docstring. |
| ⚡ **Multifungsi Cepat** | **`gpt4o`** atau **`4o`** | `openai/gpt-4o` | $2.50 / $10.00 | Ringkasan dokumen, analisis multi-bahasa, instruksi umum. |
| ⚡ **Latensi Kilat & Konteks Raksasa** | **`gemini-flash`** | `google/gemini-2.0-flash-001` | $0.10 / $0.40 | Respon super cepat dalam hitungan milidetik dengan kapasitas context window 1M token. |

---

## 💡 Contoh Cara Meminta di Chat Antigravity

Anda cukup berbicara seperti biasa dengan menyebutkan alias modelnya:

1. **Meminta Bantuan DeepSeek R1 untuk Logika Berat:**
   > *"Antigravity, tolong buatkan algoritma filtering data ini. Gunakan model `r1` untuk merancang logikanya, lalu implementasikan ke kodenya."*

2. **Meminta Refactoring Presisi ke Claude Sonnet 4.5:**
   > *"Tolong tanyakan ke `claude` bagaimana cara memecah fungsi monolitik ini menjadi sub-fungsi yang rapi dan modular."*

3. **Menggunakan Model Harian Termurah (DeepSeek V3):**
   > *"Jelaskan alur data ini menggunakan model `deepseek`."*

4. **Mode Hemat Tanpa Potong Saldo (Gratis):**
   > *"Bantu review kode ini menggunakan model `free`."*

5. **Melihat Katalog Langsung dari Chat:**
   > *"Tolong panggil `daftar_model_rekomendasi` untuk melihat opsi model saat ini."*

---

## 📊 Predictive Token Budgeting & Pemilih Model Cerdas (`cost_estimator.py`)

Untuk mencegah pembengkakan saldo OpenRouter tanpa sengaja, ekosistem menyertakan modul mandiri [cost_estimator.py](file:///d:/mobog/Videos/Youtube%20Download/vibe_tools/cost_estimator.py):

### 1. Bagaimana Cara Kerjanya?
- **Heuristic Token Estimator**: Menghitung estimasi token input (~3.5 karakter per token) dan output berdasarkan tingkat kerumitan tugas.
- **Tabel Tarif Resmi**: Mengalikan token dengan harga resmi OpenRouter per 1M token untuk setiap model (`r1`, `claude`, `v3`, `free`).
- **Interactive Modal Pop-up (`ask_question`)**:
  Jika Anda meminta tugas arsitektur/penalaran rumit dan **lupa menyebutkan model**, Antigravity IDE otomatis menampilkan modal dialog radio button berisi daftar model, estimasi token in/out, serta estimasi biaya dalam USD (misal: `~$0.003` untuk R1 atau `~$0.020` untuk Claude Sonnet).

---

## 🌐 Bilingual Token Optimization (English Bridge Pipeline)

### Mengapa Perlu Jembatan Bahasa?
Tokenizer BPE (Byte-Pair Encoding) pada Claude dan model LLM frontier lainnya dilatih mayoritas dengan korpus Bahasa Inggris. 
- **Bahasa Inggris**: Rata-rata **~1.3 token per kata**.
- **Bahasa Indonesia**: Rata-rata **~2.2 s/d 2.8 token per kata** (akibat *subword fragmentation* suku kata).

Untuk teks panjang, Bahasa Indonesia dapat memakan **40% – 50% lebih banyak token** dan biaya saldo OpenRouter.

### Solusi Otomatis (Zero-Cost Translation Bridge):
1. **Input**: Anda tetap bertanya santai dalam **Bahasa Indonesia**.
2. **Translate & Compress**: Gemini IDE (Gratis, $0.00) merangkum konteks ke dalam Bahasa Inggris teknis padat di balik layar.
3. **Reasoning**: OpenRouter (Claude Sonnet / DeepSeek-R1) mengeksekusi logika dalam Bahasa Inggris (menghemat saldo 30%–50%).
4. **Output**: Gemini IDE menerjemahkan dan menyajikan solusinya kembali kepada Anda dalam Bahasa Indonesia yang rapi tanpa biaya token tambahan!

---

## ⚙️ Lokasi Berkas & Troubleshooting

### Lokasi Standar Berkas:
- **Skrip Jembatan MCP:** `~/.gemini/openrouter_mcp.py`
- **Penyimpanan API Key:** `~/.gemini/openrouter_key.txt`
- **Konfigurasi MCP Global:** `~/.gemini/config/mcp_config.json`

### Kendala Umum & Solusi:
1. **Error `python: command not found`:**
   Pastikan Python sudah dicentang *"Add python.exe to PATH"* saat instalasi di laptop. Jika menggunakan Python environment tertentu (seperti Anaconda/venv), masukkan path absolut `python.exe` ke field `"command"` di `mcp_config.json`.
2. **Karakter encoding di Windows:**
   Skrip `openrouter_mcp.py` sudah dilengkapi konfigurasi otomatis UTF-8 untuk stdout dan stderr agar aman dari error encoding terminal Windows.
3. **Penyimpanan Saldo & Keamanan Key:**
   Simpan API Key di file lokal `openrouter_key.txt` (termasuk di `.gitignore`), bukan di-hardcode ke repositori publik.
