# 🦓 Quick-Start Cheat-Sheet: Zoo Code / Roo Code Hybrid Dual-Cockpit

Panduan ringkas 1 halaman untuk mengoperasikan **Zoo Code** (penerus resmi Roo Code) yang terintegrasi dengan Antigravity IDE dan Ollama RTX 3060.
Untuk tutorial setup lengkap dengan pemecahan masalah (troubleshooting VSIX offline, wizard setup, letak tombol model), buka:
👉 [**`vibe_tools/PANDUAN_ZOO_CODE_HYBRID.md`**](file:///d:/mobog/Videos/Youtube%20Download/vibe_tools/PANDUAN_ZOO_CODE_HYBRID.md)

---

## 🎯 Rekomendasi Model Paling Irit

1. **`deepseek/deepseek-chat` (DeepSeek-V3)**: Koding pintar harian paling murah (~Rp 2.200 per 1M token).
2. **`google/gemini-2.0-flash-001`**: Baca file besar super ngebut & murah (~Rp 1.500 per 1M token).
3. **`deepseek/deepseek-r1`**: Khusus penalaran arsitektur rumit (/grill-me & /to-spec) dengan harga 6x lebih murah dari Claude.
4. **`Ollama Local RTX 3060`**: 100% Gratis ($0) via model `qwen2.5-coder:3b` atau `7b`.

---

## 🎭 7 Custom Modes Siap Pakai

- **`🪃 Orchestrator (Selector)`** *(Default)*: Memimpin alur tugas, membagi kerja kasar lokal vs cloud.
- **`💻 Vibe Coder (Cloud Exec)`**: Eksekusi kode bersih, modular (<300 baris/file), auto `py_compile`.
- **`🏎️ Local Scout 3B (Fast $0)`**: Cari file & koordinat baris offline cepat di GPU RTX 3060.
- **`🚜 Local Scout 7B (Deep $0)`**: Analisis alur logika mendalam offline di GPU RTX 3060.
- **`🔥 Grill-Me & Spec (Architect)`**: Wawancara arsitektur fitur baru (hanya boleh edit folder `docs/`).
- **`🔍 Bug Hunter (Diagnose)`**: Investigasi akar masalah crash secara ilmiah sebelum sentuh kode.
- **`🛡️ Code Reviewer (Audit)`**: Audit kepatuhan standar clean architecture & keamanan.

---

## ⌨️ Shortcut Perintah Chat (Slash Commands)

- `/pakai-rag`   : Pakai penelusuran codebase context standar.
- `/pakai-3b`    : Alihkan pencarian file ke model lokal Ollama 3B (hemat VRAM).
- `/pakai-7b`    : Analisis mendalam offline dengan model lokal Ollama 7B.
- `/adu-metode`  : Bandingkan jawaban pencarian model lokal vs cloud.
- `/grill-me`    : Wawancara interaktif untuk mematangkan arsitektur sebelum coding.
- `/to-spec`     : Susun dokumen spesifikasi teknis formal ke `docs/specs/`.
- `/to-tickets`  : Pecah spesifikasi teknis menjadi tiket modular terurut di `docs/tickets/`.
- `/implement`   : Eksekusi tiket satu per satu secara disiplin.

---

## 🛡️ Saklar REA MCP (Reverse Engineer Anything)

REA MCP mengonsumsi ~25.000 token per putaran pesan. Pastikan selalu nonaktif kecuali saat rekayasa balik biner:
```powershell
python vibe_tools/rea_tool.py --status   # Cek kondisi di Antigravity & Zoo Code
python vibe_tools/rea_tool.py --disable  # NONAKTIF (Hemat ~25K token)
python vibe_tools/rea_tool.py --enable   # AKTIF (Untuk reverse engineering)
```

---

## 🔄 Pembaruan Ekosistem Otomatis
```powershell
python vibe_tools/update_ecosystem.py --check
python vibe_tools/update_ecosystem.py --target "D:/Path/Ke/ProjectLain"
```
