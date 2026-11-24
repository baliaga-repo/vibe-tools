# Universal Self-Learning Bug & Architecture Patterns Archive (On-Demand Reference)

> **Usage**: Do NOT load this entire file into context. Use `grep` / `Select-String` on the index below and read only the matching 10–25 line slice when troubleshooting a related domain.

## Quick Index
- **1–6**: SQLite Streaming ETL, Native DDL, PDF Space/Word UDF, Excel File Lock, Windows SQLite `[WinError 32]` & JSON Slash
- **7–9**: `py_compile` + `pyflakes` Gate, Subprocess `Path.parents[N]` & `sys.path` Order, 3-Layer API Key Fallback
- **10–14**: Windows CUDA 3-Phase DLL Loading, Multi-Model ASR Feature Negotiation, Bidirectional Duration Sync, Generic Web Automation Heuristic, Model Name Substring Overlap
- **15–19**: NLE MediaPool vs Timeline Subtitle Track, Stale Audio Cache & Force Re-Export, Speaker Tag Normalization & SRT Millisecond Arithmetic, 3-Barrier Bracket Token Isolation, Per-Turn Biometric Refinement & Cloud `num_speakers`
- **20–24**: Relative Path & `mkdir(parents=True)`, Qt Signal Cascade (`QSignalBlocker`) & Explicit Apply Gate, Local vs Cloud Word-Level Timestamps, Keyless Media Scraper & `Download-Then-Play` Qt6 Preview, SSR/RSC Pagination & Virtualized `QMovie` Grid
- **25–28**: NLE `Pan`/`Tilt` Scale & Proxy Calibration, Tiered Entity Priority & Cache Hash Isolation, Qt `setCellWidget` Padding & `&` Mnemonic Escape, 24-bit PCM (`sampwidth=3`) Decoding & Unique Unknown Speaker Ordinals

***

## Patterns 1–6: SQLite Streaming ETL, PDF Extraction, & Windows File Locks

1. **SQLite Streaming & Native DDL (`CREATE TABLE AS SELECT`) vs Python Loops**:
   - For large tables (>100k rows from PDF/Excel/CSV), avoid holding full lists/DataFrames in RAM or row-by-row Python transforms.
   - Use disk-backed SQLite with `PRAGMA journal_mode = WAL;` and run native DDL `CREATE TABLE [clean_tbl] AS SELECT ... FROM [raw_tbl];`.
2. **Single SQL Query & Header Name References `[COL_NAME]` vs Static Column Letters (`A, B, C`)**:
   - Avoid static Excel column letters (`A, B, C`) that shift when columns are inserted/deleted.
   - Use a single SQLite query referencing original header names in brackets (`[IDPEL]`, `[NO METER]`).
3. **SQL `TRIM()` Trap vs Python UDF `BERSIHKAN_SPASI()` on PDF-Extracted Numbers/IDs**:
   - PDF table extraction splits long strings/coordinates across lines, introducing inner spaces (e.g., `'115.2484562 2479914'`).
   - SQL `TRIM()` only strips leading/trailing spaces. Register a Python UDF stripping internal whitespace for IDs, serial numbers, and coordinates.
4. **Dynamic Dictionary UDF for Broken PDF Words vs Rigid `CASE WHEN`**:
   - Avoid huge `CASE WHEN` blocks for split words (`'Norm al'` -> `'Normal'`). Register a case-insensitive dictionary normalizer via `conn.create_function(...)`.
5. **Early File Lock Check (`[Errno 13] Permission denied`)**:
   - Before heavy transforms and before writing Excel outputs, test opening with `"a+b"`. If locked in Excel, prompt `askretrycancel` so the user can close the file without restarting.
6. **Windows SQLite Lock (`[WinError 32]`) & JSON Path Sanitization**:
   - Always close `cursor` and `conn` inside `finally` before `os.rename()`/`os.remove()` on `.db` files on Windows.
   - Normalize Windows directory paths with forward slashes (`/`) before persisting to `.json` to avoid `JSONDecodeError: Invalid \escape`.

## Patterns 7–9: Static Gates, Subprocess Paths, & API Key Fallbacks

7. **Silent Syntax & Undefined Symbol Gate (`py_compile` + `pyflakes`)**:
   - `python -m py_compile` only checks syntax AST and misses `NameError` (e.g., missing `Path`/`Union` import). Always run both `py_compile` and `pyflakes` after `.py` edits.
