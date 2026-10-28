# 🧰 Vibe Tools: Kotak Perkakas Portabel Vibe Coding

<p align="center">
  <a href="README.md">🇮🇩 Baca dalam Bahasa Indonesia</a> •
  <a href="README_EN.md">🇬🇧 Read in English</a>
</p>

Folder ini berisi seluruh skrip otomasi, installer MCP, generator ekosistem, server MCP, schema, dan panduan dokumentasi *vibe coding* cerdas, hemat token, dan anti-regresi. 

Folder ini dirancang agar **100% portabel (Self-Contained)**: siap disalin ke proyek baru atau PC baru mana pun.

---

## ⚡ Cara Pakai di Proyek Baru / PC Baru

### Metode 1: Sebagai Git Submodule (Paling Direkomendasikan)
Hubungkan repositori `vibe-tools` sebagai submodule agar selalu tersinkronisasi:
```bash
# 1. Tambahkan submodule di root proyek Anda
git submodule add https://github.com/baliaga-repo/vibe-tools.git vibe_tools

# 2. Jalankan installer otomatis 1-klik
python vibe_tools/setup_vibe_ecosystem.py
```

### Metode 2: Salin Folder Langsung (Standalone)
1. Salin folder `vibe_tools/` ini ke dalam folder proyek baru Anda.
2. Buka terminal proyek tersebut, lalu jalankan:
   ```cmd
   python vibe_tools/setup_vibe_ecosystem.py
   ```
3. Skrip otomatis akan:
   - ✅ Memasang seluruh library Python yang belum ada (`mcp`, `requests`, `graphifyy`, dependensi Hermes) via pip.
   - ✅ Mengonfigurasi root Antigravity IDE (`~/.gemini` dan `~/.gemini/config/mcp_config.json`) secara dinamis.
   - ✅ Memasang server MCP OpenRouter (`tanya_openrouter`) & Hermes Agent (`delegasikan_ke_hermes`).
   - ✅ Memasang schema MCP Antigravity di `~/.gemini/antigravity-ide/mcp/`.
   - ✅ Memasang global skill `/graphify` di `~/.gemini/config/skills/graphify/SKILL.md`.
   - ✅ Menyinkronkan OpenRouter API Key secara otomatis di semua tempat.
   - ✅ Membangun seluruh aturan `.agents/AGENTS.md` (Dual-Agent: Gemini context-heavy + OpenRouter/Hermes deep reasoning).
   - ✅ Memasang pengaman biaya cerdas: **Predictive Token Budgeting** (`cost_estimator.py`) dan **Interactive Model Selector** (`ask_question`).
   - ✅ Mengaktifkan **Bilingual Token Optimization** (English Bridge Pipeline) untuk menghemat 30%–50% saldo token OpenRouter.
   - ✅ Menegakkan aturan **Model Transparency & Confirmation** sebelum koding.
4. **Restart Antigravity IDE**, dan semua tools langsung aktif 100%!

---

## 📁 Katalog Isi Berkas

### 🐍 Skrip Otomasi Python
1. **`setup_vibe_ecosystem.py`** (Master Installer)  
   - *Fungsi*: Generator instan 1-klik yang mengotomatisasi seluruh pemasangan di atas tanpa konfigurasi manual.

2. **`openrouter_mcp.py`** & **`hermes_mcp.py`**  
   - *Fungsi*: Source code server MCP yang otomatis disalin ke `~/.gemini/` dengan path dinamis (bebas hardcode).

3. **`sync_universal.py`** (Universal Junction Linker)  
   - *Fungsi*: Menghubungkan direktori `vibe_tools/skills/` dan `vibe_tools/rules/` langsung ke Antigravity Global Root (`~/.gemini/config/`) menggunakan Windows NTFS Junction (`mklink /J`). Semua skill & rules otomatis aktif di SEMUA project tanpa copy-paste.

