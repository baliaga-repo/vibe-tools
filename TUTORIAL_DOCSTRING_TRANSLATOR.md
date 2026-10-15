# 📖 Panduan Lengkap Penerjemah Docstring Bilingual (Docstring Translator)

Dokumen ini menjelaskan cara penggunaan, konfigurasi API Key, penanganan limit kuota (rate limiting), serta arsitektur auto-fallback pada modul `docstring_translator.py`.

---

## 🎯 1. Latar Belakang & Tujuan

Saat mengembangkan proyek open-source atau berkolaborasi secara tim:
* **Pengembang Lokal (Indonesia)**: Lebih nyaman menulis penjelasan alur fungsi dan logika menggunakan Bahasa Indonesia (`[ID]`).
* **Kontributor Internasional & AI Coding**: Memerlukan padanan Bahasa Inggris (`[EN]`) agar model reasoning (seperti Claude, GPT-4, DeepSeek) atau kontributor luar negeri dapat memahami basis kode dengan akurat.

Modul `docstring_translator.py` membaca berkas Python secara otomatis menggunakan **Python AST (Abstract Syntax Tree)**. Script ini:
1. Mendeteksi docstring modul, kelas, fungsi, dan async function.
2. Memeriksa apakah docstring sudah memiliki format dwibahasa `[EN]`.
3. Menerjemahkan deskripsi Bahasa Indonesia ke Bahasa Inggris teknis yang ringkas dan profesional.
4. Memperbarui docstring menjadi dwibahasa tanpa mengubah satu barispun logika, indentasi, atau format kode asli.

---

## 📦 2. Prasyarat & Instalasi

Script ini hanya memerlukan pustaka HTTP bawaan `requests`:

```powershell
pip install requests
```

---

## 🔑 3. Konfigurasi API Key

Script mendukung dua engine AI sekaligus dan membaca kunci secara otomatis tanpa perlu konfigurasi manual setiap kali dijalankan:

| Engine | Sumber Kunci Lokal | Variabel Lingkungan (Env) | Kelebihan |
| :--- | :--- | :--- | :--- |
| **Google Gemini** | `~/.gemini/gemini_key.txt` | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | **100% Gratis** via Google AI Studio. |
| **OpenRouter** | `~/.gemini/openrouter_key.txt` | `OPENROUTER_API_KEY` | **Sangat Cepat**, tidak ada limit 15 RPM, biaya ultra-hemat (~Rp 0.3 per docstring via DeepSeek Chat). |

> [!TIP]
> Anda dapat menyimpan kedua kunci tersebut sekaligus di folder pengguna `~/.gemini/`. Script akan otomatis mendeteksi ketersediaan keduanya.

---

## 🚀 4. Cara Penggunaan & Perintah CLI

### A. Mode Auto-Fallback (Direkomendasikan)
Menjalankan sinkronisasi dengan mencoba **Gemini gratis terlebih dahulu**. Jika kuota Gemini habis (HTTP 429) atau server Google sibuk (HTTP 503), script **otomatis beralih ke OpenRouter di tengah jalan**:

```powershell
# Memproses seluruh folder vibe_tools
python vibe_tools/docstring_translator.py vibe_tools/

# Memproses seluruh proyek saat ini
python vibe_tools/docstring_translator.py .

# Memproses satu berkas spesifik
python vibe_tools/docstring_translator.py vibe_tools/push_to_github.py
```

---

### B. Mode Paksa OpenRouter (Bebas Hambatan Kuota)
Jika Anda memiliki banyak berkas atau docstring panjang dan ingin proses selesai super cepat tanpa terkena jeda kuota:

```powershell
python vibe_tools/docstring_translator.py --engine openrouter vibe_tools/
```

---

### C. Mode Paksa Gemini (100% Gratis)
Jika Anda hanya ingin memanfaatkan kuota gratis Google AI Studio:

```powershell
python vibe_tools/docstring_translator.py --engine gemini vibe_tools/
```

---

### D. Mode Dry-Run (Pratinjau Tanpa Mengubah Berkas Fisik)
Gunakan flag `--dry-run` untuk melihat berapa banyak docstring yang perlu disinkronkan tanpa menyentuh isi file:

```powershell
python vibe_tools/docstring_translator.py --dry-run vibe_tools/
```

---

### E. Mengatur Jeda Panggilan (Throttling Delay)
Secara default, saat menggunakan Gemini, script memberi jeda `2.0` detik antar docstring agar tidak melampaui batas 15 RPM. Anda dapat menyesuaikannya:

```powershell
python vibe_tools/docstring_translator.py --delay 3.0 vibe_tools/
```

---

## 🛡️ 5. Penanganan Error & Mekanisme Pengamanan

### 1. Error HTTP 503 (High Demand / Overload)
* **Penyebab**: Server Google AI Studio sedang mengalami lonjakan beban pengguna.
* **Solusi Otomatis**: Script akan mendeteksi status 503 dan langsung mengalihkan terjemahan ke OpenRouter secara instan.

### 2. Error HTTP 429 (Quota Exceeded / Rate Limit 15 RPM)
* **Penyebab**: Kuota gratis Gemini membatasi maksimal 15 panggilan per menit (Requests Per Minute). Menerjemahkan berkas dengan banyak fungsi berturut-turut tanpa jeda akan memicu limit ini.
* **Solusi Otomatis**: 
  - Script menyisipkan jeda aman (`--delay 2.0`).
  - Jika 429 tetap muncul, fitur auto-fallback langsung memindahkan sisa antrean ke OpenRouter sehingga eksekusi tidak macet.

### 3. Apa yang Terjadi Jika Dibatalkan (`Ctrl + C`)?
* **Mekanisme Auto-Save Parsial**:
  Jika Anda membatalkan eksekusi di tengah-tengah proses menggunakan `Ctrl + C`, script memiliki penangkap sinyal `KeyboardInterrupt`.
  Docstring yang **sudah sempat berhasil diterjemahkan akan langsung disimpan secara aman ke berkas fisik** sebelum program benar-benar berhenti. Anda tidak perlu khawatir kehilangan progres yang sudah dicapai!

---

## 🤖 6. Otomasi Otomatis via GitHub Actions

Untuk menjaga agar repositori publik Anda selalu memiliki docstring bilingual setiap kali ada commit/push baru, alur kerja GitHub Actions telah disediakan di:
`.github/workflows/bilingual_sync.yml`

### Langkah Aktivasi di GitHub:
1. Buka Repositori GitHub Anda.
2. Buka menu **Settings** > **Secrets and variables** > **Actions**.
3. Buat New repository secret:
   * **Name**: `GEMINI_API_KEY`
   * **Secret**: Kunci API dari Google AI Studio Anda.
4. Selesai! Setiap kali Anda melakukan `git push` berkas `.py`, GitHub Actions akan otomatis menerjemahkan docstring baru dan melakukan commit balik ke branch Anda dengan pesan `[skip ci]`.
