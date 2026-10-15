# 🧰 Vibe Tools: Kotak Perkakas Portabel Vibe Coding

Folder ini berisi seluruh skrip otomasi, installer MCP, generator ekosistem, server MCP, schema, dan panduan dokumentasi *vibe coding* cerdas, hemat token, dan anti-regresi. 

Folder ini dirancang agar **100% portabel (Self-Contained)**: siap disalin ke proyek baru atau PC baru mana pun.

---

## ⚡ Cara Pakai di Proyek Baru / PC Baru (Cukup 1 Baris Perintah!)

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
   - ✅ Memasang Hermes Agent CLI dan menyetel model default (`deepseek/deepseek-chat`).
   - ✅ Membangun seluruh aturan `.agents/AGENTS.md` (Dual-Agent: Gemini context-heavy + OpenRouter/Hermes deep reasoning), rules, skills, dan `.agents/MAP.md`.
4. **Restart Antigravity IDE**, dan semua tools langsung aktif 100%!

---

## 📁 Katalog Isi Berkas

### 🐍 Skrip Otomasi Python
1. **`setup_vibe_ecosystem.py`** (Master Installer)  
   - *Fungsi*: Generator instan 1-klik yang mengotomatisasi seluruh pemasangan di atas tanpa konfigurasi manual.

2. **`openrouter_mcp.py`** & **`hermes_mcp.py`**  
   - *Fungsi*: Source code server MCP yang otomatis disalin ke `~/.gemini/` dengan path dinamis (bebas hardcode).

3. **`mcp_schemas/`**  
   - *Fungsi*: Schema JSON bawaan Antigravity untuk `hermes_agent` dan `openrouter` (siap pakai offline).

4. **`graphify_SKILL.md`**  
   - *Fungsi*: Master global skill Graphify untuk direktori `~/.gemini/config/skills/graphify/SKILL.md`.

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


---

### 📄 Dokumentasi & Cheat-Sheet Prompting
1. **`PANDUAN_SETUP_VIBE_CODING_BARU.md`**  
   - Master panduan dan prompt siap tempel (*copy-paste*) ke AI pada proyek baru untuk memasang ekosistem secara non-destruktif.

2. **`Prompt_AI.md`**  
   - Katalog kata kunci sakti (*Targeted Context Tagging*, *Progressive Disclosure*, *Facade Pattern*, *Repomix*, dll.) dan pola prompting hemat token.

3. **`PANDUAN_HERMES_ANTIGRAVITY.md`**  
   - Panduan lengkap arsitektur dan cara kerja integrasi Hermes Agent dengan Antigravity IDE.

4. **`OPENROUTER_MCP_GUIDE.md`**  
   - Panduan konfigurasi OpenRouter MCP, alias cerdas (`r1`, `claude`, `sonnet`, `deepseek`, `free`), dan pengaman limit harian.