4. **[`skills/`](skills/README.md)** (Katalog 15 Skill Universal — [📖 Buka Panduan & Contoh Lengkap](skills/README.md))  
   - *Fungsi*: Menyimpan seluruh skill rekayasa perangkat lunak teroptimasi (termasuk paket rekayasa Matt Pocock, Graphify, Modular Refactor, Unit Test Generator):
     - `/grill-me`, `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/implement`
     - `/code-review`, `/diagnosing-bugs`, `/tdd`, `/codebase-design`, `/handoff`
     - `/retro`, `/ask-matt`, `/graphify`, `/modular-refactor`, `/unit-test-generator`
   - *Dokumentasi Lengkap*: Lihat penjelasaan mendalam, skenario penggunaan, dan contoh prompt nyata di [**`skills/README.md`**](skills/README.md).

5. **`rules/`** (Aturan Ekosistem Universal)  
   - *Fungsi*: Aturan arsitektur bersih (`python-clean-architecture.md`), efisiensi token & CLI guardrails (`token-efficiency.md`), dan Graphify navigation (`graphify.md`).

6. **`mcp_schemas/`**  
   - *Fungsi*: Schema JSON bawaan Antigravity untuk `hermes_agent` dan `openrouter` (siap pakai offline).

5. **`graphify_sync.py`**  
   - *Fungsi*: Penggabungan utuh antara update Knowledge Graph (Graphify) dan generator peta file AST (`.agents/MAP.md`).
   - *Fitur Cepat*:
     - `python vibe_tools/graphify_sync.py` → Jalankan sinkronisasi lengkap (graph, wiki, MAP.md, arsip).
     - `python vibe_tools/graphify_sync.py --map-only` → Hanya perbarui `.agents/MAP.md` dalam hitungan milidetik.
     - `python vibe_tools/graphify_sync.py --graph-only` → Hanya perbarui Graphify & Wiki.

6. **`push_to_github.py`**  
   - *Fungsi*: Otomasi Git staging, commit, dan push interaktif dengan pengaman file besar (>50MB/100MB) dan pembersihan file sistem (`desktop.ini`).

7. **`install_hermes_antigravity.py`**  
   - *Fungsi*: Installer mandiri Hermes Agent + MCP Worker bridge ke Antigravity IDE.

8. **`install_openrouter_mcp.py`**  
   - *Fungsi*: Installer mandiri OpenRouter MCP Server ke Antigravity IDE.

9. **`cost_estimator.py`**  
   - *Fungsi*: Kalkulator estimasi token & biaya USD berbasis tarif resmi OpenRouter serta generator opsi untuk modal interaktif `ask_question`.

10. **`docstring_translator.py`**  
    - *Fungsi*: Penerjemah docstring otomatis berbasis AST ke format dwibahasa `[ID]` & `[EN]` yang terintegrasi dengan GitHub Actions.

