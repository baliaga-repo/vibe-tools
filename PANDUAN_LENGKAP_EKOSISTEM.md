# 📚 Panduan Lengkap Ekosistem Vibe Tools

Dokumentasi komprehensif yang mengkonsolidasikan seluruh tutorial, panduan, dan best practice ekosistem vibe_tools dalam satu sumber terpadu.

---

## 📑 Daftar Isi

1. [Panduan Strategi & Prompt Siap Pakai (Antigravity IDE, Aider CLI, & Ponytail)](#1-panduan-strategi--prompt-siap-pakai-antigravity-ide-aider-cli--ponytail)
   * 1.1 [Contekan Cepat: Pilih Model & Tingkatan Sesuai Tahap (Anti-Bingung)](#11-contekan-cepat-pilih-model--cockpit-sesuai-tahap)
   * 1.2 [Alur Utama Pembangunan & Perombakan Fitur (3 Tahap Terpadu)](#12-alur-utama-pembangunan--perombakan-fitur-3-tahap-terpadu)
     * [Alur Pasca-Implementasi: Modifikasi & Fitur Lanjutan (Hemat Token)](#alur-pasca-implementasi-modifikasi--penambahan-fitur-lanjutan-hemat-token)
   * 1.3 [Tiga Prompt Spesialis Ringkas (Atasi Bug, Rapikan Kode /ponytail, & Mode Otak-Tangan)](#13-tiga-prompt-spesialis-ringkas-di-luar-bikin-fitur-baru)
   * 1.4 [Empat "Golden Rules" Anti-Blunder (Termasuk Anti-Sycophancy)](#14-tiga-golden-rules-anti-blunder)
2. [Docstring Translator Bilingual](#2-docstring-translator-bilingual)
3. [Sinkronisasi Git vibe_tools (Pindah PC ⇄ Laptop, Pengguna Publik, & Fork Global)](#3-sinkronisasi-git-vibe_tools-pindah-pc--laptop-pengguna-publik--fork-global)
   * 3.1 [Skenario Pindah PC ⇄ Laptop Anti-Bentrok](#31-skenario-pindah-pc--laptop-anti-bentrok)
   * 3.2 [Panduan Cepat untuk Pengguna Publik Baru (1 Menit)](#32-panduan-cepat-untuk-pengguna-publik-baru-1-menit)
   * 3.3 [Panduan Fork & Pull Request untuk Kontributor Global](#33-panduan-fork--pull-request-untuk-kontributor-global)
4. [REA MCP: Reverse Engineer Anything](#4-rea-mcp-reverse-engineer-anything)
5. [Hermes Agent x Antigravity IDE x Aider CLI & Self-Learning Universal](#5-hermes-agent-x-antigravity-ide-x-aider-cli--self-learning-universal)
   * 5.1 [Sinergi 3 Alat: Antigravity, Aider CLI, & Hermes Agent](#51-sinergi-3-alat-antigravity-aider-cli--hermes-agent)
   * 5.2 [Metode Pemasangan Cepat Mandiri (1 Menit)](#52-metode-pemasangan-cepat-mandiri-1-menit)
   * 5.3 [Pemasangan Manual Langkah Demi Langkah](#53-pemasangan-manual-langkah-demi-langkah)
   * 5.4 [🧠 Self-Learning Universal Lintas-Proyek](#54-self-learning-universal-lintas-proyek)
6. [Tutorial Setup PC/Laptop Baru dari Nol (Fresh Install Windows 10/11) & OpenRouter MCP](#6-tutorial-setup-pclaptop-baru-dari-nol-fresh-install-windows-1011--openrouter-mcp)
   * 6.1 [Tahap 1: Persiapan Dasar Windows 10/11 Baru](#61-tahap-1-persiapan-dasar-windows-1011-baru)
   * 6.2 [Tahap 2: Persiapan Akun & Saldo AI](#62-tahap-2-persiapan-akun--saldo-ai)
   * 6.3 [Tahap 3: Instalasi Aider Terisolasi & Auto-Approve Antigravity](#63-tahap-3-instalasi-aider-terisolasi--auto-approve-antigravity)
   * 6.4 [Tahap 4: Prompt Setup Mandiri & Alternatif Manual](#64-tahap-4-prompt-setup-mandiri--alternatif-manual)
   * 6.5 [Tahap 5: Verifikasi & Uji Koneksi](#65-tahap-5-verifikasi--uji-koneksi)
   * 6.6 [Tahap 6: Katalog Model Pilihan & Update Otomatis](#66-tahap-6-katalog-model-pilihan--update-otomatis)
   * 6.7 [Mode Otak-Tangan: Iterative Debug Loop & Session Cache](#67-mode-otak-tangan-iterative-debug-loop--session-cache)
7. [Katalog 15 Skill Universal & Panduan Penggunaan](#7-katalog-15-skill-universal--panduan-penggunaan)
8. [Arsitektur Hybrid Antigravity + Aider On-Demand (`:free` First) + Sinergi Hardware Lokal](#8-arsitektur-hybrid-antigravity--aider-on-demand-free-first--sinergi-hardware-lokal)
9. [Otomasi Pemeliharaan, Sinkronisasi Database, & Universal Updater Lintas-Proyek](#9-otomasi-pemeliharaan-sinkronisasi-database--universal-updater-lintas-proyek)

---

## 1. Panduan Strategi & Prompt Siap Pakai (Mode `/swarm` Dual-Orchestrator, Aider CLI, & Ponytail)

Panduan praktis satu pintu untuk merancang, memperbaiki bug, dan mengeksekusi kodingan secara terstruktur tanpa *over-engineering* (**`/ponytail`**), **0x ganti dropdown manual di tengah jalan**, serta **hemat kuota Claude hingga 85%+** dengan **Mode `/swarm` Native Antigravity**: Anda cukup parkir dropdown di **`Gemini 4 Neon (High)` / `Orchestrator (Neon)`** (atau **`Orchestrator (Argon)` / `Gemini 4 Argon (High)`** saat mode hemat Claude/refactor berat) sebagai **Coordinator**, dan biarkan Coordinator memanggil serta mematikan worker **`Claude Sonnet / Opus`** atau **`Gemini Argon / Hydrogen / Flash`** secara otomatis di ruang konteks bersih (*starts fresh*).

<a id="11-contekan-cepat-pilih-model--cockpit-sesuai-tahap"></a>
### 🧠 1.1 Contekan Cepat: Mode `/swarm` Dual-Orchestrator & Strategi 3 Pool Kuota (Anti-Ribet!)

> [!TIP]
> **Aturan Emas Parkir Dropdown & Manajemen 3 Pool Kuota (`/swarm`):**
> 1. **Pahami 3 Pool (Ember) Kuota Terpisah di Antigravity**:
>    - **Pool 1 — Harian (`Orchestrator (Neon)`, `Gemini 4 Neon`, `Hydrogen`, `3.8 Flash`)**: Reset paling cepat (harian/jam). Gunakan **`Gemini 4 Neon (High)`** atau **`Orchestrator (Neon)`** sebagai **Parkir Dropdown Harian Utama**.
>    - **Pool 2 — Mingguan (`Orchestrator (Argon)`, `Gemini 4 Argon`)**: Reset tiap **7 hari** (terpisah 100% dari Pool Neon & Claude!). Gunakan **`Orchestrator (Argon)`** / **`Gemini 4 Argon (High)`** sebagai **Coordinator Cadangan Strategis & Refactor Berat** (saat kuota Claude kritis `<= 15%`, saat Pool Neon menurun, atau saat memimpin Tahap 2+3 multi-file). *Jangan diparkir 100% untuk obrolan ringan harian agar kuota mingguan tetap awet.*
>    - **Pool 3 — Premium (`Claude Sonnet 5.5`, `Claude Opus 5.5`, `GPT-OSS 120B`)**: Semua model Claude berbagi **1 pool kuota yang sama** dan reset beberapa hari sekali. **DILARANG KERAS memarkir `Claude Opus` sebagai Orchestrator/Coordinator dropdown** karena riwayat chat panjang & loop tool CLI akan langsung menguras habis kuota Claude Anda!
> 2. **Awali Prompt Utama dengan `/swarm`**: Trigger ini mengaktifkan tool `swarm` sehingga Coordinator (`Neon` / `Argon`) dapat mengecek sisa kuota (`swarm(action="models")`), memanggil worker model spesifik (`add`), dan langsung mematikannya (`kill`) setelah 1 giliran.
> 3. **Bebas Polusi Konteks Tanpa `/compact` Manual**: Setiap worker yang dipanggil via `swarm(action="add")` otomatis lahir di ruang percakapan baru (**0% sampah history** ikut terkirim!).
> 4. **Rem Anti-Boros Orchestrator (*3-Tier Escalation*)**:
>    - *Catatan:* Model berlabel `Orchestrator` punya kecenderungan alami suka men-spawn worker. Untuk mencegah overhead token worker pada tugas sepele, protokol ini memasang **Rem Tier 1**:
>    - **Tier 1 (Bug 1–2 file jelas / edit rutin)** ➔ Coordinator (`Neon` / `Argon`) wajib selesaikan sendiri (**DILARANG spawn worker = 0% kuota Claude & 0 overhead worker**).
>    - **Tier 2 (Tugas multi-file / logika / arsitektur)** ➔ Coordinator otomatis spawn **maks 1 worker `Claude Sonnet (Low)`** (`brief` English `< 60 baris`, jawaban Claude `<= 35 baris` English diff/bullet) ➔ **langsung `kill`**.
>    - **Tier 3 (Buntu / Red-Team ekstrem)** ➔ Coordinator otomatis eskalasi ke **`Claude Sonnet (Medium)`** atau **`Claude Opus (High)`** (tetap 1 worker 1-turn + auto-`kill`).
> 5. **Mode Hemat & Fallback Otomatis Jika Kuota Claude Kritis (`<= 15%`) atau Limit**:
>    - **Fallback #1 (100% Native Antigravity — Pool Mingguan/Harian):** Jika `swarm(action="models")` menunjukkan kuota Claude `<= 15%` atau habis, Coordinator otomatis mengalihkan tugas worker Otak ke **`Gemini 4 Argon (High)` / `Orchestrator (Argon)`** (arsitektur/kontrak) atau **`Gemini 4 Hydrogen (High / XHigh)`** (bug pelik/rumus) — **0% memotong sisa kuota Claude!**
>    - **Fallback #2 (Ban Serep MCP):** Panggil `openrouter:tanya_openrouter(model="r1")` atau `model="claude"` / `:free`.
> 6. **Kapan Buka *New Conversation*?** Selama masih di **1 fitur / 1 kasus bug yang sama**, tidak perlu *New Conversation*. Buka *New Conversation* (atau `/compact` 1x) hanya saat **pindah ke fitur baru yang berbeda topik** agar Coordinator tetap ringan.
> 7. **Matikan MCP Berat Tak Terpakai**: Nonaktifkan MCP seperti `rea` (~160+ tools) saat coding harian agar tidak membayar pajak tetap ribuan token di setiap prompt.

#### 🎛️ Peta Peran Tim Otomatis di Dalam `/swarm` (3 Pool Kuota Terpisah)

| Peran di `/swarm` | Model & Pool Kuota | Tugas Spesifik & Batas Ketat |
| :--- | :--- | :--- |
| 🎼 **Coordinator Harian (Parkir Utama)** | 💡 **`Gemini 4 Neon (High)`** atau **`Orchestrator (Neon)`**<br>*(Pool 1 — Harian)* | Berinteraksi langsung dengan Anda (`ask_question`), menyelesaikan langsung tugas Tier 1 (1–2 file), menulis Spec/Tiket & kode utuh, menjalankan tes CLI & Triple-Gate, menyusun `brief` `< 60 baris` English, dan langsung me-`kill` worker. *(Pilih `Orchestrator (Neon)` jika ingin disiplin delegasi `/swarm` maksimal).* |
| 🛡️ **Coordinator Arsitektur Berat / Mode Hemat Claude** | 🛡️ **`Orchestrator (Argon)`** atau **`Gemini 4 Argon (High)`**<br>*(Pool 2 — Mingguan 7 Hari)* | **Fungsi Ganda:** (1) Dipilih di dropdown saat memimpin Tahap 2+3 multi-modul berat atau saat Pool 1 menurun; (2) Di-spawn otomatis oleh Coordinator Neon untuk `/modular-refactor` (`> 250 baris` + Facade Pattern) ATAU sebagai **Pengganti Utama Claude (Fallback #1)** saat kuota Claude `<= 15%` / limit. |
| ⚡ **Worker Scout** *(Opsional saat cari file luas)* | ⚡ **`Gemini 3.8 Flash (Medium)`**<br>*(Pool 1 — Harian)* | Mencari file lintas proyek & mengekstrak *Fact Packet* (`< 60 baris` English). **Dilarang `read_file` dump HTML/JSON/log mentah `> 5 KB`** (wajib 1-liner Python). |
| 🧠 **Worker Otak Harian** *(Default Tier 2 — 85%)* | 🧠 **`Claude Sonnet 5.5 (Low)`**<br>*(Pool 3 — Premium Claude)* | **1-Turn Only + Auto-`kill`!** Mengeluarkan *blindspots*, pertanyaan tajam `/grill-me`, validasi kontrak Spec/Caller, atau `[ROOT_CAUSE] + [CLI_CHECK] + [CODE_DIFF]` dalam **English Telegraphic `<= 35 baris`** (tanpa tulis ulang file utuh). |
| 👑 **Worker Otak Eskalasi** *(Tier 3 — 15% Buntu / Berat)* | 🧠 **`Claude Sonnet 5.5 (Medium)`** / 👑 **`Claude Opus 5.5 (High)`**<br>*(Pool 3 — Premium Claude)* | **Dilarang jadi Coordinator parkir!** Hanya di-spawn oleh Coordinator untuk **1 giliran (`<= 35 baris` English + auto-`kill`)** saat arsitektur sangat sistemik (4+ modul), Red-Team ekstrem, atau investigasi bug buntu. |
| 🔬 **Worker Deep-Bug Fallback** *(Saat Claude Limit)* | 🔬 **`Gemini 4 Hydrogen (High / XHigh)`**<br>*(Pool 1 — Harian)* | Di-spawn otomatis menggantikan `Claude Opus` pada investigasi bug misterius / algoritma rumit ketika kuota Pool 3 (Claude) sedang habis atau kritis (`<= 15%`). |

<details>
<summary>🌐 <b>(Ban Serep) OpenRouter MCP & Aider CLI — Hanya Jika Limit Antigravity Habis</b></summary>

* **OpenRouter MCP (`tanya_openrouter`)**: Coordinator otomatis memakai ini sebagai **Fallback #2** (`model="r1"`, `"claude"`, atau `"free-reason"`) jika kuota Claude bawaan limit dan dibutuhkan otak non-Gemini.
* **Aider CLI (`Rp 0` via `:free`)**: Untuk tiket tunggal hemat ekstrem di luar Antigravity, jalankan `aider` ➔ `/add <file>` (`cohere/north-mini-code:free`).
</details>

---

<a id="12-alur-utama-pembangunan--perombakan-fitur-3-tahap-terpadu"></a>
### 🚀 1.2 Alur Utama Pembangunan & Perombakan Fitur (2-Prompt Fast-Track di `/swarm`)

> **Alur 2-Prompt Otomatis (Dropdown di `Gemini 4 Neon High` / `Orchestrator Neon`, atau `Orchestrator Argon` / `Argon High`):**
> - **Prompt 1 (Tahap 1 — Konsultasi & `/grill-me`)**: Scout kode ➔ **Tembakan Claude #1** (*fatal flaws & pertanyaan tajam* ➔ auto-`kill`; otomatis dialihkan ke `Argon High` bila kuota Claude `<= 15%`/limit) ➔ Coordinator memandu `ask_question` interaktif & menulis **Draf Spesifikasi `.md`** + **Prompt Pengingat Siap-Salin**.
> - **Prompt 2 (Tahap 2+3 Gabung — 1x Jalan Tuntas!)**: Begitu Anda menyetujui draf, Coordinator melakukan **Tembakan Claude #2** (*validasi kontrak, caller, & test oracle* ➔ auto-`kill`), menulis `docs/specs/0XX_*.md` + `docs/INDEX.md` + `docs/tickets/0XX_*/`, lalu **langsung mengeksekusi seluruh tiket + Triple-Gate Verification** sampai kode lulus 100%!
>
> 💡 **Format Wajib Rujukan Raw di Kotak Pengingat Otomatis AI**:
> - File / Folder: `` `[nama_file.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/nama_file.md#L1-1)` `` *(URL-encode `:` ➔ `%3A`, spasi ➔ `%20`)*
> - Skill / Slash Command: `` `[swarm](slashCommand;swarm)` ``, `` `[/grill-me](slashCommand;grill-me)` ``, `` `[/to-spec](slashCommand;to-spec)` ``, `` `[/to-tickets](slashCommand;to-tickets)` ``, `` `[/ponytail](slashCommand;ponytail)` ``, `` `[/implement](slashCommand;implement)` ``

<a id="tahap-1-brainstorming-detail--tanya-jawab-grill-me---masuk-ke-draf-awal"></a>
#### 🔹 Tahap 1: Brainstorming Kritis & `/grill-me` ➔ Draf Spesifikasi `.md` (Prompt 1 dari 2)
*Pastikan dropdown berada di **`Gemini 4 Neon (High)` / `Orchestrator (Neon)`** (atau **`Orchestrator (Argon)` / `Gemini 4 Argon (High)`**), lalu tempel prompt ini:*

```markdown
[swarm](slashCommand;swarm) MODE KONSULTASI & BRAINSTORMING MURNI (COORDINATOR NEON/ARGON + TEMBAKAN OTAK #1).

Kondisi / Ide Fitur:
[Jelaskan fitur yang ingin dibuat / masalah yang ingin diselesaikan]

PROTOKOL ORKESTRASI /SWARM (0x GANTI DROPDOWN & REM KUOTA 3-POOL):
1. SCOUT FAKTA (COORDINATOR / WORKER FLASH):
   - Cari lokasi file relevan & baca hanya slice fungsi terkait (< 80 baris). DILARANG `read_file` dump HTML/JSON/log mentah (> 5 KB).
   - Susun ringkasan Fact Packet (< 60 baris English telegraphic).
2. TEMBAKAN OTAK #1 — DEVIL'S ADVOCATE (AUTO-KILL 1-TURN):
   - Cek kuota via `swarm(action="models")`: jika kuota Claude > 15%, spawn maks 1 worker `Claude Sonnet (Low)` (atau `Medium`/`Opus` bila arsitektur sangat berat). Jika kuota Claude <= 15% atau limit, OTOMATIS gunakan worker `Gemini 4 Argon (High)` / `Orchestrator (Argon)` (0% potong kuota Claude!).
   - Instruksikan worker menjawab <= 35 baris English padat: (a) 3-5 fatal flaws / blindspots / over-engineering, (b) 2-3 opsi pendekatan + trade-off, (c) daftar 3-5 pertanyaan `/grill-me` paling kritis.
   - WAJIB langsung `swarm(action="kill")` worker segera setelah 1 respons diterima!
3. SESI INTERAKTIF `/grill-me` (COORDINATOR — 0% CLAUDE):
   - Sajikan kritik Devil's Advocate & perbandingan opsi dalam Bahasa Indonesia (dilarang bersikap yes-man).
   - Jalankan [/grill-me](slashCommand;grill-me) satu pertanyaan per giliran via `ask_question` sampai konsensus tercapai.

REM PENGAMAN & PENGINGAT OTOMATIS (STRICT):
- DILARANG KERAS membuat atau mengedit file kodingan (.py) pada Tahap 1 ini.
- Setelah konsensus tercapai, simpan hasil ke DRAF SPESIFIKASI (.md).
- WAJIB cetak 2 kotak prompt siap-salin (format raw link file & skill, ganti path absolut URL-encoded):
  1. **Kotak Revisi Draf Awal (Opsional)** — untuk mengubah poin draf sebelum dieksekusi.
  2. **Prompt 2: Tahap 2+3 Gabung (1x Jalan Sampai Kode Lulus Tes)** — merujuk ke [nama_draf_spesifikasi.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/nama_draf_spesifikasi.md#L1-1) & [INDEX.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/INDEX.md#L1-1) (serta opsi singkat bila user ingin Tahap 2 Saja dulu).
- JANGAN mengeksekusi Tahap 2+3 sebelum saya menempel Prompt 2 dan menyetujuinya.
```

<details>
<summary>🔥 <b>(Varian Khusus) Mode Red-Team Ekstrem — Otomatis Eskalasi Worker <code>Claude Opus 5.5 (High)</code> 1-Turn</b></summary>

```markdown
[swarm](slashCommand;swarm) MODE RED-TEAM EKSTREM (COORDINATOR NEON/ARGON + WORKER CLAUDE OPUS 1-TURN).

Ide/Inovasi Saya: [Jelaskan ide/solusi yang ingin diuji secara brutal].

PROTOKOL:
1. Scout fakta kode & jalankan maks 1 one-liner probe empiris (`python -c "..."`) bila bergantung API/SDK eksternal, lalu rangkum < 60 baris English.
2. Spawn 1 worker `Claude Opus 5.5 (High)` (fallback `Gemini 4 Hydrogen (XHigh)` / `Orchestrator (Argon)` bila kuota Claude <= 15% atau limit) untuk menjawab <= 35 baris English: 5 alasan gagal total, 3 pertanyaan pembunuh ide, & 1 counter-thesis super sederhana (stdlib/Ponytail). Langsung `swarm(action="kill")` setelah 1 respons!
3. Terjemahkan kritik brutal ke Bahasa Indonesia, pandu `/grill-me` via `ask_question` tanpa menyentuh file `.py`, tulis Draf `.md`, dan cetak kotak prompt pengingat Revisi Draf & Tahap 2+3 Gabung (format raw).
```
</details>

<details>
<summary>🔄 <b>(Opsional) Kotak Revisi Draf Awal — 100% di Coordinator (0% Kuota Claude & 0 Worker)</b></summary>

```markdown
REM PENGAMAN AKTIF: DILARANG MENYENTUH FILE KODE (.py) & JANGAN SPAWN WORKER APA PUN.

Terkait draf [nama_draf_spesifikasi.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/nama_draf_spesifikasi.md#L1-1), tolong revisi bagian berikut:
1. [Bagian yang ingin diubah]: ubah menjadi [keinginan baru].
2. [Bagian yang ingin diperjelas]: jelaskan lebih sederhana.

Perbarui DRAF SPESIFIKASI (.md) saja, lalu perbarui kotak Prompt 2 (Tahap 2+3 Gabung) dalam format raw tanpa memulai kodingan dulu!
```
</details>

---

<a id="tahap-2-matangkanrombak-rancangan-ke-docsspecs--buat-tiket-ke-docstickets-1x-jalan"></a>
<a id="tahap-3-eksekusi-tiket-koding-implement--ponytail"></a>
#### 🔹 Tahap 2+3 Gabung (Jalur Utama 1x Jalan): Kunci Spec & Tiket ➔ Eksekusi Penuh & Triple-Gate (Prompt 2 dari 2)
*Gunakan langsung di sesi `/swarm` yang sama begitu Anda setuju dengan Draf Tahap 1 — **1 prompt langsung mengunci Spec/Tiket sekaligus mengeksekusi kode sampai lulus tes!***

```markdown
SETUJU dengan draf di [nama_draf_spesifikasi.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/nama_draf_spesifikasi.md#L1-1). Jalankan TAHAP 2+3 GABUNG (1x Jalan Penuh di [swarm](slashCommand;swarm) — Tembakan Otak #2 + Eksekusi Gemini):

MODIFIKASI TAMBAHAN (HAPUS BILA DRAF SUDAH 100% PAS):
- [Tulis penyesuaian kecil di sini]

FASE A — KUNCI KONTRAK, SPEC, & TIKET ([/to-spec](slashCommand;to-spec) + [/to-tickets](slashCommand;to-tickets)):
1. PRE-FLIGHT REALITY CHECK (COORDINATOR): Periksa signature fungsi, struktur data, & caller aktual (< 80 baris/baca) serta cek nomor 3-digit terakhir di [INDEX.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/INDEX.md#L1-1).
2. TEMBAKAN OTAK #2 — VALIDASI KONTRAK (AUTO-KILL 1-TURN):
   - Jika kuota Claude > 15%, spawn maks 1 worker `Claude Sonnet (Low)` (eskalasi `Medium` bila 3+ file lintas-modul). Jika kuota Claude <= 15% / limit (atau jika Coordinator saat ini sudah `Argon High` / `Orchestrator Argon` dan modifikasi <= 2 modul), validasi menggunakan `Gemini 4 Argon (High)` / `Orchestrator (Argon)` dengan `brief` Draf + signature aktual (< 60 baris English).
   - Minta output <= 35 baris English: daftar kontrak data/edge-case, zero-omission checklist (imports/callers), urutan DAG tiket, & one-liner smoke command tiap tiket.
   - WAJIB langsung `swarm(action="kill")` worker segera setelah 1 respons diterima!
3. MATERIALISASI DOKUMEN (COORDINATOR — 0% CLAUDE):
   - Patuhi [/ponytail](slashCommand;ponytail) (< 250 baris stdlib-first; > 250-300 baris wajib Facade Pattern).
   - Buat [0XX_nama_fitur.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/0XX_nama_fitur.md#L1-1), daftarkan ke [INDEX.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/INDEX.md#L1-1), dan pecah tiket berurutan ke [0XX_nama_fitur#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/tickets/0XX_nama_fitur#L1-1).

FASE B — EKSEKUSI OTOMATIS PENUH ([/implement](slashCommand;implement) — 100% GEMINI):
4. Langsung eksekusi SEMUA tiket (Tiket 1 -> Tiket N) tanpa berhenti meminta konfirmasi antar-tiket (spawn worker `Gemini 4 Argon (High)` / `Orchestrator (Argon)` bila Coordinator sedang di Neon dan ada tiket refactor > 250 baris / lintas 3+ modul).
5. Komentar & docstring wajib Bahasa Indonesia; jalankan **Triple-Gate Verification** setelah tiap tiket:
   - Gate 1 (Zero-Omission): Cocokkan semua import, parameter, return value, & caller terhadap checklist tiket.
   - Gate 2 (Syntax & Symbol): `python -m py_compile <file>` dan `python -m pyflakes <file>` (jika terpasang).
   - Gate 3 (Smoke Test): Jalankan one-liner smoke test (`python -c "..."` atau `pytest -q`) dengan edge-case (`None`/kosong).
6. Jika mentok 2x pada error arsitektural fatal, spawn 1x worker `Claude Sonnet (Medium)` / `Opus (High)` (<= 35 baris English, auto-`kill`; fallback `Hydrogen XHigh` / `Argon High` bila Claude <= 15% / limit), lalu selesaikan.
7. Setelah SEMUA tiket lulus Triple-Gate, berikan **1 ringkasan final padat dalam Bahasa Indonesia**.
```

<details>
<summary>🛡️ <b>(Opsi Terpisah — Khusus Fitur Super Sensitif) Jalankan Tahap 2 Saja Dulu agar Bisa Tinjau Tiket Sebelum Koding</b></summary>

```markdown
SETUJU dengan draf di [nama_draf_spesifikasi.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/nama_draf_spesifikasi.md#L1-1). Jalankan TAHAP 2 SAJA DULU ([/to-spec](slashCommand;to-spec) + [/to-tickets](slashCommand;to-tickets)) di [swarm](slashCommand;swarm) — BERHENTI SEBELUM KODING:
1. Lakukan Pre-Flight Reality Check + Tembakan Otak #2 (1x worker `Claude Sonnet Low/Medium`, <= 35 baris English, auto-`kill`; fallback `Argon High` / `Orchestrator Argon` bila kuota Claude <= 15% atau limit).
2. Buat [0XX_nama_fitur.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/0XX_nama_fitur.md#L1-1), update [INDEX.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/INDEX.md#L1-1), dan tulis seluruh tiket di [0XX_nama_fitur#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/tickets/0XX_nama_fitur#L1-1) dengan kontrak data, daftar caller, & smoke command.
3. JANGAN ubah file `.py` dulu! Tampilkan ringkasan daftar tiket + cetak kotak prompt pengingat siap-salin untuk mengeksekusi [/implement](slashCommand;implement) Tiket 1..N (format raw).
```
</details>

---

<a id="alur-pasca-implementasi-modifikasi--penambahan-fitur-lanjutan-hemat-token"></a>
#### 🔹 Alur Pasca-Implementasi: Modifikasi & Fitur Lanjutan (1 Prompt Langsung di `/swarm`)
*Gunakan jika fitur sudah selesai diimplementasikan namun Anda ingin menambah/mengubah perilaku. Jika modifikasi hanya 1–2 file dan sudah jelas, Coordinator (`Neon` / `Argon`) mengerjakannya langsung (**0% kuota Claude & 0 worker**):*

```markdown
[swarm](slashCommand;swarm) [/to-spec](slashCommand;to-spec) Perbarui [spec_terkait.md#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/specs/spec_terkait.md#L1-1), tambahkan tiket lanjutan ke [folder_tiket#L1-1](fileLineRange;file:///d%3A/path/proyek/docs/tickets/folder_tiket#L1-1), lalu langsung eksekusi [/implement](slashCommand;implement) sampai lulus Triple-Gate:

MODIFIKASI YANG DIINGINKAN:
1. [Jelaskan perubahan / fitur tambahan secara spesifik]

ATURAN:
- Jika menyentuh 1-2 file jelas (Tier 1): Coordinator (`Neon` / `Argon`) kerjakan langsung sendiri (DILARANG spawn worker = 0% Claude).
- Jika lintas 3+ modul / kompleks (Tier 2): spawn 1x worker `Claude Sonnet (Low)` untuk validasi kontrak (<= 35 baris English, auto-`kill`; fallback `Argon High` bila kuota Claude <= 15% / limit) sebelum Coordinator mengeksekusi kode.
- Patuhi [/ponytail](slashCommand;ponytail), jalankan Triple-Gate (`Zero-Omission` + `py_compile`/`pyflakes` + smoke test), & laporkan 1 ringkasan akhir Bahasa Indonesia.
```

---

<a id="13-tiga-prompt-spesialis-ringkas-di-luar-bikin-fitur-baru"></a>
### 🛠️ 1.3 Tiga Prompt Spesialis Ringkas (Semua 1-Prompt Otomatis di `/swarm` — Dual-Orchestrator `Neon` / `Argon`)

#### 🐞 Kasus A: Mengatasi Error Run / Bug Saat Aplikasi Dijalankan (1-Prompt Otomatis 3-Tier)
*Cukup tempel 1 prompt ini di Coordinator (`Gemini 4 Neon High` / `Orchestrator Neon` / `Orchestrator Argon`). Coordinator otomatis menentukan apakah cukup dibereskan sendiri (**0% Claude**) atau perlu memanggil 1x worker di ruang konteks bersih:*

```markdown
[swarm](slashCommand;swarm) [/diagnosing-bugs](slashCommand;diagnosing-bugs) Investigasi & perbaiki bug ini dengan Protokol Otomatis 3-Tier:

GEJALA / TRACEBACK / KELUHAN BUG:
[PASTE PESAN ERROR / TRACEBACK / KELUHAN BUG DI SINI]

PROTOKOL EKSEKUSI OTOMATIS (COORDINATOR NEON / ARGON):
1. SCOUT FAKTA (ANTI-POLUSI):
   - Cari lokasi `file:line`, baca slice relevan (< 80 baris), & jalankan maks 1-2 probe CLI read-only.
   - DILARANG `read_file` pada file HTML/JSON/log/dump mentah (> 5 KB) — wajib ekstrak ringkas lewat 1-liner Python (`len`, `<title>`, <= 5 baris sampel).
2. ESKALASI 3-TIER MANDIRI (ZERO INTERRUPTION & REM KUOTA):
   - **Tier 1 (Bug 1-2 file jelas):** Langsung perbaiki & verifikasi sendiri oleh Coordinator (DILARANG spawn worker = 0% kuota Claude).
   - **Tier 2 (Bug logika / multi-file):** Susun Fact Packet (< 60 baris English), spawn 1x worker `Claude Sonnet (Low)` -> minta `<= 35 baris` English (`[ROOT_CAUSE]`, `[CLI_CHECK]`, `[CODE_DIFF]` tanpa tulis ulang file utuh) -> langsung `swarm(action="kill")`.
   - **Tier 3 (Bug buntu / ekstrem):** Otomatis eskalasi ke 1x worker `Claude Sonnet (Medium)` atau `Claude Opus (High)` (auto-`kill`).
   - **Mode Hemat / Fallback Limit Claude (`<= 15%`):** Otomatis alihkan worker ke `Gemini 4 Hydrogen (High/XHigh)` atau `Gemini 4 Argon (High)` / `Orchestrator (Argon)` (atau MCP `openrouter:tanya_openrouter` bila perlu).
3. EKSEKUSI & VERIFIKASI (COORDINATOR):
   - Kembangkan diff menjadi kode utuh (komentar/docstring Indonesia, 0 import/caller terlewat).
   - Jalankan `python -m py_compile <file>`, `python -m pyflakes <file>` (jika terpasang), dan seluruh tes verifikasi CLI sampai lulus 100%.
   - Laporkan akar masalah, perubahan, & hasil tes secara ringkas dalam **Bahasa Indonesia**.
```

---

#### ✂️ Kasus B: Menyederhanakan Kode Ribet (`/ponytail`) & Hapus Fungsi Mati (*Dead Code*)
```markdown
[swarm](slashCommand;swarm) [/code-review](slashCommand;code-review) Audit [file_target.py#L1-1](fileLineRange;file:///d%3A/path/proyek/src/file_target.py#L1-1) dengan aturan [/ponytail](slashCommand;ponytail) ultra & [/graphify](slashCommand;graphify):
1. Coordinator (atau worker `Gemini Flash`) memindai seluruh fungsi mati (zero callers) dan kode bertele-tele di target, lalu meringkas temuan (< 60 baris English).
2. Spawn 1x worker `Claude Sonnet (Low)` (fallback `Argon High` / `Orchestrator Argon` bila kuota Claude <= 15% atau limit) untuk menyusun tabel pemangkasan stdlib-first & smoke test checklist (`<= 35 baris` English) -> langsung `swarm(action="kill")`.
3. Tampilkan tabel temuan dalam Bahasa Indonesia untuk persetujuan saya — JANGAN hapus/ubah kode sebelum saya setujui. Begitu saya ketik "SETUJU", Coordinator langsung mengeksekusi pemangkasan & memverifikasi `py_compile`, `pyflakes`, serta smoke test.
```

---

#### 🔬 Kasus C: Mode Otak-Tangan Ilmiah (Bug Misterius / *Race Condition* / SDK Eksternal — Loop Otomatis Hingga 4 Putaran)
*Tidak perlu bolak-balik ganti dropdown antar putaran! Coordinator otomatis menjalankan siklus eksperimen ilmiah hingga tuntas (maks 4 putaran):*

```markdown
[swarm](slashCommand;swarm) [/diagnosing-bugs](slashCommand;diagnosing-bugs) MODE OTAK-TANGAN ILMIAH OTOMATIS (COORDINATOR NEON/ARGON + WORKER OTAK 1-TURN/PUTARAN).

DESKRIPSI MASALAH MISTERIUS:
[Jelaskan perilaku aneh, race condition, desinkronisasi, atau error SDK di sini]

SIKLUS EKSPERIMEN ILMIAH OTOMATIS (MAKS 4 PUTARAN):
1. Coordinator lakukan observasi awal + maks 1-2 probe reproduksi CLI (dilarang `read_file` dump > 5 KB) -> susun Evidence Packet (< 60 baris English).
2. Spawn 1x worker Otak (Putaran 1: `Claude Sonnet Low`; Putaran 2+: eskalasi `Claude Sonnet Medium` / `Opus High`; Fallback otomatis bila kuota Claude <= 15% atau limit: `Gemini 4 Hydrogen XHigh` / `Argon High`, atau MCP `openrouter:tanya_openrouter`).
   - Minta worker menjawab <= 35 baris English: `[HYPOTHESES]` (#1/#2), `[CLI_EXPERIMENTS]` (1-2 perintah pembuktian definitif), & `[CODE_DIFF]` (diterapkan HANYA bila #1 terbukti).
   - WAJIB langsung `swarm(action="kill")` worker Otak setelah 1 respons!
3. Coordinator eksekusi `[CLI_EXPERIMENTS]` di terminal:
   - **Jika terbukti (`[STATUS: SELESAI]`):** Terapkan `[CODE_DIFF]` utuh, jalankan `py_compile` + `pyflakes` + tes ulang sampai lulus 100%, lalu laporkan akar masalah & `[PELAJARAN_KUNCI]` (2-3 poin) dalam **Bahasa Indonesia**.
   - **Jika terbantahkan:** JANGAN patch spekulatif — kemas bukti baru (< 45 baris English) dan lanjutkan putaran berikutnya (maks 4 putaran; jika masih buntu setelah putaran 4, berhenti dan laporkan seluruh temuan ke saya).
```

<details>
<summary>🛟 <b>(Ban Serep Tanpa `/swarm`) Mode Otak-Tangan via OpenRouter MCP</b></summary>

```markdown
Selesaikan investigasi bug ini via Pola Otak-Tangan MCP (`openrouter:tanya_openrouter` model="claude" atau "r1", `mode_debug=True`, session_id unik, maks 4 putaran):
DESKRIPSI MASALAH: [Paste error/perilaku aneh di sini]
ALUR: Kirim Evidence Packet padat (< 60 baris English) ke `tanya_openrouter` -> eksekusi `[PERINTAH_TES]` di terminal -> kirim hasil kembali sampai `[STATUS: SELESAI]` -> terapkan kode utuh + `py_compile`/`pyflakes` + ringkas dalam Bahasa Indonesia.
```
</details>

---

<a id="14-tiga-golden-rules-anti-blunder"></a>
### 🛡️ 1.4 Empat "Golden Rules" Anti-Blunder & Hemat Kuota 3-Pool

1. **Paham Dulu Baru Eksekusi**: Selalu mulai fitur baru dari **Tahap 1 (Brainstorming & `/grill-me`)** dengan rem pengaman aktif sampai Anda benar-benar sepakat pada Draf Spesifikasi `.md`.
2. **Aturan Ambang 250 Baris (`/ponytail` vs Clean Architecture)**: Selama file masih **< 250 baris**, tulis kode sesingkat mungkin di file yang ada tanpa membuat class/file baru. Pemecahan file (`/modular-refactor` + *Facade Pattern*) baru dilakukan saat file menyentuh **250–300 baris**.
3. **Disiplin `/swarm` Dual-Orchestrator & Proteksi 3 Pool Kuota**:
   - Parkir dropdown harian di **`Gemini 4 Neon (High)` / `Orchestrator (Neon)`** (Pool 1 Harian), atau gunakan **`Orchestrator (Argon)` / `Gemini 4 Argon (High)`** (Pool 2 Mingguan) saat memimpin refactor berat / menghemat Claude. **Dilarang keras memarkir `Claude Opus` sebagai Coordinator dropdown!**
   - Tugas Tier 1 (1–2 file jelas) wajib dibereskan langsung oleh Coordinator tanpa men-spawn worker (**0% Claude & 0 overhead worker**).
   - Saat butuh worker Otak (Tembakan #1/#2 atau bug multi-file/buntu), kirim `brief` **English `< 60 baris`**, batasi jawaban **`<= 35 baris` English**, dan **langsung `swarm(action="kill")`** setelah 1 giliran (otomatis alihkan ke `Argon High` / `Orchestrator Argon` / `Hydrogen XHigh` bila kuota Claude `<= 15%` atau limit).
4. **Anti-Sycophancy (Wajib Menantang Ide / Devil's Advocate)**: AI dilarang menjadi *cheerleader* atau *yes-man* yang langsung memuji ide baru. Dalam perencanaan fitur (Tahap 1), AI wajib menguji asumsi, menunjukkan potensi cacat fatal, risiko *over-engineering*, dan blindspot sebelum menyepakati spesifikasi.

---

## 2. Docstring Translator Bilingual

Modul `docstring_translator.py` membaca berkas Python secara otomatis menggunakan **Python AST (Abstract Syntax Tree)** untuk menerjemahkan penjelasan alur fungsi dan logika dari Bahasa Indonesia (`[ID]`) ke padanan Bahasa Inggris (`[EN]`) tanpa mengubah indentasi atau logika kode asli.

Modul ini **100% menggunakan pustaka standar Python (`urllib.request`)** sehingga tidak memerlukan instalasi dependensi luar (`requests`).

### 🚀 Perintah CLI Cepat:
```powershell
# Terjemahkan seluruh berkas .py di proyek saat ini (otomatis fallback Gemini -> OpenRouter)
python vibe_tools/docstring_translator.py .

# Pratinjau tanpa mengubah berkas fisik
python vibe_tools/docstring_translator.py --dry-run .
```

### 🤖 Otomasi Otomatis via GitHub Actions:
Workflow `.github/workflows/bilingual_sync.yml` sudah tersedia di dalam repositori. Cukup tambahkan `GEMINI_API_KEY` pada **Settings > Secrets and variables > Actions** di GitHub. Setiap kali ada commit baru, docstring baru otomatis diterjemahkan.

---

## 3. Sinkronisasi Git vibe_tools (Pindah PC ⇄ Laptop, Pengguna Publik, & Fork Global)

Direktori `vibe_tools/` dirancang sebagai modul universal portabel yang dapat dipakai di berbagai proyek dan sinkron lintas komputer.

<a id="31-skenario-pindah-pc--laptop-anti-bentrok"></a>
### 🔄 3.1 Skenario Pindah PC ⇄ Laptop Anti-Bentrok

Jika Anda sering berpindah antara PC utama dan Laptop, gunakan langkah berikut agar perubahan lokal di kedua perangkat **tidak saling menimpa atau hilang**:

1. **Di Perangkat Pertama (Sebelum Berpindah)**:
   Dorong pembaruan lokal Anda ke repositori GitHub:
   ```powershell
   python vibe_tools/push_to_github.py
   ```
2. **Di Perangkat Kedua (Saat Membuka Proyek)**:
   Jika perangkat kedua juga memiliki editan lokal, gunakan perintah *rebase with autostash*:
   ```powershell
   git -C vibe_tools pull --rebase --autostash origin main
   ```
   > [!TIP]
   > Flag `--autostash` otomatis mengamankan perubahan lokal Anda ke memori sementara, menarik pembaruan terbaru dari GitHub, lalu mengembalikan editan lokal Anda di atasnya secara rapi tanpa konflik!

3. **Kunci Pointer di Repositori Utama**:
   ```powershell
   git add vibe_tools
   git commit -m "chore: perbarui pointer commit vibe_tools lintas perangkat"
   ```

<a id="32-panduan-cepat-untuk-pengguna-publik-baru-1-menit"></a>
### 📦 3.2 Panduan Cepat untuk Pengguna Publik Baru (1 Menit)

Untuk menggunakan `vibe_tools` di proyek Python baru (`my-awesome-app`):
```powershell
# 1. Masuk ke folder proyek Anda
cd my-awesome-app

# 2. Tambahkan vibe_tools sebagai Git Submodule
git submodule add https://github.com/vibe-ecosystem/vibe-tools.git vibe_tools

# 3. Jalankan setup otomatis satu klik
python vibe_tools/setup_vibe_ecosystem.py
```
Seluruh aturan `.agents`, skills universal, dan template konfigurasi Aider langsung aktif seketika!

<a id="33-panduan-fork--pull-request-untuk-kontributor-global"></a>
### 🤝 3.3 Panduan Fork & Pull Request untuk Kontributor Global

Bagi pengembang global yang ingin berkontribusi menyempurnakan `vibe_tools`:
1. Klik tombol **Fork** di pojok kanan atas repositori [https://github.com/vibe-ecosystem/vibe-tools](https://github.com/vibe-ecosystem/vibe-tools).
2. Clone fork ke komputer Anda:
   ```bash
   git clone https://github.com/username-anda/vibe-tools.git
   cd vibe-tools
   git checkout -b feat/fitur-baru-keren
   ```
3. Lakukan modifikasi, pastikan kode mematuhi batas `< 250 baris`, lulus verifikasi sintaks:
   ```powershell
   python -m py_compile <file_yang_diubah>
   ```
4. Push dan buat **Pull Request**:
   ```bash
   git add .
   git commit -m "feat: tambahkan fitur xyz"
   git push origin feat/fitur-baru-keren
   ```

---

## 4. REA MCP: Reverse Engineer Anything

REA (*Reverse Engineer Anything*) adalah MCP server berbasis Node.js yang memberikan kemampuan **analisis binary mendalam** (PE, ELF, APK, Mach-O, firmware, dan web bundles).

### ⚡ Instalasi Cepat:
```powershell
# Status saklar MCP (Dual-Cockpit)
python vibe_tools/rea_tool.py --status

# Nonaktifkan REA MCP (DEFAULT - Menghemat ~25.000 token per pesan)
python vibe_tools/rea_tool.py --disable

# Aktifkan hanya saat butuh reverse engineering biner
python vibe_tools/rea_tool.py --enable
```

---

## 5. Hermes Agent x Antigravity IDE x Aider CLI & Self-Learning Universal

<a id="51-sinergi-3-alat-antigravity-aider-cli--hermes-agent"></a>
### 🌐 5.1 Sinergi 3 Alat: Antigravity, Aider CLI, & Hermes Agent

Ekosistem menggabungkan kekuatan tiga pilar AI:
1. **Antigravity IDE (Utama)**: Arsitek sistem dengan jendela konteks raksasa (1M–2M token) untuk perencanaan besar, `/grill-me`, spesifikasi, audit, dan eksekusi harian.
2. **Aider CLI (Cadangan On-Demand `:free`)**: Asisten terminal ringan berbasis Tree-sitter RepoMap (`map-tokens: 1024`) dan edit diff minimal (`auto-commits: false`), siap dipakai kapan saja untuk refactor atau saat kuota IDE menipis.
3. **Hermes Agent**: Background worker mandiri otonom berbasis CLI (default model gratis cepat + fallback `deepseek-chat`) yang menangani investigasi mendalam dan menyimpan memori jangka panjang.

<a id="52-metode-pemasangan-cepat-mandiri-1-menit"></a>
### 🚀 5.2 Metode Pemasangan Cepat Mandiri (1 Menit)

Jalankan installer otomatis yang telah dirampingkan:
```powershell
python vibe_tools/install_hermes_antigravity.py
```
Skrip akan mengunduh Hermes Agent, memasang dependensi, menyalin bridge `hermes_mcp.py` ke `~/.gemini/`, dan mendaftarkannya ke `mcp_config.json`.

<a id="53-pemasangan-manual-langkah-demi-langkah"></a>
### 🛠️ 5.3 Pemasangan Manual Langkah Demi Langkah
1. Clone repositori: `git clone https://github.com/NousResearch/hermes-agent.git C:/hermes_env/hermes-agent`
2. Install paket: `pip install -e C:/hermes_env/hermes-agent`
3. Atur model default di terminal:
   ```cmd
   hermes config set model "deepseek/deepseek-chat"
   ```
4. Salin `vibe_tools/hermes_mcp.py` ke `%USERPROFILE%/.gemini/hermes_mcp.py`.
5. Daftarkan di `%USERPROFILE%/.gemini/config/mcp_config.json`.

<a id="54-self-learning-universal-lintas-proyek"></a>
### 🧠 5.4 Self-Learning Universal Lintas-Proyek

Hermes Agent memiliki keunggulan **Self-Learning** yang dapat mengingat pelajaran arsitektur dan kesalahan koding secara permanen di `%USERPROFILE%/.hermes/memories/MEMORY.md`.

Setiap kali Anda menyelesaikan sesi diskusi atau refaktor besar, perintahkan AI untuk menyimpannya ke memori universal:

```markdown
Tolong delegasikan ke Hermes Agent:
"Pelajari hasil percakapan dan konsensus arsitektur hari ini. Catat aturan, batasan Ponytail, dan pola terbaik ke memori jangka panjang universal (~/.hermes/memories/MEMORY.md) agar otomatis aktif dan diingat pada seluruh sesi vibe coding di proyek mana pun."
```
Dengan cara ini, ilmu dan best-practice yang dipelajari pada satu proyek otomatis diterapkan di proyek-proyek Anda berikutnya!

---

## 6. Tutorial Setup PC/Laptop Baru dari Nol (Fresh Install Windows 10/11) & OpenRouter MCP

<a id="61-tahap-1-persiapan-dasar-windows-1011-baru"></a>
### 💻 6.1 Tahap 1: Persiapan Dasar Windows 10/11 Baru
1. Pasang **Git for Windows** dari [git-scm.com](https://git-scm.com).
2. Pasang **Python 3.11+** dari [python.org](https://python.org).
   > [!IMPORTANT]
   > Pada layar pertama installer Python, **WAJIB CENTANG kotak "Add python.exe to PATH"**!

<a id="62-tahap-2-persiapan-akun--saldo-ai"></a>
### 💳 6.2 Tahap 2: Persiapan Akun & Saldo AI
1. **Google AI Studio / Gemini Plus / Advanced**: Siapkan akun Google Anda.
2. **OpenRouter**: Daftar di [openrouter.ai](https://openrouter.ai), buat API Key di menu *Keys*, lalu lakukan top-up saldo minimal **\$5.00** (cukup untuk ribuan sesi koding hemat).

<a id="63-tahap-3-instalasi-aider-terisolasi--auto-approve-antigravity"></a>
### ⚙️ 6.3 Tahap 3: Instalasi Aider Terisolasi & Auto-Approve Antigravity
Agar AI dapat mengeksekusi rangkaian tiket secara mandiri:
* **Antigravity IDE**: Masuk ke Settings / Preferences -> Cari "Terminal Approval" -> Setel ke Auto-Approve untuk sandboxed commands.
* **Aider CLI Terisolasi (On-Demand Free Tier)**:
  1. Jalankan 1 perintah universal dari folder proyek Anda:
     ```powershell
     python vibe_tools/setup_aider_hybrid.py
     ```
  2. Skrip otomatis memasang `aider` via `aider-install` (`uv` virtual environment terisolasi di `~/.local/bin`, tidak mencemari Python global proyek) serta menyalin template `.aider.conf.yml`, `.aiderignore`, dan `CONVENTIONS.md` dengan `auto-commits: false`.
  3. Untuk menguji daftar model `:free` tercepat yang lolos format diff secara live sebelum ngoding, jalankan:
     ```powershell
     python vibe_tools/free_model_bench.py --maks 14
     ```

<a id="64-tahap-4-prompt-setup-mandiri--alternatif-manual"></a>
### 🚀 6.4 Tahap 4: Prompt Setup Mandiri & Alternatif Manual

#### Opsi 1: Satu Prompt Otomatis di Chat Antigravity
Salin prompt berikut dan kirim ke chat Antigravity IDE:
```markdown
Halo Antigravity, tolong bantu pasang dan konfigurasikan OpenRouter MCP Server di laptop ini secara global:
1. Pastikan folder ~/.gemini dan ~/.gemini/config/ sudah ada.
2. Pasang dependensi: python -m pip install -q mcp.
3. Salin vibe_tools/openrouter_mcp.py ke ~/.gemini/openrouter_mcp.py.
4. Buat ~/.gemini/openrouter_key.txt dan masukkan OpenRouter API Key saya.
5. Daftarkan server openrouter ke ~/.gemini/config/mcp_config.json.
```

#### Opsi 2: Eksekusi Skrip Mandiri via Terminal
```powershell
python vibe_tools/install_openrouter_mcp.py
```

<a id="65-tahap-5-verifikasi--uji-koneksi"></a>
### 🔍 6.5 Tahap 5: Verifikasi & Uji Koneksi
Ketikkan di chat:
> *"Tolong jalankan tool `cek_koneksi_openrouter` untuk memvalidasi API Key dan saldo OpenRouter saya."*

<a id="66-tahap-6-katalog-model-pilihan--update-otomatis"></a>
### 🏆 6.6 Tahap 6: Katalog Model Pilihan & Update Otomatis

Server MCP OpenRouter mendukung **Sistem Alias Cerdas**:

| Kategori | Alias Cepat | Model ID Resmi | Kasus Rekomendasi |
| :--- | :---: | :--- | :--- |
| 👑 **Standar Emas Coding** | **`claude`** / **`sonnet`** | `anthropic/claude-sonnet-4.6` | Arsitektur Python, debugging terarah, & *Devil's Advocate* |
| 🏛️ **Flagship Kompleks** | **`opus`** | `anthropic/claude-opus-4.6` | Investigasi bug sistemik & arsitektur lintas-modul rumit |
| 🛠️ **Spesialis Engineering** | **`codex`** / **`gpt5`** | `openai/gpt-5-codex` | Rekayasa perangkat lunak presisi, kontrak data, & *clean code* |
| 🧠 **Penalaran (Reasoning)** | **`r1`** | `deepseek/deepseek-r1-0528` | Logika rumit, algoritma matematika, & pembuktian alur data |
| ⚡ **Harian Gesit & Super Hemat** | **`deepseek`** / **`v3`** | `deepseek/deepseek-v3.2` | Rekomendasi harian utama (DSA) & diskusi eksplorasi super hemat |
| 💻 **Spesialis Kode Open-Weight** | **`qwen`** / **`qwen3`** | `qwen/qwen3-coder` | Cepat & efisien untuk Python/JS (MoE) |
| 🚀 **Thinker Ringan** | **`haiku`** | `anthropic/claude-haiku-4.5` | Cepat & cerdas untuk tugas pembantu |
| 🎁 **100% Gratis (Auto-Fallback)** | **`free`** / **`free-code`** / **`free-fast`** / **`free-reason`** | `cohere/north-mini-code:free` / `baidu/ernie-5.5-flash-preview:free` / `nvidia/nemotron-3-ultra-550b-a55b:free` | Eksperimen koding, tugas cepat, & penalaran bebas biaya (\$0.00) |

> [!TIP]
> Untuk mengecek daftar model dan harga terbaru langsung dari OpenRouter secara otomatis, ketik:  
> *"Panggil tool `daftar_model_rekomendasi`."*

<a id="67-mode-otak-tangan-iterative-debug-loop--session-cache"></a>
### 🧠 6.7 Mode Otak-Tangan (Iterative Debug Loop & Session Cache)

Server MCP OpenRouter mendukung siklus **Scientific Debugging Loop** menggunakan parameter baru pada `tanya_openrouter`:
* `session_id: str`: Menyimpan memori sesi ringan berbasis *Sliding Window* (maksimal 4 putaran terakhir = 8 pesan) di `~/.gemini/cache/openrouter_sessions.json`.
  * Awali dengan `new:<id>` atau `reset:<id>` untuk membersihkan riwayat lama sebelum memulai investigasi baru.
* `mode_debug: bool = True`: Menyuntikkan protokol tag terstruktur wajib bagi Claude:
  * `[HIPOTESIS]`: Dugaan teknis penyebab bug yang sedang diuji saat ini.
  * `[PERINTAH_TES]`: Perintah CLI / pytest / python minimal untuk dieksekusi Gemini di terminal IDE.
  * `[STATUS]`: `LANJUT_TES` (masih butuh pengujian) atau `SELESAI` (akar masalah terbukti pasti).
  * `[SOLUSI_KODE]`: Instruksi perbaikan presisi saat status `SELESAI`.
  * `[PELAJARAN_KUNCI]`: Rangkuman 1–2 kalimat akar masalah & pencegahannya untuk *self-learning*.

> 💰 **Keuntungan Token & Biaya:** Gemini Flash menjalankan seluruh uji coba terminal, kompilasi sintaks, dan inspeksi berkas lokal secara **gratis** ($0), sedangkan Claude hanya menerima ringkasan hasil tes padat (< 2.500 token), menghemat biaya API hingga **> 90%** dan menjaga batas harian `$1.00/hari` tetap aman.

---

## 7. Katalog 15 Skill Universal & Panduan Penggunaan

Folder `vibe_tools/skills` terhubung secara global ke `~/.gemini/config/skills` melalui Windows NTFS Junction (`sync_universal.py`).

| Perintah | Deskripsi Singkat | Contoh Prompt Universal |
| :--- | :--- | :--- |
| **`/ask-matt`** | Router penunjuk jalan rekayasa perangkat lunak | `"/ask-matt apa langkah terbaik untuk fitur ini?"` |
| **`/grill-me`** | Interview arsitektur interaktif satu per satu | `"/grill-me interogasi rancangan modul data cache"` |
| **`/grill-with-docs`** | Domain glossary & Architectural Decision Records (ADR) | `"/grill-with-docs buat ADR untuk pemilihan database"` |
| **`/to-spec`** | Formalisasi spesifikasi teknis modular (< 300 baris) | `"/to-spec buat spec teknis modul auth"` |
| **`/to-tickets`** | Pemecah spesifikasi jadi tiket terurut | `"/to-tickets pecah spec menjadi tiket terurut"` |
| **`/implement`** | Eksekusi tiket disiplin berurutan | `"/implement kerjakan tiket nomor 1"` |
| **`/tdd`** | Siklus Red-Green-Refactor berbasis pytest | `"/tdd buat fungsi hitung durasi dengan pytest"` |
| **`/diagnosing-bugs`**| Pelacak bug via reproduksi tes gagal terlebih dahulu | `"/diagnosing-bugs telusuri penyebab KeyError di line 40"` |
| **`/code-review`** | Audit kepatuhan 3-sumbu (<300 baris, tiket, & Ponytail) | `"/code-review audit perubahan pada src/app.py"` |
| **`/ponytail`** | Anti-over-engineering 7 tangga & stdlib-first (lite/full/ultra) | `"/ponytail sederhanakan kode agar pakai stdlib Python"` |
| **`/modular-refactor`**| Pemecah script monolitik (>300 baris) tanpa regresi | `"/modular-refactor pecah src/processor.py"` |
| **`/unit-test-generator`**| Generator tes isolasi mock fixtures | `"/unit-test-generator buat tes untuk src/api_client.py"` |
| **`/graphify`** | Peta dependensi kode AST & GraphRAG lokal | `"/graphify petakan dependensi fungsi di folder src"` |
| **`/handoff`** | Kompresi konteks percakapan untuk ganti chat/model | `"/handoff rangkum sesi kerja ini ke dokumen handoff"` |
| **`/retro`** | Retrospeksi & penyempurnaan rules guardrails | `"/retro evaluasi proses pengerjaan fitur tadi"` |

📖 Panduan detail setiap skill tersedia di: [**`vibe_tools/skills/README.md`**](skills/README.md).

---

## 8. Arsitektur Hybrid Antigravity + Aider On-Demand (`:free` First) + Sinergi Hardware Lokal

Arsitektur hybrid menggabungkan kepraktisan IDE dengan eksekutor CLI ultra-hemat:
- **Utama (Antigravity IDE)**: Perencanaan arsitektur, wawancara `/grill-me`, `/to-spec`, debugging Otak-Tangan, dan coding harian tanpa overhead per-token OpenRouter.
- **Cadangan On-Demand (Aider CLI)**: Siap dipanggil kapan saja dari terminal (`aider`), dengan konteks ramping (`map-tokens: 1024`, `subtree-only: true`, `/add` manual), proteksi rahasia via `.aiderignore`, `auto-commits: false`, serta rute model 4-State:
  1. **Cloud `:free` Utama** (`cohere/north-mini-code:free`) — cepat, non-reasoning, Rp 0.
  2. **Cloud `:free` Cadangan** (`baidu/ernie-5.5-flash-preview:free`, `inclusionai/ling-3.2-flash:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`).
  3. **Opsional GPU Lokal CUDA (misal RTX 3060 6GB + iGPU Display Offload)**: Jika Ollama terpasang, **jangan menggabungkan dGPU + iGPU (*Split-GPU*) untuk 1 LLM** karena RAM sistem memperlambat CUDA. Biarkan iGPU merender layar/IDE agar VRAM dGPU utuh, lalu manfaatkan dGPU untuk *offload* `weak-model` (`qwen2.5-coder:3b`) atau fallback anti-429 (`qwen2.5-coder:7b-instruct-q4_K_M`) dengan **`OLLAMA_KEEP_ALIVE=5m`** agar VRAM kembali bersih untuk rendering/AI lain.
  4. **Fallback Berbayar Murah**: `/model openrouter/deepseek/deepseek-v3.2` saat tugas kompleks atau `:free` sedang sibuk.

---

## 9. Otomasi Pemeliharaan, Sinkronisasi Database, & Universal Updater Lintas-Proyek

Ekosistem menyediakan perangkat otomatis untuk sinkronisasi pembaruan, ekstraksi riwayat database percakapan, dan saklar hemat token.

### 🚀 9.1 Universal Updater Lintas-Proyek (`update_ecosystem.py`)
```powershell
# Cek perbedaan berkas tanpa mengubah disk (Dry-Run)
python vibe_tools/update_ecosystem.py --check

# Dorong ekosistem dari master lokal ke proyek lain (< 2 detik, offline)
python vibe_tools/update_ecosystem.py --target "D:/Path/Ke/ProjectLain"

# Pulihkan kondisi ke sebelum update jika diperlukan (Rollback)
python vibe_tools/update_ecosystem.py --rollback
```

### 🧠 9.2 Ekstraksi Riwayat Percakapan Database (`doc_db_extractor.py`)
Mengekstrak intisari percakapan nyata dari database Antigravity IDE (`monitor/monitor_cache.db`):
```powershell
# Ekstrak percakapan 2 hari terakhir (kemarin & hari ini) ke scratch/recent_db_knowledge.md
python vibe_tools/doc_db_extractor.py 2
```

### 🔧 9.3 Saklar Toggle REA MCP (`rea_tool.py`)
```powershell
# Nonaktifkan REA MCP (DEFAULT - Menghemat ~25.000 token per pesan)
python vibe_tools/rea_tool.py --disable

# Aktifkan hanya saat butuh reverse engineering biner
python vibe_tools/rea_tool.py --enable
```
