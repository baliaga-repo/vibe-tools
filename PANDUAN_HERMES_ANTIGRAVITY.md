# ⚡ Panduan Pemasangan Instan: Hermes Agent x Antigravity IDE

Panduan ini digunakan untuk memasang **Hermes Agent** di PC lain yang menggunakan **Antigravity IDE** agar berfungsi sebagai **Background Worker MCP** untuk menghemat kuota token Claude / GPT.

---

## 🚀 Metode 1: Instalasi Otomatis (Direkomendasikan - 1 Menit)

Kami sudah menyediakan skrip installer otomatis: [install_hermes_antigravity.py](file:///d:/mobog/Videos/Youtube%20Download/vibe_tools/install_hermes_antigravity.py).

### Langkah-langkah:
1. Pastikan di PC baru sudah terpasang:
   - **Python 3.10+** (Centang *"Add Python to PATH"* saat instalasi).
   - **Git for Windows**.
2. Salin folder `vibe_tools/` atau file [install_hermes_antigravity.py](file:///d:/mobog/Videos/Youtube%20Download/vibe_tools/install_hermes_antigravity.py) ke PC baru.
3. Buka **Command Prompt (CMD)** atau PowerShell, lalu jalankan:
   ```cmd
   python vibe_tools/install_hermes_antigravity.py
   ```
4. Masukkan:
   - Folder instalasi (Tekan **Enter** untuk default `C:\hermes_env`).
   - **OpenRouter API Key** Anda (format `sk-or-v1-...`).
5. Skrip otomatis memasang:
   - Repository Hermes Agent
   - Dependensi esensial (`ruamel.yaml`, `psutil`, `rich`, dll.)
   - Konfigurasi model default OpenRouter (`deepseek/deepseek-chat`)
   - Bridge MCP Antigravity (`~/.gemini/hermes_mcp.py` & `mcp_config.json`)
6. **Restart Antigravity IDE**. Selesai!

---

## 🛠️ Metode 2: Pemasangan Manual Langkah Demi Langkah

Jika Anda ingin memasangnya secara manual tanpa skrip otomatis, ikuti langkah-langkah berikut:

### 1. Clone & Pasang Hermes Agent
Buka Command Prompt (CMD) atau PowerShell:
```cmd
mkdir C:\hermes_env
cd /d C:\hermes_env
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
pip install -e .
```

> [!IMPORTANT]
> **Khusus Python < 3.14 (misalnya Python 3.11 / 3.12 / 3.13):**
> Pada `pyproject.toml`, paket inti Hermes memiliki pembatas `python_version >= '3.14'`. Akibatnya, `pip install -e .` melewatkan dependensi tersebut sehingga memicu error seperti `ModuleNotFoundError: No module named 'ruamel'` atau `psutil` atau `rich`.
> 
> **Wajib pasang paket dependensi inti secara manual:**
> ```cmd
> pip install ruamel.yaml psutil rich tomli-w fire tenacity jinja2 markdown tzdata prompt_toolkit croniter pathspec snowballstemmer mcp
> ```

---

### 2. Simpan Kunci OpenRouter & Atur Model Default

1. **Simpan Kunci API:**
   Buka atau buat file:
   📁 `%LOCALAPPDATA%\hermes\.env`
   
   Isikan baris berikut:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
   ```

2. **Atur Model Default (Wajib non-interaktif):**
   *Jangan biarkan model default kosong karena akan memicu error `HTTP 400: No models provided` dari OpenRouter.*
   Jalankan perintah ini di CMD / PowerShell:
   ```cmd
   hermes config set model "deepseek/deepseek-chat"
   ```
   *(Pilihan model lain: `anthropic/claude-3.5-sonnet`, `deepseek/deepseek-r1`, atau `meta-llama/llama-3.3-70b-instruct:free`).*

---

### 3. Buat File Bridge MCP Antigravity
Buat file baru di path:
📁 `%USERPROFILE%\.gemini\hermes_mcp.py`

Isikan dengan kode berikut:
```python
r"""
Hermes Agent Worker MCP Server untuk Antigravity IDE.
"""
import sys
import os
import subprocess
from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Hermes-Worker")
HERMES_REPO = r"C:\hermes_env\hermes-agent"

@mcp.tool(
    name="delegasikan_ke_hermes",
    description="Kirim tugas background ke Hermes Agent (file search, execute command, scrape, dll) untuk menghemat token."
)
def delegasikan_ke_hermes(tugas: str, direktori_kerja: str = "", model: str = "") -> str:
    cwd = direktori_kerja if (direktori_kerja and Path(direktori_kerja).exists()) else HERMES_REPO
    cmd = ["hermes", "-z"]
    if model:
        cmd.extend(["-m", model.strip()])
    cmd.append(tugas)
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300
        )
        return res.stdout.strip() or res.stderr.strip() or "Selesai tanpa output teks."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
```

---

### 4. Daftarkan ke `mcp_config.json` Antigravity
Buka atau buat file konfigurasi di:
📁 `%USERPROFILE%\.gemini\config\mcp_config.json`

Tambahkan blok `hermes_agent`:
```json
{
  "mcpServers": {
    "hermes_agent": {
      "command": "python",
      "args": [
        "C:/Users/<Username-Anda>/.gemini/hermes_mcp.py"
      ],
      "disabled": false
    }
  }
}
```

---

## 🩺 Diagnosa & Verifikasi

Untuk memastikan Hermes Agent siap bekerja tanpa kendala:

1. **Jalankan Pengecekan Kesehatan:**
   ```cmd
   hermes doctor
   ```
   Pastikan tanda centang hijau muncul untuk `Python Environment`, `Required Packages`, `OpenRouter API`, dan `Model`.

2. **Uji Perintah Oneshot Cepat:**
   ```cmd
   hermes -z "Jawab hanya 1 kata: 'Hermes Siap'"
   ```
   Jika muncul output `Hermes Siap`, instalasi 100% sempurna!

---

## 🎯 Pola Kerja Utama: Gemini (Context Distiller & Executor) + OpenRouter/Hermes (Deep Reasoning Offload)

Sistem ini menggunakan pembagian peran berdasarkan kekuatan alami masing-masing model untuk menghemat kredit OpenRouter dan memaksimalkan akurasi:

1. **Gemini (Primary Model di Antigravity IDE - Context Distiller & Precision Coder)**:
   - **Tugas Berat Konteks (Context Heavy)**: Memanfaatkan *context window* raksasa Gemini (1M–2M token) untuk membaca log terminal yang panjang, scan banyak file sekaligus, menjalankan CLI/test, dan memahami arsitektur besar.
   - **Distilasi Konteks**: Menyaring ribuan baris kode mentah dan log menjadi ringkasan padat (*dense context*, hanya 50–200 baris esensial).
   - **Eksekutor Koding**: Menerima solusi arsitektur/logika dari model reasoning dan langsung mengeksekusi penulisan kode ke codebase secara presisi.

2. **Deep Reasoning & Thinking Offload (Otomatis & Tanpa Overhead)**:
   - **Pure Reasoning & Architecture via `openrouter:tanya_openrouter`**:
     - Menggunakan `model="claude"` (*Claude 3.7 Sonnet Thinking*) atau `model="r1"` (*DeepSeek-R1*).
     - Otomatis dipanggil untuk bedah logika, algoritma, arsitektur, dan investigasi bug rumit. Respon langsung, instan, dan hemat biaya.
   - **Multi-Step Agentic Tasks via `hermes_agent:delegasikan_ke_hermes`**:
     - Digunakan jika penalaran membutuhkan investigasi bertahap atau simulasi di lingkungan mandiri Hermes.
   - **100% Kredit untuk Reasoning**: Kredit OpenRouter Anda tidak terbuang sia-sia untuk memproses ribuan token input mentah/boilerplate, melainkan murni terpakai untuk *reasoning tokens* (chain-of-thought) tingkat tinggi.

---

## 💬 Format Pola Kerja di Antigravity Chat

Anda cukup berinteraksi santai dengan Gemini di IDE:
> **"Tolong analisa error / bug pada fungsi ini dan perbaiki."**

### Alur Eksekusi Otomatis & Koordinasi Dual-Agent:
1. **Konfirmasi & Transparansi Model**: AI wajib mengonfirmasi model mana yang sedang aktif digunakan (misal: *Model Utama IDE Gemini Flash*, *Hermes Worker*, atau *Claude Sonnet*) sebelum menulis/mengubah kode.
2. **Context Distillation**: Gemini menyaring file luas dan log menjadi ringkasan masalah (~100 baris).
3. **Interactive Model Selector**: Jika tugas bersifat arsitektural/penalaran rumit dan Anda belum menyebut model, AI memanggil `ask_question` untuk menampilkan pop-up estimasi biaya USD & token in/out (`cost_estimator.py`).
4. **Bilingual Bridge (Hemat Token)**: Gemini menerjemahkan prompt ke Bahasa Inggris teknis padat sebelum dilempar ke OpenRouter (menghemat saldo 30%–50%).
5. **Delegasi Sesuai Tugas**:
   - **Tugas Penalaran / Logika**: Dirouting ke `tanya_openrouter` (Claude Sonnet 4.5 / DeepSeek R1).
   - **Tugas Investigasi Otonom / Multi-step CLI**: Didelegasikan ke `hermes_agent` (background worker mandiri).
6. **Eksekusi Presisi**: Gemini menerjemahkan kembali hasil penalaran ke Bahasa Indonesia dan menerapkan perubahan kode secara presisi ke berkas Anda secara gratis ($0.00).

---

## 🎛️ Cara Memilih Model Hermes Sesuka Hati

Anda memiliki dua opsi fleksibel:

### Opsi A: Ganti Default Model Secara Global (Terminal)
Jika Anda ingin Hermes selalu memakai model tertentu setiap kali dipanggil tanpa perlu mengetik nama model di chat:
```cmd
# 1. Pakai model gratis 100%:
hermes config set model "meta-llama/llama-3.3-70b-instruct:free"

# 2. Pakai DeepSeek V3 (Sangat murah, pintar coding):
hermes config set model "deepseek/deepseek-chat"

# 3. Pakai Gemini 2.5 Flash (Sangat cepat, context 1M token):
hermes config set model "google/gemini-2.5-flash"

# Atau pilih interaktif dengan panah keyboard:
hermes model
```

### Opsi B: On-Demand per Instruksi Chat (Tanpa Mengubah Default)
Cukup sebutkan model yang diinginkan dalam prompt chat Antigravity:
* *"Suruh Hermes pakai model `google/gemini-2.5-flash` untuk..."*
* *"Delegasikan ke Hermes pakai model `deepseek/deepseek-chat` untuk..."*
* *"Jalankan tes via Hermes pakai model free..."*

Antigravity akan otomatis mengoper parameter `model="..."` ke tool `delegasikan_ke_hermes`!

---

## 📋 Daftar Model Rekomendasi untuk Hermes Worker

| Model ID | Biaya | Keunggulan Utama |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | **Gratis** ($0) | Cocok untuk search file biasa dan ekstraksi log tanpa biaya sama sekali. |
| `deepseek/deepseek-chat` (DeepSeek-V3) | Sangat Murah ($0.14 / 1M token) | Sangat cerdas dalam bash/python command, scripting, dan koding. |
| `google/gemini-2.5-flash` | Sangat Murah | Kecepatan kilat, context window 1M token (bisa membaca file log raksasa). |
| `qwen/qwen-2.5-coder-32b-instruct` | Murah | Spesialis pemahaman sintaks dan refactoring code. |