11. **`install_rea_mcp.py`**  
    - *Fungsi*: Installer otomatis REA MCP Server ([morluto/rea](https://github.com/morluto/rea)) ke Antigravity IDE. Mendaftarkan 207 tools reverse engineering (ASAR, Electron, APK Android, native binary) dengan profil compact hemat token.

12. **`setup_roo_hybrid.py` & `roo_hybrid/`** ([📖 Panduan Cepat](PANDUAN_ROO_CODE_HYBRID.md))  
    - *Fungsi*: Installer & updater portabel arsitektur **Hybrid Dual-Cockpit (VS Code Roo Code + Antigravity + Ollama RTX 3060)**. Memasang/memperbarui `.roomodes` (7 mode), `.roo/rules/*`, `.roo/commands/*` (`/pakai-rag`, `/pakai-3b`, `/pakai-7b`, `/adu-metode`, `/grill-me`), dan `.roo/mcp.json` bebas API key ke proyek saat ini maupun proyek lain (`--target "D:/ProjectLain"`).

---

### 📄 Dokumentasi & Cheat-Sheet Prompting

#### 🎯 Panduan Sentral Ekosistem (Utama)
1. **[`PANDUAN_LENGKAP_EKOSISTEM.md`](PANDUAN_LENGKAP_EKOSISTEM.md)** ⭐
   - **Panduan Konsolidasi Lengkap**: Menyatukan seluruh panduan ekosistem dalam satu dokumen terstruktur:
     - 📖 **Bab 1**: Docstring Translator bilingual `[ID]` & `[EN]`
     - 🧪 **Bab 2**: Testing modal interaktif `ask_question` & cost estimator
     - 🔄 **Bab 3**: Sinkronisasi Git Submodule `vibe_tools`
     - 🔍 **Bab 4**: REA MCP untuk reverse engineering (ASAR, APK, binary)
     - ⚡ **Bab 5**: Hermes Agent x Antigravity IDE (arsitektur Duo-Model)
     - 🌐 **Bab 6**: OpenRouter MCP, alias cerdas, dan katalog model
     - ❓ **Bab 7**: FAQ & Troubleshooting

#### 📚 Dokumen Pendukung
2. **`PANDUAN_SETUP_VIBE_CODING_BARU.md`**  
   - Master panduan dan prompt siap tempel (*copy-paste*) ke AI pada proyek baru untuk memasang ekosistem secara non-destruktif.

3. **`Prompt_AI.md`**  
   - Katalog kata kunci sakti (*Targeted Context Tagging*, *Progressive Disclosure*, *Facade Pattern*, *Repomix*, dll.) dan pola prompting hemat token.

---

## 🔄 Alur Sinkronisasi & Pembaruan Lintas Proyek

> 💡 **Panduan Lengkap & Troubleshooting**: Baca [TUTORIAL_SINKRONISASI_VIBE_TOOLS.md](TUTORIAL_SINKRONISASI_VIBE_TOOLS.md) untuk langkah-langkah detail, pembersihan cache Google Drive, dan template prompt AI siap pakai.

Karena `vibe_tools` menggunakan **Git Submodule**, Anda dapat mengeditnya langsung dari proyek mana pun yang sedang Anda kerjakan:

### 1. Mengedit & Push Pembaruan dari Proyek Mana Saja
Jika Anda menambahkan skrip atau memperbaiki prompt di dalam folder `vibe_tools/`:
```bash
# Masuk ke folder submodule
cd vibe_tools

# Push langsung ke repositori vibe-tools (otomatis atau git biasa)
python push_to_github.py
# Atau: git add . && git commit -m "feat: fitur baru" && git push origin main

# Kembali ke root proyek utama dan simpan catatan pointer versi
cd ..
git add vibe_tools
git commit -m "chore: perbarui vibe_tools ke versi terbaru"
git push
```

### 2. Mengambil Pembaruan di Proyek Lain (PC Sama / PC Lain)
Buka terminal di root proyek lain yang sudah terhubung dengan `vibe_tools`, lalu jalankan:
```bash
git submodule update --remote --merge
```
*Seketika seluruh file di folder `vibe_tools` pada proyek tersebut akan otomatis sinkron ke versi terbaru.*

### 3. Clone Proyek di Komputer / Laptop Baru
Saat meng-clone proyek yang memiliki submodule di komputer baru:
```bash
# Clone sekaligus mengunduh isi submodule
git clone --recurse-submodules <URL_REPOSITORI_PROYEK>

# Jika terlanjur clone biasa dan folder vibe_tools masih kosong:
git submodule update --init --recursive
```

### 4. Menjalankan Ulang Setup (Jika Ada Tool / MCP Baru)
Jika pembaruan menyertakan MCP server baru atau library baru:
```bash
python vibe_tools/setup_vibe_ecosystem.py
```

---

## 🤝 Berkontribusi (Contributing)

Kontribusi sangat terbuka untuk siapa saja! Baik berupa penambahan MCP server baru, perbaikan prompt template, optimasi token, maupun pengayaan skrip:
1. **Fork** repositori ini: [github.com/baliaga-repo/vibe-tools](https://github.com/baliaga-repo/vibe-tools)
2. Buat branch baru: `git checkout -b fitur/nama-fitur`
3. Commit perubahan: `git commit -m "feat: deskripsi perubahan"`
4. Push ke branch Anda: `git push origin fitur/nama-fitur`
5. Buat **Pull Request (PR)** di GitHub.

---

## 📄 Lisensi (License)

Proyek ini dilisensikan di bawah [MIT License](LICENSE) — bebas digunakan, dimodifikasi, dan didistribusikan untuk proyek pribadi maupun komersial.
