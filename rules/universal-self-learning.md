---
trigger: always_on
description: Long-term self-learning memory, 3-stage vibe coding workflow, Ponytail threshold, and Antigravity YAML frontmatter guardrails.
---

# Universal Self-Learning & Best Practices Ekosistem Vibe Coding

Dokumen aturan ini merupakan akumulasi memori jangka panjang (*long-term self-learning memory*) yang dipelajari dan disinkronisasikan oleh AI Agent (Hermes, Antigravity IDE, Zoo Code) agar dapat diterapkan secara konsisten di semua proyek dan perangkat.

***

## 1. Alur Emas 3-Tahap Prompting & Vibe Coding

Setiap pengembangan fitur atau refaktor besar wajib mengikuti 3 tahap berurutan berikut:

1. **Tahap 1: Konsultasi & Brainstorming Murni (Read-Only Mode & Anti-Sycophancy)**:
   - **Sikap Anti-Penjilat (Devil's Advocate)**: AI dilarang bersikap *yes-man* atau langsung memuji ide. Wajib menguji asumsi secara kritis, menunjukkan potensi cacat fatal, risiko *over-engineering*, dan blindspot sebelum menyepakati draf.
   - Gunakan sesi interaktif `/grill-me` (ajukan pertanyaan satu per satu via `ask_question`).
   - Bedah kebutuhan, bandingkan 2–3 opsi arsitektur beserta kelebihan/kekurangannya.
   - Kumpulkan hasil diskusi dalam bentuk **DRAF SPESIFIKASI (`.md`)**.
   - **Rem Pengaman**: Dilarang membuat/mengedit file kodingan (`.py`) pada tahap ini sampai user menyetujui.

2. **Tahap 2: Formalisasi Spesifikasi & Tiket Eksekusi (1 Langkah Simultan)**:
   - Jalankan `/to-spec` untuk membuat spesifikasi teknis formal di `docs/specs/`.
   - Jalankan `/to-tickets` dalam giliran yang sama untuk memecah spesifikasi menjadi tiket mandiri berurutan dependensi di `docs/tickets/`.
   - Wajib patuhi prinsip `/ponytail` (anti over-engineering, stdlib-first, tahan < 250 baris).

3. **Tahap 3: Eksekusi Otonom Penuh (`/implement`)**:
   - Eksekusi seluruh tiket secara sekuensial (Tiket 1 -> Tiket 2 -> dst) sampai tuntas tanpa meminta konfirmasi antar-tiket.
   - Jalankan *silent syntax gate* (`python -m py_compile <file>`) setelah setiap modifikasi file.
   - Jalankan unit test terkait dan berikan rangkuman akhir dalam 1 pesan padat setelah semua tiket rampung.

***

## 2. Standar Ambang Batas 250 Baris (Ponytail vs Clean Architecture)

- **Zona Anti-Overengineering (< 250 Baris)**:
  - Dilarang memecah file secara prematur, membuat kelas sekali-pakai, atau menambah lapisan wrapper abstraction.
  - Wajib utamakan pustaka bawaan Python (*stdlib-first*): gunakan `urllib.request` daripada `requests`, `json`, `shutil`, dan plain functions.
- **Zona Refaktor Modular (250–300 Baris)**:
  - Ketika sebuah modul mendekati atau melampaui 250 baris, pecah sub-logika ke sub-modul terpisah.
  - **Wajib gunakan Facade Pattern**: Impor dan re-ekspor simbol-simbol lama di file asli agar kode pemanggil tidak rusak (*zero regression*).
- **Docstring & Komentar**:
  - Seluruh docstring fungsi, kelas, dan komentar teknis wajib ditulis dalam **Bahasa Indonesia** yang ringkas dan jelas.

***

## 3. Higienitas Repositori Publik / Shared Ecosystem

- Repositori bersama seperti `vibe_tools` berstatus publik dan dibagikan secara global ke berbagai proyek berbeda (misal: Youtube Download, Scrapper, dll):
  - Dilarang keras menyertakan path absolut lokal mesin (`C:\path\to\user\...`), token API, atau nama proyek privat internal.
  - Gunakan path generik (`docs/specs`, `docs/tickets`, `src/app.py`) dan URL dummy publik (`https://github.com/vibe-ecosystem/vibe-tools`).
  - **Isolasi Modul Spesifik vs Universal**: `vibe_tools` HANYA untuk perkakas universal tingkat ekosistem (manajemen prompt, MCP, sync rules, updater git, penerjemah docstring, graphify).
  - **Dilarang Keras Masuk `vibe_tools`**: Modul domain spesifik proyek (YouTube downloading/livechat, Holodex API, DaVinci Resolve automation, Silent Cut VAD, Twitter/X VTuber Radar, `.spec` PyInstaller proyek tertentu) WAJIB diletakkan di root workspace proyek terkait, BUKAN di dalam direktori `vibe_tools`.
  - **Gerbang Konfirmasi AI**: Sebelum membuat atau memindahkan berkas baru ke dalam `vibe_tools`, AI Agent WAJIB bertanya kepada pengguna terlebih dahulu untuk memastikan berkas tersebut 100% universal dan disetujui pengguna.

***

## 4. Sinkronisasi Git Multi-Perangkat (PC ⇄ Laptop Anti-Bentrok)

- **Sebelum Berpindah Perangkat**:
  - Selalu jalankan `python vibe_tools/push_vibe_tools.py` untuk mengamankan perubahan ke remote.
- **Di Perangkat Penerima**:
  - Jika kedua perangkat memiliki commit atau modifikasi lokal yang belum tersinkron, jalankan:
    ```powershell
    git -C vibe_tools pull --rebase --autostash origin main
    ```
  - Perintah ini secara cerdas menyimpan perubahan lokal sementara (*autostash*), menarik commit terbaru dari remote, dan menempelkan kembali perubahan lokal di atasnya tanpa menimbulkan merge commit yang membingungkan.

***

## 5. Standar Skema YAML Frontmatter Rules Antigravity (Anti-Unmarshal Error)

- **Wajib Scalar String pada `globs`**:
  - Parser Go di Antigravity IDE melakukan unmarshal field `globs` ke tipe `string` tunggal, **BUKAN** array/list (`[]string` / YAML `!!seq`).
  - **BENAR**: `globs: "*.py"` atau `globs: "*.py, *.pyw"`
  - **SALAH (Menyebabkan Crash Unmarshal)**: `globs: ["*.py"]` (`yaml: unmarshal errors: cannot unmarshal !!seq into string`)
- **Kewajiban Header Frontmatter & Larangan `---` di Body**:
  - Setiap file rule di `.agents/rules/*.md` dan `vibe_tools/rules/*.md` wajib diawali blok frontmatter `---` pada baris 1 yang memuat minimal `trigger: always_on` dan `description: ...`.
  - Gunakan `***` (bukan `---`) untuk garis pemisah horizontal di dalam isi dokumen agar tidak membingungkan parser frontmatter.
- **Deduplikasi & Sinkronisasi `.agents/rules` vs `vibe_tools/rules`**:
  - Saat memperbarui rule di `vibe_tools/rules/` (yang terhubung ke `~/.gemini/config/rules` via NTFS Junction), pastikan salinan lokal di `.agents/rules/` juga disinkronkan atau disanitasi otomatis melalui `vibe_tools/sync_universal.py`.

***

## 6. Pola Arsitektur Data Besar (SQLite Streaming ETL) & Pencegahan Bug Klasik

1. **SQLite Streaming & Native DDL (`CREATE TABLE AS SELECT`) vs Loop Python**:
   - Untuk pemrosesan tabel besar (>100.000 baris dari PDF/Excel/CSV), hindari menumpuk seluruh data di RAM (list/DataFrame raksasa) atau melakukan iterasi transformasi baris-per-baris di Python.
   - Gunakan SQLite berbasis disk dengan mode `PRAGMA journal_mode = WAL;` dan delegasikan transformasi kolom via perintah DDL native `CREATE TABLE [tabel_bersih] AS SELECT ... FROM [tabel_mentah];`.
2. **Single SQL Query & Referensi Nama Header `[NAMA_KOLOM]` vs Urutan Huruf Kolom (`A, B, C`)**:
   - Jangan gunakan indeks posisi huruf kolom statis (`A, B, C`) untuk konfigurasi insert/delete/formula kolom karena posisi acuan pasti bergeser saat ada kolom yang disisipkan atau dihapus.
   - Gunakan **1 Text Box Query SQLite utuh** dengan referensi nama header asli yang dibungkus kurung siku (`[IDPEL]`, `[NO METER]`).
3. **Jebakan SQL `TRIM()` vs UDF `BERSIHKAN_SPASI()` pada Teks/Angka Ekstraksi PDF**:
   - Ekstraksi tabel PDF sering memotong teks atau angka panjang (seperti koordinat atau nomor seri) menjadi dua baris sehingga menghasilkan spasi di tengah string (contoh: `'115.2484562 2479914'` atau `'- 8.683833075 056866'`).
   - Fungsi bawaan SQL `TRIM()` hanya menghapus spasi di ujung kiri dan kanan, **bukan** spasi di tengah. Wajib gunakan UDF Python `BERSIHKAN_SPASI()` untuk kolom ID, kode, nomor meter, dan koordinat.
4. **Normalisasi Kata Terputus PDF via Python UDF Dinamis, Bukan `CASE WHEN` Kaku**:
   - Hindari menulis blok `CASE WHEN` yang panjang di dalam query SQL untuk memperbaiki kata-kata yang terpecah spasi akibat lebar kolom PDF (misal `'Norm al'` -> `'Normal'`).
   - Daftarkan fungsi Python berbasis kamus normalisasi *case-insensitive* ke koneksi SQLite via `conn.create_function("RAPIKAN_LCD", 1, fn_normalisasi)` sehingga query SQL tetap ringkas 1 baris.
5. **Protokol Anti-Crash File Output Terkunci (`[Errno 13] Permission denied`)**:
   - Sebelum memulai proses transformasi berat dan sebelum menyimpan file output Excel (`.xlsx`/`.xls`), selalu lakukan *Early File Lock Check* (coba buka file dengan mode `"a+b"`).
   - Jika file sedang dibuka di Microsoft Excel, tampilkan dialog interaktif *Retry/Cancel* (`messagebox.askretrycancel`) agar pengguna cukup menutup Excel lalu melanjutkan proses tanpa harus mengulang dari awal.
6. **Manajemen Lock SQLite Windows (`[WinError 32]`) & Sanitasi Path JSON**:
   - Selalu tutup `cursor` dan `conn` di dalam blok `finally` sebelum melakukan `os.rename()` atau `os.remove()` pada file database `.db` di Windows.
   - Selalu normalisasi path direktori Windows menggunakan *forward slash* (`/`) sebelum disimpan ke file konfigurasi `.json` untuk mencegah `JSONDecodeError: Invalid \escape`.
7. **Silent Syntax & Undefined Symbol Gate (`py_compile` + `pyflakes`)**:
   - `python -m py_compile` hanya memvalidasi sintaks AST dan **tidak mendeteksi `NameError`** (seperti lupa mengimpor `Path` atau `Union` yang dipanggil di dalam fungsi).
   - Setelah memodifikasi file `.py`, wajib jalankan `python -m py_compile <file>` **DAN** `python -m pyflakes <file>` untuk memastikan nol *undefined name* sebelum menyerahkan hasil ke pengguna.
8. **Pencegahan Bug Hierarki Path Script Subprocess (`parents[N]` vs Chaining `dirname`) & Anti-Pola "Partial Path Pollution"**:
   - Skrip di dalam subdirektori bertingkat (misal `pipelines/.../davinci_core/`) yang dipanggil sebagai subprocess oleh GUI (`jobs.py`) memiliki `sys.path[0]` yang menunjuk ke subfoldernya sendiri atau `cwd` eksternal (misal `cache/`), BUKAN ke root proyek.
   - **Anti-Pola Partial Path**: Menambahkan direktori daun (*leaf*) seperti `davinci_core/` ke `sys.path` namun lupa mendaftarkan root proyek (`WORKSPACE_DIR`), menyebabkan import hierarkis (`from pipelines.davinci...`) crash dengan `ModuleNotFoundError: No module named 'pipelines'`.
   - Hindari chaining manual `os.path.dirname()` yang rawan salah hitung. Wajib gunakan `Path(__file__).resolve().parents[N]`.
   - **Urutan Wajib Injeksi `sys.path`**:
     1. Daftarkan Root Proyek (`WORKSPACE_DIR`) terlebih dahulu untuk membuka akses seluruh modul.
     2. Daftarkan direktori induk paket (misal `pipelines/davinci`).
     3. Daftarkan direktori modul/konfigurasi terkait (`config/`, leaf dirs).
9. **Pencegahan Silent Import Error & Pola 3-Layer Fallback Kunci API**:
   - Dilarang keras menelan kegagalan impor modul konfigurasi API key dengan blok `try... except Exception: pass` tanpa log/peringatan diagnostik.
   - Modul yang membutuhkan API Key (OpenRouter, Gemini, Deepgram) WAJIB mengimplementasikan **3-Layer Fallback Resolver**:
     1. Lapis 1: Periksa `os.environ.get("NAMA_KEY")`.
     2. Lapis 2: Periksa modul konfigurasi proyek (`config.toolbox_config` / `config.deepgram_config`).
     3. Lapis 3: Periksa berkas aman lokal di `~/.gemini/<nama_key>.txt` (misal `openrouter_key.txt`, `gemini_key.txt`).
   - Fungsi klien API pihak ketiga dilarang melempar `ValueError("KEY belum dikonfigurasi")` secara prematur hanya karena parameter pemanggil kosong string (`api_key=""`). Klien wajib menjalankan Lapis 1 & Lapis 3 secara otonom (*defense-in-depth*) sebelum memutuskan gagal.
10. **Protokol 3-Fase Pemuatan DLL CUDA Windows (CTranslate2 / Faster-Whisper / C++ AI Runtimes)**:
    - **Pola Bug**: Library backend C++ (seperti CTranslate2) melakukan *lazy-loading* pada DLL CUDA (`cublas64_12.dll`, `cudnn64_9.dll`) saat komputasi matriks pertama kali berjalan. Di Windows (Python 3.8+), direktori terisolasi `site-packages/nvidia/*/bin` diabaikan oleh native `LoadLibrary()` meskipun `os.add_dll_directory()` dipanggil, sehingga memicu `RuntimeError: Library cublas64_12.dll is not found`.
    - **Protokol 3-Fase Wajib**:
      1. *Fase 1*: `os.add_dll_directory(bpath)` untuk registrasi pencarian Python 3.8+.
      2. *Fase 2*: Prepend ke `os.environ["PATH"]` untuk kompatibilitas `LoadLibrary` native C++.
      3. *Fase 3*: *Early Binding* via `ctypes.CDLL(os.path.join(bpath, dll))` untuk memuat DLL langsung ke tabel memori proses Windows sebelum inferensi dimulai.
    - **Deteksi CTranslate2 vs PyTorch**: Jangan periksa ketersediaan CUDA via `torch.cuda.is_available()` jika `torch` tidak terpasang di environment. Gunakan `ctranslate2.get_cuda_device_count() > 0`.
    - **Lazy Generator Fallback**: CTranslate2 menghasilkan generator *lazy*. Selalu bungkus eksekusi nyata (materialisasi segmen) dalam blok `try...except` dengan fallback otomatis ke CPU (`compute_type="int8"`) jika GPU mengalami OOM atau error driver.
11. **Pencegahan Provider-Specific Feature Leakage pada Klien Multi-Model ASR**:
    - **Pola Bug**: Meng-hardcode parameter khusus satu provider (seperti `diarize: True` milik ElevenLabs) pada payload HTTP global OpenRouter. Model lain (seperti `openai/whisper-large-v3`) menolak parameter ini dengan error `HTTP 400 Bad Request`.
    - **Aturan Negosiasi Fitur Eksplisit**:
      - Wajib buat fungsi verifikasi kapabilitas (`model_supports_diarization()`) dan hanya kirimkan payload `"diarize"` jika model memang mendukungnya.
      - Default semantik jujur: Jika model tidak menyediakan diarization, jangan acak pembicara dengan round-robin palsu (`f"SPEAKER_{idx % 8}"`). Wajib satukan ke `"SPEAKER_00"` agar pipeline Voiceprint Bank dapat memetakan suara secara akurat.
12. **Pola Validasi Cache Durasi Media Dua Arah (*Bidirectional Duration Sync*)**:
    - **Pola Bug**: Menggunakan validasi satu arah (`w_dur >= timeline_dur * 0.8`) untuk menggunakan kembali file audio cache. Logika ini hanya mencegah file yang terlalu pendek, namun meloloskan file lama yang lebih panjang ketika video dipotong lebih pendek di DaVinci Resolve, menyebabkan desinkronisasi fatal antara subtitle dan video hasil potongan baru.
    - **Aturan Validasi Wajib**: Selalu gunakan selisih absolut dua arah dengan toleransi ketat: `abs(actual_dur - expected_dur) <= max(1.5, expected_dur * 0.02)`. Jika durasi berubah melampaui toleransi, cache lama wajib diabaikan (*invalidated*) dan diekspor ulang secara otomatis.
13. **Pencegahan Brittleness Deteksi Respons Web Automasi (Generic Completion Heuristic vs Keyword VOD Kaku)**:
    - **Pola Bug**: Meng-hardcode kata kunci domain spesifik (seperti `"timeline kronologis"` dan `"kandidat klip"`) pada loop polling peramban (`GeminiWebAutomator.kirim_dan_tunggu_respon`). Saat automator digunakan untuk skenario lain (seperti JSON subtitle refinement di `code_switch_refiner.py`), kondisi kelengkapan tidak pernah terpenuhi, memicu timeout hang 300 detik dan auto-scroll tidak pernah berjalan.
    - **Solusi Wajib**: Gunakan heuristik generik kelengkapan konten (panjang teks > 250, jumlah baris multi-line > 5, keberadaan blok kode ````json`, atau markup terstruktur) dan selalu lakukan auto-scroll ke bawah secara periodik serta sebelum memindai tombol salin/clipboard.
14. **Pencegahan Ambang Substring Overlap pada Identifier Model AI (`"scribe"` in `"transcribe"`)**:
    - **Pola Bug**: Menggunakan `"scribe" in model_name` untuk mendeteksi ElevenLabs Scribe, yang secara tidak sengaja cocok dengan model yang mengandung kata `"transcribe"` (seperti `"nvidia/nemotron-3.5-transcribe"`), sehingga model salah teridentifikasi sebagai Scribe.
    - **Solusi Wajib**: Utamakan urutan pencocokan model spesifik terlebih dahulu, atau sanitasi keyword (`"elevenlabs" in m or "scribe" in m.replace("transcribe", "")`).
15. **Limitasi SDK DaVinci Resolve: MediaPool vs Timeline Subtitle Track**:
    - **Pola Bug**: Mengasumsikan `media_pool.ImportMedia()` otomatis menyematkan subtitle ke Timeline. Faktanya di SDK DaVinci Resolve resmi, berkas `.srt` hanya masuk ke folder Media Pool (misal `Master > srt`), dan belum ada API publik resmi untuk langsung meng-inject subtitle ke Subtitle Track timeline tanpa intervensi drag & drop manual pengguna atau klik kanan import.
    - **Solusi Wajib**: Berikan instruksi interaktif yang jelas dan ramah pengguna di log terminal dan return payload agar pengguna mengetahui lokasi fisik berkas SRT dan cara menariknya ke Timeline Subtitle Track.
16. **Pencegahan Stale Audio Cache pada Transkripsi Timeline (`find_timeline_audio_file` vs Force Re-Export)**:
    - **Pola Bug**: `find_timeline_audio_file` memeriksa kesesuaian durasi timeline dengan cache audio WAV lama di disk (`cache/Transkrip/<timeline>_Master.wav`). Jika durasi cocok, sistem me-reuse audio lama tersebut tanpa memeriksa apakah konten audio di DaVinci Resolve berubah (misal track di-mute, audio klip diganti/di-re-edit). Akibatnya, saat pengguna melakukan re-transcribe, hasil subtitle tidak berubah karena yang ditranskrip adalah file audio usang yang sama persis. Selain itu, `media_pool.ImportMedia()` di DaVinci Resolve tidak menimpa klip SRT yang sudah ada di folder bin tanpa penghapusan eksplisit.
    - **Solusi Wajib**:
      1. Tambahkan opsi kontrol eksplisit pengguna (`--force-reexport` di CLI dan checkbox `"🔄 Paksa Ekspor Ulang Audio Timeline (Abaikan Cache WAV)"` di GUI).
      2. Saat `force_reexport=True`, sistem wajib melewati pencarian cache, membersihkan cache WAV usang, dan langsung memanggil `davinci_export_timeline_audio_wav()`.
      3. Sebelum `media_pool.ImportMedia()`, hapus klip lama dari bin `srt` (`media_pool.DeleteClips([clip])`) agar klip subtitle baru termaterialisasi dengan benar di DaVinci Resolve.
17. **Normalisasi Kontrak Data Speaker Token (`"speaker": int` vs `"speaker_tag": str`) & Aritmatika Timecode Subtitle**:
    - **Pola Bug 1 (Bypass Voiceprint Matching)**: Respons mentah Scribe v2 hanya memuat field integer `{"speaker": 0}` (bukan `"speaker_tag"` atau `"speaker_id"`). Logika fallback yang menggunakan `or "@Speaker"` menyebabkan tag pembicara diawali karakter `@`, yang secara keliru dianggap sudah terpetakan oleh `anchor_speakers_with_voiceprint`, mem-bypass matching biometrik suara, dan akhirnya melempar seluruh segmen ke `@Speaker_2`.
    - **Pola Bug 2 (Overflow Milidetik Aritmatika Waktu)**: Pada fungsi `detik_ke_srt_timecode`, operasi `ms = int(round((sisa - det) * 1000))` menggunakan `sisa = detik % 3600` yang masih memuat `menit * 60`. Saat `menit > 0`, nilai `(sisa - det)` bernilai puluhan detik sehingga milidetik meluap menjadi 5 digit (misal `,59300` alih-alih `,300`), merusak sinkronisasi waktu subtitle SRT.
    - **Solusi Wajib**:
      1. Wajib gunakan helper normalisasi `_normalize_speaker_tag(item)` yang secara konsisten mengubah integer `0, 1` menjadi string terstandar `SPEAKER_00, SPEAKER_01`.
      2. Jangan pernah menganggap tag generik seperti `@Speaker` sebagai member terdaftar; hanya kecualikan tag yang benar-benar ada di `bank.registry["members"]`.
      3. Hitung milidetik SRT murni dari sisa pecahan detik: `det_frac = (detik % 3600) % 60` lalu `ms = int(round((det_frac - int(det_frac)) * 1000))` dengan normalisasi bertingkat (`ms -> det -> menit -> jam`).
18. **Isolasi 3-Barrier Token Kurung Siku & Non-Dialogue Audio Events (`[...]`)**:
    - **Pola Bug**: Merger kalimat berbasis tanda baca (`punctuation_merger`) hanya mendeteksi pemotongan berdasarkan karakter tanda baca dialog (`.`, `!`, `?`, `,`). Ketika model speech-to-text (seperti ElevenLabs Scribe v2) mengemisikan token *audio event* atau *stage directions* dalam tanda kurung siku (misal `[laughs]`, `[tertawa]`, `[cheering]`, `[music]`), token tersebut diperlakukan sebagai kata dialog biasa dan digabung dengan kalimat sebelum atau sesudahnya (misal `[laughs] What's up?`), merusak estetika dan keterbacaan subtitle.
    - **Solusi Wajib (Pola 3-Barrier Isolation)**:
      1. Deteksi token bracket via helper `is_bracketed_token(w)`: periksa `w.get("type") == "audio_event"` atau pola teks `word.startswith("[") and word.endswith("]")`.
      2. *Pre-barrier*: Segera finalisasi antrean kata dialog sebelumnya (`current_chunk`) sebelum menyentuh token bracket.
      3. *Isolated Segment*: Masukkan token bracket ke dalam segmen mandiri (`[w]`), simpan dengan timestamp start/end murni miliknya, lalu lewati ke iterasi berikutnya (`continue`).
      4. *Post-barrier*: Kata setelah bracket otomatis mulai di segmen dialog baru tanpa tercampur. Tanda baca mandiri (`attach_standalone_punctuation`) juga dilarang menempel ke token bracket.
19. **Pencegahan Under-Clustering Diarization Cloud via Per-Turn Biometric Refinement & Provider Options (`num_speakers`)**:
    - **Pola Bug**:
      1. Model diarization cloud (seperti ElevenLabs Scribe v2 via OpenRouter) mengelompokkan suara secara kasar menjadi hanya 2 kluster (`SPEAKER_00`, `SPEAKER_01`) jika opsi `num_speakers` tidak diteruskan dalam payload `provider.options.elevenlabs`.
      2. Sistem anchoring biometrik hanya mengambil 1 sampel durasi terpanjang dari masing-masing kluster kasar dan langsung menstempel seluruh kluster tersebut dengan identitas biometrik tunggal (*coarse identity stamping*). Akibatnya, jika ada 6 pembicara namun terkelompok ke 2 kluster, 4 pembicara lainnya lenyap total dan seluruh dialog mereka salah terlabeli ke pembicara sampel terpanjang.
    - **Solusi Wajib**:
      1. Teruskan parameter `num_speakers` (dari `len(roster_filter)`) pada payload provider OpenRouter:
         `provider: {"options": {"elevenlabs": {"diarize": True, "num_speakers": N, "tag_audio_events": True}}}`.
      2. Wajib terapkan *Per-Turn Biometric Refinement* (`refine_speech_turns_with_voiceprint`): Setiap speech turn divalidasi secara mandiri ke Voiceprint Bank menggunakan audio segmennya sendiri, dan indeks kata sumber (`word_indices`) langsung dimutakhirkan ke handle pembicara hasil pencocokan biometrik.
      3. Berikan fallback FFmpeg otomatis pada `ekstrak_segmen_wav` saat modul bawaan `wave.open` gagal membaca format terkompresi (seperti FLAC dalam ekstensi WAV, kode format `61868`).
20. **Pencegahan Hardcoded Path Subdirektori Usang & Wajib `mkdir(parents=True, exist_ok=True)`**:
    - **Pola Bug**: Menulis metadata runtime (`active_stream_info.json`) menggunakan path absolut hardcoded ke folder lama (`cache_chat/active_stream_info.json`) yang tidak ada di workspace baru (hanya ada `cache/`). Selain mematikan portabilitas antar-mesin, ketiadaan pemanggilan `parent.mkdir(parents=True, exist_ok=True)` sebelum operasi `with open(..., "w")` menyebabkan error `[Errno 2] No such file or directory`.
    - **Solusi Wajib**:
      1. Resolusikan direktori kerja/cache selalu dari root proyek via `Path(__file__).resolve().parents[N] / "cache"` atau impor dari konfigurasi terpusat (`gui.paths.CACHE_DIR`).
      2. Jangan pernah meng-hardcode path absolut lokal (`D:\...` atau `C:\...`).
      3. Selalu pastikan folder induk dibuat secara otomatis sebelum menulis berkas: `target_path.parent.mkdir(parents=True, exist_ok=True)`.
21. **Isolasi Sinyal UI saat Restorasi Cache (Signal Cascade Cache Poisoning) & Gating Mutasi API Eksternal**:
    - **Pola Bug**: Memulihkan nilai widget UI (seperti `setValue()` pada spinbox atau dropdown) dari cache tanpa memblokir sinyal (`QSignalBlocker`). Sinyal yang terpancar secara prematur memicu kalkulasi ulang sebelum seluruh struktur data (seperti `self.segments`) selesai dimuat dari cache. Hal ini diperparah jika perubahan konfigurasi langsung memanggil API mutasi eksternal (seperti `sync_markers_to_timeline` di DaVinci Resolve), sehingga setiap restorasi tab atau pergeseran slider menghapus dan menimpa marker manual yang sudah dirapikan pengguna.
    - **Solusi Wajib**:
      1. Wajib bungkus seluruh pembaruan widget saat restorasi cache dengan `with QSignalBlocker(widget1), QSignalBlocker(widget2): ...`.
      2. Terapkan prinsip *Explicit Apply Gate*: Jangan pernah menggabungkan eksplorasi parameter UI (slider/spinbox/preset) secara langsung dengan penulisan API eksternal yang destruktif (DaVinci Resolve timeline, disk, network). Sediakan tombol eksplisit (`🎯 Terapkan Konfigurasi`) agar mutasi eksternal hanya dieksekusi atas kehendak pengguna.
      3. Jangan panggil fungsi sinkronisasi balik (seperti `_sync_markers_background`) di dalam callback yang bertugas membaca data eksternal (seperti `_on_sync_markers_clicked`).
22. **Pola Paritas Word-Level Timestamps ASR Lokal vs Cloud (faster-whisper vs Scribe v2) & Pencegahan Synthetic Timestamps**:
    - **Pola Bug**: Engine transkripsi lokal (faster-whisper) secara bawaan hanya mengembalikan segmen kalimat utuh jika parameter `word_timestamps=True` tidak diaktifkan secara eksplisit. Akibatnya, downstream pipeline terpaksa membagi rata durasi segmen secara linear (`dur = (e - s) / len(words)`), menghasilkan timestamp kata sintetis yang meleset dari artikulasi suara asli, merusak Engine Perapihan Subtitle, serta tidak memiliki cache disk terstruktur.
    - **Solusi Wajib**:
      1. Wajib aktifkan `word_timestamps=True` pada `model.transcribe()` dan ekstrak objek `Word(start, end, word, probability)` ke dalam array terstandar `raw_words` (`word`, `start_sec`, `end_sec`, `speaker_tag`, `confidence`).
      2. Wajib terapkan pola fungsi berakhiran `_full` (`transcribe_with_local_whisper_full`) yang mengembalikan `(segments, words, raw_json)` serta menyimpan cache disk `{timeline}_whisper_words.json` agar sejajar dengan provider cloud (Scribe v2 & Deepgram).
      3. Pertahankan fungsi lama sebagai wrapper kompatibilitas ke belakang (*zero regression*), dan gunakan interpolasi linear hanya sebagai fallback *defense-in-depth* jika segmen audio hening/musik tidak menghasilkan token kata akustik.