8. **Subprocess Path Hierarchy (`parents[N]`) & Anti-Partial Path Pollution**:
   - Nested scripts invoked as subprocesses inherit leaf `sys.path[0]` or external `cwd`, breaking hierarchical imports (`ModuleNotFoundError`).
   - Avoid chained `os.path.dirname()`; use `Path(__file__).resolve().parents[N]` and inject `sys.path` in order: (1) Project Root, (2) Package parent, (3) Module/config dirs.
9. **No Silent Import Swallowing & 3-Layer API Key Fallback**:
   - Never swallow config import errors with `except Exception: pass`.
   - Resolve API keys in 3 layers: (1) `os.environ.get(...)`, (2) project config module, (3) local key file `~/.gemini/<key_name>.txt`. API clients must run layers 1 & 3 autonomously before raising `ValueError`.

## Patterns 10–14: Windows CUDA DLLs, Multi-Model ASR, Cache Sync, & Automation

10. **Windows 3-Phase CUDA DLL Loading (CTranslate2 / Faster-Whisper)**:
    - C++ backends lazy-load CUDA DLLs (`cublas64_12.dll`, `cudnn64_9.dll`) where native `LoadLibrary` ignores isolated `site-packages/nvidia/*/bin`.
    - Execute 3 phases before inference: (1) `os.add_dll_directory(bpath)`, (2) prepend to `os.environ["PATH"]`, (3) early bind via `ctypes.CDLL(...)`.
    - Detect CUDA via `ctranslate2.get_cuda_device_count() > 0` (not `torch` if absent), and wrap lazy generator materialization in `try...except` with CPU `int8` fallback.
11. **Multi-Model ASR Feature Negotiation (No Provider Leakage)**:
    - Never hardcode provider-specific flags (e.g., `diarize: True`) in global payloads; verify capability first (`model_supports_diarization()`).
    - Without diarization, default honestly to `"SPEAKER_00"` instead of fake round-robin speaker IDs.
12. **Bidirectional Media Duration Cache Sync**:
    - Never use one-sided cache checks (`actual >= expected * 0.8`), which allow stale longer audio when a timeline is trimmed shorter.
    - Enforce two-sided tolerance: `abs(actual_dur - expected_dur) <= max(1.5, expected_dur * 0.02)`.
13. **Generic Web Automation Completion Heuristic**:
    - Avoid hardcoding domain keywords in browser polling loops. Use generic structural completeness checks (text length > 250, multi-line > 5, code fences) and auto-scroll before scanning copy buttons.
14. **Model Identifier Substring Overlap (`"scribe"` in `"transcribe"`)**:
    - Match specific model identifiers first or sanitize overlapping tokens (`"scribe" in m.replace("transcribe", "")`) to avoid misclassifying models containing `"transcribe"`.

## Patterns 15–19: NLE SDK, Subtitle Timecode, & Speaker Diarization

15. **NLE MediaPool vs Timeline Subtitle Track Limitation**:
    - `media_pool.ImportMedia()` imports `.srt` into a Media Pool bin only; it does not auto-place onto the Timeline Subtitle Track. Log explicit physical path and placement instructions.
16. **Stale Timeline Audio Cache & Media Pool Overwrite**:
    - Duration match alone misses audio content edits (muted tracks/replaced clips). Provide `--force-reexport` / UI checkbox to bypass and purge stale WAV cache, and delete old SRT clips (`DeleteClips`) before re-importing.
17. **Speaker Token Contract Normalization & SRT Millisecond Overflow**:
    - Normalize raw integer speaker fields (`{"speaker": 0}`) via `_normalize_speaker_tag()` -> `SPEAKER_00`. Never treat generic `@Speaker` as a registered voiceprint member.
    - Compute SRT milliseconds strictly from fractional seconds: `det_frac = (sec % 3600) % 60`, `ms = int(round((det_frac - int(det_frac)) * 1000))` with carry-over (`ms -> sec -> min -> hr`).
18. **3-Barrier Isolation for Bracketed Audio Events (`[...]`)**:
    - Detect via `type == "audio_event"` or `[...]`. Flush pending dialogue chunk (pre-barrier), emit isolated bracket segment with its own timestamps, and prevent standalone punctuation attachment (post-barrier).
