# 🚀 Master Guide: Setup Vibe Coding Cerdas, Ramping & Hemat Token untuk Proyek Baru

> 💡 **Tujuan Dokumen**: Panduan dan template prompt siap pakai untuk memasang seluruh ekosistem **Agent Customization**, **Knowledge Graph (Graphify)**, **Auto-Peta Berkas (.agents/MAP.md)**, **Modular Guardrails**, dan **Otomasi Git** ke dalam proyek baru manapun. Cukup berikan prompt ini ke AI pada proyek baru, dan seluruh sistem akan langsung terpasang otomatis!

---

## 🧭 Daftar Isi
1. [🌟 Manfaat Ekosistem Ini Bagi Proyek Baru](#-manfaat-ekosistem-ini-bagi-proyek-baru)
2. [📋 Prasyarat Sistem & Dependensi](#-prasyarat-sistem--dependensi)
3. [⚡ Master Prompt Sekali Tempel (Copy-Paste ke AI)](#-master-prompt-sekali-tempel-copy-paste-ke-ai)
4. [🛠️ Opsi Alternatif: Setup Otomatis via Skrip Python Mandiri](#️-opsi-alternatif-setup-otomatis-via-skrip-python-mandiri)
5. [📁 Struktur Berkas Hasil Pemasangan](#-struktur-berkas-hasil-pemasangan)
6. [🎯 Cheat-Sheet Prompting Harian (Vibe Coding Efisien)](#-cheat-sheet-prompting-harian-vibe-coding-efisien)

---

## 🌟 Manfaat Ekosistem Ini Bagi Proyek Baru

Dengan memasang ekosistem ini, proyek baru Anda akan memiliki keunggulan:
- 📉 **Hemat Kuota Token Drastis (Hingga 70%+)**: AI tidak perlu membaca seluruh isi file atau meraba-raba struktur folder. AI dipandu urutan eksplorasi: `.agents/MAP.md` → `grep_search` → sliced `view_file` (maks 100 baris).
- 🛡️ **Anti-Kode Spageti & Anti-Monolitik**: Mencegah AI menggabungkan fungsi-fungsi menjadi satu file raksasa ribuan baris (*Universal No Monolithizing*). Kode otomatis dipecah rapi (*Separation of Concerns* & *Facade Pattern*).
- 🕸️ **Knowledge Graph Tanpa Kuota API**: Memanfaatkan Graphify lokal untuk memetakan dependensi kode dan wiki secara instan tanpa mengonsumsi token konteks LLM.
- 💬 **Komunikasi & Dokumentasi Bahasa Indonesia**: Percakapan, komentar fungsi, dan docstring otomatis ditulis dalam Bahasa Indonesia yang jelas dan profesional.
- 🔒 **Aman dari Git Overwrite**: AI dilarang melakukan `git commit` / `git push` otomatis tanpa persetujuan, dan folder `.git` dibersihkan dari gangguan file sistem seperti `desktop.ini` (khusus pengguna Google Drive).
- 🧩 **100% Ramah Setup Spesialis (Non-Destruktif)**: Menjamin berkas, skrip, dan aturan khusus yang sudah ada di proyek tidak akan pernah dihapus atau ditimpa. AI hanya menambahkan guardrails efisiensi di sekelilingnya tanpa merusak fondasi unik proyek Anda.

---

## 📋 Prasyarat Sistem & Dependensi

Sebelum meminta AI melakukan setup atau sebelum menjalankan pipeline, pastikan hal-hal berikut telah terpasang di komputer:

1. **Python 3.9+** telah terpasang.
2. **Library Graphify**:
   ```bash
   pip install -q graphifyy
   ```
3. **Git**: Git command line terpasang dan dapat diakses dari terminal/PowerShell.

---

## ⚡ Master Prompt Sekali Tempel (Copy-Paste ke AI)

> 📌 **Cara Pakai**: Buka proyek baru Anda di IDE (misal Antigravity IDE), lalu buka chat AI baru dan **tempelkan teks di bawah ini seluruhnya**. AI akan membaca instruksi dan langsung membangun seluruh fondasi proyek!

```markdown
Hai AI, tolong siapkan fondasi Vibe Coding cerdas, hemat token, modular, dan terstruktur rapi untuk proyek ini.
Pasang seluruh konfigurasi agent (.agents), aturan modularitas, skrip pembuat peta file otomatis, integrasi graphify, serta skrip git helper dengan rincian berikut:

### ⚠️ Sifat Pemasangan (Non-Destruktif & Pelestarian Setup Spesialis):
1. **DILARANG MENGHAPUS SETUP ASING / SPESIALIS**:
   - Setiap proyek memiliki keunikan dan spesialisasi kebutuhan sendiri (misal: konfigurasi Docker, database khusus, Playwright, API bot, pipeline CI/CD, modul scraping, atau berkas konfigurasi pihak ketiga).
   - Jika mendapati berkas, folder, atau aturan yang terasa "asing" atau di luar template standar ini, **JANGAN DIHAPUS, JANGAN DIUBAH, DAN JANGAN DISEDERHANAKAN**. Wajib 100% dipertahankan!
2. **Merge Cerdas untuk `.agents/AGENTS.md`**:
   - Jika `.agents/AGENTS.md` sudah ada dan memuat aturan khusus proyek, **pertahankan seluruh aturan lama tersebut**.
   - Cukup selipkan atau tambahkan guardrails Vibe Coding (hemat token, sliced view, anti-monolitik, RTK guardrails) di bagian bawahnya tanpa menimpa aturan yang sudah ada.
3. **Smart Gap-Filling (Hanya Lengkapi yang Belum Ada)**:
   - Cek terlebih dahulu direktori proyek sebelum membuat berkas apapun.
   - Jika suatu aturan, skill, atau skrip sudah ada, **lewati dan jangan timpa**.
   - Jika Graphify sudah ada tetapi folder `graphify-out/wiki/` belum terbentuk, jalankan perintah ekspor wiki (`graphify export wiki`).
   - Jika `.agents/MAP.md` sudah ada catatan deskripsi manual, **wajib dipertahankan** dan hanya daftarkan berkas baru.

---

### 1. Struktur Folder dan File Target:
Pastikan direktori dan berkas berikut tersedia lengkap di root proyek ini:
- `.agents/AGENTS.md`
- `.agents/MAP.md`
- `.agents/rules/python-clean-architecture.md`
- `.agents/rules/graphify.md`
- `.agents/skills/modular-refactor/SKILL.md`
- `.agents/skills/unit-test-generator/SKILL.md`
- `.agents/workflows/graphify.md`
- `vibe_tools/graphify_sync.py` (Penggabungan pembaruan Knowledge Graph dan generator peta file AST)
- `vibe_tools/push_to_github.py` (Otomasi Git commit & push aman)
- `vibe_tools/setup_vibe_ecosystem.py` (Generator ekosistem repo baru)
- `vibe_tools/install_hermes_antigravity.py` (Installer Hermes Agent MCP)
- `vibe_tools/install_openrouter_mcp.py` (Installer OpenRouter MCP)

---

### 2. Isi Spesifik Setiap File (Hanya Buat Jika Belum Ada):

#### A. `.agents/AGENTS.md`
Isi dengan panduan guardrails agent (dalam Bahasa Inggris padat agar hemat token prompt sistem):
```markdown
# Custom Agent Rules

## Communication & Language
- **User Explanations**: ALWAYS communicate in **Indonesian** during chatting and vibe coding.
- **Code Comments & Docstrings**: MUST be written in **Indonesian**.

## Execution & Code Changes
- **Direct Code Changes**: Apply file edits directly without implementation_plan.md or walkthrough.md unless requested.
- **No Autonomous Testing on Updates**: DO NOT run self-tests, syntax checks, or builds after edits. Let user test manually first.
- **Autonomous Error Fixing**: Autonomously fix and verify runtime crashes/errors reported by user.
- **Proactive Command Execution**: Execute routine terminal commands directly without asking confirmation.
- **Minimal Context**: Focus strictly on target files; avoid broad scans/greps unless requested.
- **Token Efficiency**: Never load whole large files; use sliced viewing (StartLine/EndLine, max 100 lines) focused on target functions.
- **Exploration Order**: .agents/MAP.md -> grep_search -> sliced view_file. Use graphify-out/wiki only for cross-module relationships.
- **RTK Emulation & CLI Guardrails**: Drastically prevent terminal stdout token bloat:
  - Enforce quiet/summary flags where available (pip -q, git status -s, git diff --stat, pytest -q).
  - Redirect verbose outputs to temp logs and inspect tails only (> scratch/tmp.log 2>&1; Get-Content ... -Tail 10).
  - Prefer boolean/sentinel checks (Test-Path, (Get-ChildItem).Count, exit code) over dumping object listings.
  - Never view files via shell commands (cat, type, Get-Content); strictly use native sliced view_file.
  - Always compress remaining CLI output via pipes (Select -First 20, Select-String).
- **Cache Friendly**: Keep system rules and prompt prefixes stable to maximize API cache hits.
- **Data Pre-aggregation**: Never read raw CSV, JSON, or log files directly; aggregate data via python scripts first and inspect summary only.
- **Git Auto-Commit Control**: NEVER run git commit or git push automatically.
- **Graphify Refresh**: Run graphify update . or python vibe_tools/graphify_sync.py on structural changes.

## Modular Architecture Guardrails
- **Universal No Monolithizing**: STRICTLY FORBIDDEN to create monolithic scripts exceeding 300 lines. Separate concerns across dedicated packages.
- **Facade Pattern**: Keep root entry points slim and backward-compatible, delegating heavy logic to modular subpackages.
- **Direct Unicode Symbols**: NEVER use LaTeX math notation (e.g. $\rightarrow$). Always use direct Unicode symbols (e.g. ->, •).
```

#### B. `.agents/rules/python-clean-architecture.md`
```markdown
---
trigger: always_on
description: Standar arsitektur bersih, batasan panjang berkas, dan efisiensi token.
globs: ["*.py"]
---

# Standar Clean Architecture & Efisiensi Token
1. **Batas Ukuran Berkas (Maksimal 250 - 300 Baris)**: Pecah berkas menjadi sub-modul terfokus jika mendekati 300 baris.
2. **Separation of Concerns**: Pisahkan konfigurasi, logika inti (domain), integrasi eksternal, dan launcher/entry point.
3. **Dokumentasi & Bahasa**: Semua komentar kode, docstring modul/fungsi, dan log teknis WAJIB menggunakan Bahasa Indonesia.
4. **Edit Tertarget**: Gunakan replace_file_content berbasis baris tertarget, hindari menulis ulang seluruh berkas.
```

#### C. `.agents/rules/graphify.md`
```markdown
---
trigger: always_on
description: Gunakan knowledge graph graphify-out/ untuk menjawab arsitektur proyek.
---

## Aturan Graphify
- Periksa knowledge graph lebih dulu bila graphify-out/graph.json ada: gunakan graphify query, graphify path, atau graphify explain.
- Telusuri graphify-out/wiki/index.md daripada membaca berkas mentah secara acak.
- Jalankan python graphify_update.py setelah modifikasi struktural kode.
- Bersihkan arsip lama di graphify-out/, pertahankan maksimal 2 arsip terbaru.
```

#### D. `.agents/skills/modular-refactor/SKILL.md`
```markdown
---
name: modular-refactor
description: Panduan refactoring inkremental memecah skrip monolitik menjadi modular dengan kompatibilitas mundur 100%.
---

# Skill: Modular Refactor
1. **Zero Regression**: Pertahankan antarmuka dan launcher lama menggunakan Facade Pattern.
2. **Inkremental**: Pindahkan satu domain/submodul dalam satu waktu ke folder paket terpisah.
3. **Docstring & Type Hints**: Tambahkan docstring Bahasa Indonesia dan type hints.
4. **Update Graph & Map**: Jalankan python graphify_update.py setelah selesai.
```

#### E. `.agents/skills/unit-test-generator/SKILL.md`
```markdown
---
name: unit-test-generator
description: Pembuatan unit test cepat dan terisolasi menggunakan pytest dan unittest.mock.
---

# Skill: Unit Test Generator
1. **Strict Mocking**: Selalu mock I/O, koneksi internet, database, dan browser. Hindari ketergantungan nyata saat tes.
2. **Fokus & Ringkas**: Uji fungsi secara terisolasi (panjang test file < 150 baris).
3. **Bahasa**: Gunakan docstring dan penamaan test dalam Bahasa Indonesia yang jelas.
```

#### F. `.agents/workflows/graphify.md`
```markdown
---
name: graphify
description: Membangun knowledge graph navigasi untuk direktori proyek.
---

# Workflow: graphify
Jalankan perintah: python vibe_tools/graphify_sync.py
```

#### G. `vibe_tools/graphify_sync.py`
Skrip Python terpadu 1-klik untuk:
1. Memindai kode proyek via AST, mengekstrak docstring, menghitung jumlah baris, dan memperbarui `.agents/MAP.md` secara non-destruktif.
2. Memperbarui Knowledge Graph (`graphify update .`) dan mengekspor wiki (`graphify export wiki`).
3. Memverifikasi konsistensi wiki vs graph.
4. Merapikan folder arsip lama di `graphify-out/` (maksimal 2 arsip terbaru).
*Mendukung flag `--map-only` untuk pembaruan instan MAP.md tanpa graphify.*

#### H. `vibe_tools/push_to_github.py`
Skrip otomasi git push aman:
- Membersihkan `desktop.ini` di `.git` (mencegah error sinkronisasi cloud).
- Otomatis berpindah direktori kerja ke root git repositori.
- Memeriksa batas ukuran file (>50MB / >100MB).
- Melakukan staging, commit interaktif/otomatis, dan push ke branch aktif.

#### I. `.agents/MAP.md`
Inisialisasi file `.agents/MAP.md` dengan header navigasi dan daftarkan file-file awal yang telah dibuat.

Setelah semua file dibuat, jalankan pemindaian awal dengan `python vibe_tools/graphify_sync.py --map-only` agar `.agents/MAP.md` langsung terisi lengkap!
```

---

## 🛠️ Opsi Alternatif: Setup Instan via Skrip Python Mandiri (0 Token AI)

Jika Anda tidak ingin membuang kuota token percakapan AI sama sekali pada proyek baru, gunakan skrip mandiri [`setup_vibe_ecosystem.py`](file:///i:/My%20Drive/Kerja/Scrapper_new_acmt/setup_vibe_ecosystem.py) yang sudah kami buatkan secara lengkap di repositori ini.

### ⚡ Langkah Pemasangan 1-Detik:
1. **Salin** berkas [`setup_vibe_ecosystem.py`](file:///i:/My%20Drive/Kerja/Scrapper_new_acmt/setup_vibe_ecosystem.py) ke root folder proyek baru Anda.
2. **Jalankan** perintah terminal / PowerShell di folder tersebut:
   ```bash
   python vibe_tools/setup_vibe_ecosystem.py
   ```
3. **Selesai!** Dalam 1 detik, seluruh folder `.agents/`, semua berkas rules, skills, workflows, skrip otomasi di `vibe_tools/`, dan peta awal `.agents/MAP.md` akan langsung ter-generate secara otomatis!

---

## 📁 Struktur Berkas Hasil Pemasangan

Setelah ekosistem terpasang, direktori proyek baru Anda akan memiliki tata letak standar berikut:

```text
📁 NAMA_PROYEK/
├── 📁 .agents/
│   ├── 📄 AGENTS.md                  # Aturan utama agent (guardrails, hemat token, anti-monolitik)
│   ├── 📄 MAP.md                     # Peta navigasi file ringkas (indeks utama AI saat mulai sesi)
│   ├── 📁 rules/
│   │   ├── 📄 graphify.md            # Aturan penggunaan knowledge graph
│   │   └── 📄 python-clean-architecture.md # Aturan batas 300 baris & clean code
│   ├── 📁 skills/
│   │   ├── 📁 modular-refactor/      # Skill memecah skrip monolitik (Facade Pattern)
│   │   └── 📁 unit-test-generator/   # Skill membuat unit test terisolasi (Mocking)
│   └── 📁 workflows/
│       └── 📄 graphify.md            # Shortcut workflow /graphify
│
├── 📁 vibe_tools/                     # 🧰 Kotak perkakas portabel vibe coding
│   ├── 🐍 graphify_sync.py           # Pipeline 1-klik (update graph -> wiki -> MAP.md -> rapikan arsip)
│   ├── 🐍 push_to_github.py          # Otomasi git add/commit/push interaktif & pembersih desktop.ini
│   ├── 🐍 setup_vibe_ecosystem.py    # Generator instan .agents & ekosistem repo baru
│   ├── 🐍 install_hermes_antigravity.py # Installer otomatis Hermes Agent MCP
│   ├── 🐍 install_openrouter_mcp.py  # Installer otomatis OpenRouter MCP
│   └── 📄 README.md                  # Katalog panduan isi folder vibe_tools
│
└── 📁 (Modul Proyek Anda)             # Kode aplikasi Anda yang terstruktur rapi
```

---

## 🎯 Cheat-Sheet Prompting Harian (Vibe Coding Efisien)

Gunakan *template prompt* ringkas ini untuk berinteraksi dengan AI di proyek baru Anda:

### 1. Memulai Fitur Baru / Modul Baru
> *"Buatkan modul baru untuk [nama fitur] di dalam folder `core/` (atau nama package terkait). Jangan taruh logika berat di root entry point, pertahankan batas di bawah 250 baris, dan gunakan komentar serta docstring Bahasa Indonesia."*

### 2. Memecah File yang Membengkak (>300 Baris)
> *"Tolong rampingkan file `nama_file.py` menggunakan skill `modular-refactor`. Pecah fungsinya ke dalam folder modular terpisah, jadikan file utama sebagai facade entry point ramping dengan backward compatibility 100%, lalu jalankan `python vibe_tools/graphify_sync.py`."*

### 3. Menanyakan Arsitektur & Relasi Kode Tanpa Boros Token
> *"Gunakan knowledge graph `graphify-out/` atau `graphify query` untuk menjelaskan bagaimana alur data dari modul A menuju modul B tanpa membaca keseluruhan isi file."*

### 4. Membuat Unit Test Cepat
> *"Gunakan skill `unit-test-generator` untuk membuatkan unit test modul `core/fitur.py`. Terapkan strict mocking pada semua I/O dan jaringan, simpan di `tests/test_fitur.py`."*

### 5. Sinkronisasi Kode ke GitHub
> *"Tolong jalankan `python push_github.py` untuk mengunggah perubahan terbaru ke GitHub secara aman."*

---

> 💡 **Tips Pro**: Simpan file panduan ini di Google Drive atau repository Anda sebagai aset berharga. Setiap kali membuat repo/proyek baru, Anda tinggal menyalin isi bagian **Master Prompt Sekali Tempel** ke chat AI pertama!
