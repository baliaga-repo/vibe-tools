# 🔍 Panduan REA MCP: Reverse Engineer Anything di Antigravity IDE

REA (*Reverse Engineer Anything*) adalah MCP server berbasis Node.js yang memberikan kemampuan **reverse engineering mendalam** kepada AI Agent. Dibangun oleh [morluto/rea](https://github.com/morluto/rea) dan tersedia di npm sebagai `rea-agents`.

Dengan REA aktif di Antigravity IDE, Anda dapat meminta AI untuk:
- Membedah fitur aplikasi **tanpa source code** (hanya dari binary/ASAR/APK).
- Menganalisis bundle JavaScript/Electron yang dikompilasi (*minified*/*obfuscated*).
- Menginspeksi lalu lintas jaringan tersimpan (HAR, mitmproxy, Fiddler).
- Mendekompilasi file biner native (`.exe`, `.dll`, ELF, Mach-O) via Ghidra/Hopper/IDA.
- Membongkar APK Android, IPA iOS, atau paket HarmonyOS HAP.

---

## ⚡ Instalasi Cepat

```bash
python vibe_tools/install_rea_mcp.py
```

Setelah selesai, **restart Antigravity IDE sekali**. REA langsung aktif dengan 207 tools reverse engineering.

---

## 🧭 Kapan Menggunakan REA?

| Situasi | Gunakan REA? |
| :--- | :---: |
| Analisis **source code repository biasa** (ada `.py`, `.js`, `.ts`) | ❌ Tidak perlu |
| Membedah file **ASAR, APK, IPA, .exe, .dll** tanpa source code | ✅ Ya |
| Menganalisis **bundle JavaScript terkompilasi** (webpack, rollup, vite) | ✅ Ya |
| Menginspeksi **lalu lintas HTTP** yang direkam (HAR, mitmproxy) | ✅ Ya |
| Meniru fitur dari aplikasi lain ke proyek Anda | ✅ Ya |
| Mengaudit aplikasi untuk tracker/telemetri tersembunyi | ✅ Ya |
| Membandingkan dua versi aplikasi untuk melihat perubahan | ✅ Ya |

---

## 🚀 Panduan Penggunaan

### 1. Analisis Aplikasi Electron/ASAR (Paling Umum & Tanpa Decompiler)

**Via Terminal (tanpa konfigurasi MCP):**
```bash
npx -y rea-agents@latest analyze-javascript-application /path/absolut/ke/app
```

**Template Prompt di Antigravity IDE:**
```text
Gunakan REA untuk menganalisis aplikasi Electron di folder:
D:/apps/NamaAplikasi
Saya ingin memahami bagaimana fitur [nama fitur] bekerja secara internal.
Tampilkan temuan beserta buktinya dan pisahkan antara observasi vs inferensi.
```

---

### 2. Analisis Web Bundle / Webpack

**Template Prompt:**
```text
Gunakan REA untuk menganalisis bundle JavaScript dari halaman:
https://example.com
Target: halaman [nama halaman], endpoint: [URL endpoint jika diketahui]
Saya ingin mengetahui struktur modul, import, dan dependensinya.
```

---

### 3. Analisis APK Android

**Template Prompt:**
```text
Gunakan REA untuk menginspeksi APK Android:
/path/ke/aplikasi.apk
Cari class yang mengandung logika [autentikasi / enkripsi / tracking].
Tampilkan referensi masuk dan keluar untuk class yang relevan.
```

---

### 4. Membandingkan Dua Versi Aplikasi

**Template Prompt:**
```text
Gunakan REA untuk membandingkan dua versi bundle JavaScript:
- Versi lama: /path/ke/app_v1/
- Versi baru: /path/ke/app_v2/
Tunjukkan perubahan fitur, modul baru yang ditambahkan, dan modul yang dihapus.
```

---

### 5. Dekompilasi Binary Native (Perlu Ghidra/Hopper/IDA)

> ⚠️ **Prasyarat Tambahan:** Salah satu dari Ghidra, Hopper, atau IDA harus terinstal dan dikonfigurasi via environment variable.

**Konfigurasi Ghidra (gratis & open source):**
```powershell
# Setelah mengunduh dari https://ghidra-sre.org/ (versi 12.1.x+)
$env:GHIDRA_INSTALL_DIR = "C:/ghidra_12.1"
# Tambahkan ke System Environment Variables secara permanen untuk tetap aktif
```

**Template Prompt:**
```text
Gunakan REA dengan Ghidra untuk mendekompilasi:
C:/path/ke/program.exe
Fokus pada fungsi yang berkaitan dengan [enkripsi / autentikasi / network].
Tampilkan pseudocode dan assembly dari fungsi yang relevan.
```

---

## 🛠️ Pemeliharaan & Troubleshooting

```bash
# Cek status dan diagnostik REA (207 tools harus healthy)
npx -y rea-agents@latest mcp doctor

# Update REA ke versi terbaru
npx -y rea-agents@latest update
# Lalu daftarkan ulang ke Antigravity:
npx -y rea-agents@latest setup --client antigravity --yes

# Instal ulang dari awal jika bermasalah
python vibe_tools/install_rea_mcp.py
```

---

## 📊 Kapabilitas REA (207 Tools Aktif, Profil Compact)

| Kategori Target | Deskripsi Kapabilitas REA |
| :--- | :--- |
| **JavaScript / Electron / ASAR** | Rekonstruksi statis modul, import, batas Electron, source map |
| **Web Bundle & Capture** | Analisis bundle halaman via CDP, inspeksi network HAR/mitmproxy |
| **Native Binary (ELF, Mach-O, PE)** | Pseudocode, assembly, strings, simbol, call graph via Ghidra/Hopper/IDA |
| **Android APK / JADX** | Inspeksi kelas, metode, referensi masuk/keluar |
| **Managed .NET Assembly** | Inventaris member bertipe, deklarasi P/Invoke |
| **Firmware** | Inspeksi dan analisis region firmware |
| **Proses Runtime (ADB, Frida)** | Observasi UI, eksekusi Frida script, capture jaringan |
| **Perbandingan Versi** | Diff dua Evidence bundle dari dua versi aplikasi |

---

## 📚 Referensi Resmi

- [🐙 Repositori GitHub REA (morluto/rea)](https://github.com/morluto/rea)
- [🌐 Website Resmi REA](https://rea.tools/)
- [📖 Dokumentasi Instalasi Lengkap](https://github.com/morluto/rea/blob/main/docs/installation.md)
- [📦 npm Package: rea-agents](https://www.npmjs.com/package/rea-agents)
- [💬 Komunitas Discord REA](https://discord.gg/GkcryMnJDM)
