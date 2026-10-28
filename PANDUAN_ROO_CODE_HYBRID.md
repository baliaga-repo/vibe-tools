# ⚡ Quick-Start Cheat-Sheet: Roo Code Hybrid Dual-Cockpit

Panduan ringkas 1 halaman untuk mengoperasikan VS Code Roo Code yang terintegrasi dengan Antigravity IDE dan Ollama RTX 3060.

---

## 🎯 4 Profil API Roo Code (Settings -> Profiles)

1. **`DeepSeek-R1 (OpenRouter)`**:
   - URL: `https://openrouter.ai/api/v1` | Model: `deepseek/deepseek-r1`
   - Digunakan untuk mode: `grill-me-spec`, `bug-hunter`
2. **`Claude 3.7 Sonnet (OpenRouter)`**:
   - URL: `https://openrouter.ai/api/v1` | Model: `anthropic/claude-3.7-sonnet`
   - Digunakan untuk mode: `orchestrator`, `code-reviewer`
3. **`Gemini Flash Free (OpenRouter / Google)`**:
   - Model: `google/gemini-2.0-flash-001`
   - Digunakan untuk mode: `vibe-coder`
4. **`Ollama Local RTX 3060 (0 Token Cost)`**:
   - URL: `http://localhost:11434/v1` | Model: `qwen2.5-coder:7b-instruct-q4_K_M`
   - Digunakan untuk mode: `local-scout-3b`, `local-scout-7b`

---

## ⌨️ Shortcut Perintah Chat (Slash Commands)

- `/pakai-rag`   : Pakai penelusuran codebase context Antigravity.
- `/pakai-3b`    : Alihkan pencarian file ke model lokal Ollama 3B (hemat VRAM).
- `/pakai-7b`    : Analisis mendalam offline dengan model lokal Ollama 7B.
- `/adu-metode`  : Bandingkan jawaban pencarian model lokal vs cloud.
- `/grill-me`    : Wawancara interaktif untuk mematangkan arsitektur sebelum coding.
- `/to-spec`     : Susun dokumen spesifikasi teknis formal.
- `/to-tickets`  : Pecah spesifikasi teknis menjadi tiket modular terurut.
- `/implement`   : Eksekusi tiket satu per satu secara disiplin.

---

## 🛡️ Saklar REA MCP (Reverse Engineer Anything)

REA MCP mengonsumsi ~25.000 token per putaran pesan. Pastikan selalu nonaktif kecuali saat rekayasa balik biner:
```powershell
python vibe_tools/rea_tool.py --status   # Cek kondisi di Antigravity & Roo Code
python vibe_tools/rea_tool.py --disable  # NONAKTIF (Hemat ~25K token)
python vibe_tools/rea_tool.py --enable   # AKTIF (Untuk reverse engineering)
```

---

## 🔄 Pembaruan Ekosistem Otomatis
```powershell
python vibe_tools/update_ecosystem.py --check
python vibe_tools/update_ecosystem.py --target "D:/Path/Ke/ProjectLain"
```