19. **Cloud Diarization Under-Clustering & Per-Turn Biometric Refinement**:
    - Pass `num_speakers` in provider options when roster size is known.
    - Validate each speech turn individually against the voiceprint bank rather than coarse cluster stamping, and provide FFmpeg fallback when `wave.open` fails on compressed WAV headers (e.g., FLAC format code `61868`).

## Patterns 20–24: Portable Paths, Qt6 Signals, Word Timestamps, & Async Media Grids

20. **No Hardcoded Legacy Paths & Mandatory `mkdir(parents=True, exist_ok=True)`**:
    - Resolve cache/runtime dirs from `Path(__file__).resolve().parents[N]` or centralized `paths` config, never hardcoded absolute machine paths, and always call `target.parent.mkdir(parents=True, exist_ok=True)`.
21. **Qt Signal Cascade Poisoning & Explicit Apply Gate**:
    - Wrap widget restoration from cache in `QSignalBlocker(...)`.
    - Decouple exploratory UI controls (sliders/spinboxes) from destructive external API writes using an explicit Apply button; never trigger write-back inside read-sync callbacks.
22. **Local vs Cloud Word-Level Timestamps Parity**:
    - Enable `word_timestamps=True` on local ASR (`faster-whisper`), emit standardized `raw_words` (`word, start_sec, end_sec, speaker_tag, confidence`), persist `{name}_whisper_words.json` via `_full` functions, and keep legacy wrappers for backwards compatibility.
23. **Keyless Media Scraper & Qt6 `Download-Then-Play` Preview**:
    - Avoid deprecated public demo keys (`HTTP 403`); use co-located HTML anchor scraping with base-ID deduplication.
    - Download short preview clips/GIFs on a background thread to local cache for `QMediaPlayer`/`QMovie` instead of raw streaming or `QWebEngineView` (which crashes under `QT_QPA_PLATFORM=offscreen`).
24. **SSR/RSC Pagination Cap & Virtualized Async `QMovie` Grid**:
    - Inspect live HTTP responses first; parse embedded JSON state (`<script id="store-cache">`), handle absolute/relative `href`, exclude static `_s.gif`, and degrade pagination cleanly when keyless.
    - In Qt6 `QListWidget` (`IconMode`, `setUniformItemSizes(True)`): guard `QThreadPool` callbacks with a generation counter + `@Slot`, virtualize active `QMovie` instances (<= 32 visible, debounce ~80 ms, release offscreen via `stop()`, `setFileName("")`, `setDevice(None)`, `deleteLater()` to prevent Windows `[WinError 32]`), and update selection styles in O(1).

## Patterns 25–28: NLE Coordinates, Priority Filtering, Qt Cell Widgets, & 24-bit PCM

25. **NLE `Pan`/`Tilt` Scale-to-Fit & Proxy Resolution Calibration**:
    - Compensate both aspect-ratio fit fraction (`x_scale`, `y_scale`) and proxy scale (`quarter=4.0`, `half=2.0`, `original=1.0`, checking timeline setting then project setting fallback) in one helper: `Pan = (cx - cw*0.5) / (proxy_scale * x_scale)`.
26. **Tiered Entity Priority & Cache Hash Isolation**:
    - Preserve per-track entity/character metadata before batching to LLM, filter stopwords from overlap scoring, split prompt quota (e.g., 2/3 priority + 1/3 general fallback), include normalized entity in cache MD5 key, and exclude entity aliases from bare slug matching.
27. **Qt `setCellWidget` Clipped Buttons & `&` Mnemonic Escape**:
    - Use compact cell button padding (`padding: 3px 10px;`), set `verticalHeader().setDefaultSectionSize(38)`, fixed column width >= combined `sizeHint().width()` + margin, verify under `QT_QPA_PLATFORM=offscreen`, and escape `&` -> `&&` on dynamic button labels.
28. **24-bit PCM (`sampwidth=3`) Silent Corruption & Unknown Speaker Cluster Collapse**:
    - Explicitly decode `sampwidth in (2, 3, 4)` (including 24-bit sign-extension to 32-bit) and resample to `target_sr=16000` before voiceprint scoring.
    - Preserve unique ordinal labels per unknown cluster (`@Speaker_1`, `@Speaker_2`, ...) instead of collapsing all into `@Speaker_2`, and restrict host lock to registered voiceprint members only.
