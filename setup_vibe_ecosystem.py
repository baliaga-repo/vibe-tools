"""
[ID]: Skrip Otomasi Pemasangan Ekosistem Vibe Coding Cerdas, Ramping & Hemat Token.
Menghasilkan seluruh folder .agents, rules, skills, workflows, graphify_map.py,
graphify_update.py, push_github.py, dan MAP.md secara instan dalam 1 detik.

Cara Penggunaan di Proyek Baru:
    1. Salin berkas 'setup_vibe_ecosystem.py' ke folder proyek baru Anda.
    2. Jalankan perintah terminal:
           python setup_vibe_ecosystem.py
    3. Ekosistem langsung siap dipakai tanpa perlu membuang kuota token AI!

[EN]: Smart, Lean & Token-Efficient Vibe Coding Ecosystem Auto-Setup Script.
Instantly generates all .agents, rules, skills, workflows folders along with graphify_map.py,
graphify_update.py, push_github.py, and MAP.md files in just 1 second.

Usage for New Projects:
    1. Copy 'setup_vibe_ecosystem.py' to your new project folder.
    2. Run terminal command:
           python setup_vibe_ecosystem.py
    3. The ecosystem is immediately ready without wasting AI token quota!
"""
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == "vibe_tools":
    BASE_DIR = os.path.dirname(BASE_DIR)


def baca_skrip_lokal(nama_file: str) -> str:
    """
[ID]: Membaca isi skrip dari folder lokal vibe_tools jika tersedia.
[EN]: Reads the script content from the local vibe_tools folder if available.
"""
    lokal = os.path.join(os.path.dirname(os.path.abspath(__file__)), nama_file)
    if os.path.exists(lokal):
        try:
            with open(lokal, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return ""


def buat_berkas(rel_path: str, isi: str):
    """
[ID]: Menulis berkas jika belum ada, mencegah penimpaan file atau setup spesialis yang sudah ada.
[EN]: Writes the file if it does not exist, preventing overwriting or disrupting existing specialized setups.
"""
    target = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if not os.path.exists(target):
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(isi.strip() + "\n")
        print(f"[BUAT] {rel_path}")
    else:
        print(f"[LEWATI] {rel_path} (sudah ada, konfigurasi spesialis proyek dipertahankan)")


def pasang_agents_md():
    """
[ID]: Memasang atau menggabungkan aturan .agents/AGENTS.md secara non-destruktif.
    Jika file sudah ada dengan aturan kustom/spesialis, aturan lama 100% dipertahankan!

[EN]: Installs or merges the .agents/AGENTS.md rules non-destructively.
    If the file already exists with custom/specialized rules, the old rules are 100% preserved!
"""
    target = os.path.join(BASE_DIR, ".agents", "AGENTS.md")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if not os.path.exists(target):
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(KONTEN_AGENTS_MD.strip() + "\n")
        print("[BUAT] .agents/AGENTS.md")
    else:
        with open(target, "r", encoding="utf-8") as f:
            isi_lama = f.read()
        if "RTK Emulation" in isi_lama or "Token Efficiency" in isi_lama:
            print("[LEWATI] .agents/AGENTS.md (aturan spesialis & guardrails sudah lengkap)")
        else:
            guardrails_tambah = (
                "\n\n---\n\n## Vibe Coding & Token Efficiency Guardrails (Auto-Appended)\n"
                "- **Token Efficiency**: Never load whole large files; use sliced viewing (StartLine/EndLine, max 100 lines) focused on target functions.\n"
                "- **Exploration Order**: .agents/MAP.md -> grep_search -> sliced view_file. Use graphify-out/wiki only for cross-module relationships.\n"
                "- **RTK Emulation & CLI Guardrails**: Drastically prevent terminal stdout token bloat:\n"
                "  - Enforce quiet/summary flags where available (pip -q, git status -s, git diff --stat, pytest -q).\n"
                "  - Redirect verbose outputs to temp logs and inspect tails only (> scratch/tmp.log 2>&1; Get-Content ... -Tail 10).\n"
                "  - Prefer boolean/sentinel checks (Test-Path, (Get-ChildItem).Count, exit code) over dumping object listings.\n"
                "  - Never view files via shell commands (cat, type, Get-Content); strictly use native sliced view_file.\n"
                "  - Always compress remaining CLI output via pipes (Select -First 20, Select-String).\n"
                "- **Universal No Monolithizing**: STRICTLY FORBIDDEN to create monolithic scripts exceeding 300 lines. Separate concerns across dedicated packages.\n"
                "- **Direct Unicode Symbols**: NEVER use LaTeX math notation. Always use direct Unicode symbols (e.g. ->, •).\n"
            )
            with open(target, "a", encoding="utf-8", newline="\n") as f:
                f.write(guardrails_tambah)
            print("[GABUNG] .agents/AGENTS.md (aturan spesialis lama dipertahankan 100%, guardrails hemat token ditambahkan di bawah)")


# ==============================================================================
# KONTEN BERKAS .agents DAN ATURAN
# ==============================================================================

KONTEN_AGENTS_MD = """# Custom Agent Rules

## Communication & Language
- **User Explanations**: ALWAYS communicate in **Indonesian** during chatting and vibe coding.
- **Code Comments & Docstrings**: MUST be written in **Indonesian**.
- **Model Transparency & Confirmation**: ALWAYS explicitly state the active model being used (e.g., Primary Model Gemini Flash, Claude Sonnet 4.5, DeepSeek-R1, or Hermes) to confirm with the user before writing or editing code.

## Execution & Code Changes
- **Direct Code Changes**: Apply file edits directly without implementation_plan.md or walkthrough.md unless requested.
- **No Autonomous Testing on Updates**: DO NOT run self-tests, syntax checks (python -m py_compile), or builds after edits. Let user test manually first.
- **Autonomous Error Fixing**: Autonomously fix and verify runtime crashes/errors reported by user.
- **Proactive Command Execution**: Execute routine short terminal commands directly without asking confirmation.
- **Dual-Agent Role Specialization**:
  - **Primary Model (Gemini/IDE)**: Leverages its massive context window for heavy context lifting: broad file inspections, running CLI/tests, digesting extensive logs, distilling issues into dense snippets (50-200 lines), and executing precision code edits for FREE.
  - **Deep Reasoning & Thinking Offload (Automated Selection)**:
    - **Pure Reasoning & Architecture**: Autonomously route to `openrouter:tanya_openrouter` using `model="claude"` (Claude Sonnet 4.5) or `model="r1"` (DeepSeek-R1) for direct, zero-overhead algorithmic analysis, root-cause investigation, and architecture design.
    - **Multi-Step Agentic Tasks**: Route to `hermes_agent:delegasikan_ke_hermes` when autonomous multi-step problem solving, iterative probing, or Hermes sub-tools are required.
    - **Autonomous Routing & Interactive Model Selector**: When encountering complex architectural or reasoning tasks where the user DID NOT specify a model, trigger `ask_question` with cost & token estimation (DeepSeek-R1, Claude Sonnet, DeepSeek-V3, Gemini Flash IDE Free, Hermes) so user can choose before execution. If user explicitly mentions a model, route immediately.
- **Context Distillation Before Reasoning**: Never pass raw file dumps or voluminous log dumps to OpenRouter or Hermes; always distill essential context first to preserve OpenRouter credits and maximize reasoning accuracy.
- **Bilingual Token Optimization (English Bridge Pipeline)**:
  - When dispatching prompts to OpenRouter models (Claude Sonnet, DeepSeek-R1), the primary model MUST translate and compress user context into dense technical **English** to maximize BPE tokenizer efficiency (saving 30-50% in token volume compared to Indonesian/non-English) and improve reasoning quality.
  - Instruct external models to respond in concise technical English.
  - The primary model then translates, synthesizes, and presents the findings back to the user in **Indonesian** at zero token cost.
- **Reasoning Output Compression**: Always request concise, pre-aggregated reasoning summaries and logic diffs from external reasoning models for immediate implementation by the primary model.
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
- **Graphify Refresh**: Run graphify extract . --code-only on structural changes (file/folder renames, adding/removing classes/functions, major refactor). Inform user explicitly.

## Rules & Skills Maintenance
- **Language Format**: Write rules and skills in concise **English** without HTML comments or duplicate translations.
"""


KONTEN_RULES_ARCH = """---
trigger: always_on
description: Standar arsitektur bersih, batasan panjang berkas, dan efisiensi token.
globs: ["*.py"]
---

# Standar Clean Architecture & Efisiensi Token
1. **Batas Ukuran Berkas (Maksimal 250 - 300 Baris)**: Pisahkan menjadi sub-modul terfokus jika mendekati 300 baris.
2. **Separation of Concerns**: Pisahkan konfigurasi, logika domain inti, integrasi eksternal, dan orchestrator/entry point.
3. **Dokumentasi & Bahasa**: Semua komentar kode, docstring fungsi/modul, dan log teknis WAJIB menggunakan Bahasa Indonesia.
4. **Edit Tertarget**: Gunakan replace_file_content berbasis rentang baris spesifik, hindari menulis ulang seluruh berkas.
"""

KONTEN_RULES_GRAPHIFY = """---
trigger: always_on
description: Gunakan knowledge graph graphify-out/ untuk menjawab arsitektur proyek.
---

## Aturan Graphify
- Periksa knowledge graph lebih dulu bila graphify-out/graph.json ada: gunakan graphify query, graphify path, atau graphify explain.
- Telusuri graphify-out/wiki/index.md daripada membaca berkas mentah acak.
- Jalankan python vibe_tools/graphify_sync.py setelah modifikasi struktural.
- Bersihkan arsip lama di graphify-out/, pertahankan maksimal 2 arsip terbaru.
"""

KONTEN_SKILL_MODULAR = """---
name: modular-refactor
description: Panduan refactoring inkremental memecah skrip monolitik menjadi modular dengan kompatibilitas mundur 100%.
---

# Skill: Modular Refactor
1. **Zero Regression**: Pertahankan antarmuka publik dan file launcher lama menggunakan Facade Pattern.
2. **Inkremental**: Pindahkan satu domain dalam satu waktu ke folder subpaket.
3. **Docstring & Type Hints**: Tambahkan docstring Bahasa Indonesia dan type hints.
4. **Update Graph & Map**: Jalankan python vibe_tools/graphify_sync.py setelah refactor.
"""

KONTEN_SKILL_TEST = """---
name: unit-test-generator
description: Pembuatan unit test cepat dan terisolasi menggunakan pytest dan unittest.mock.
---

# Skill: Unit Test Generator
1. **Strict Mocking**: Selalu mock I/O, database, API, dan browser. Hindari ketergantungan nyata saat tes.
2. **Fokus & Ringkas**: Uji fungsi secara spesifik (panjang file test < 150 baris).
3. **Bahasa**: Gunakan docstring dan komentar dalam Bahasa Indonesia.
"""

KONTEN_WORKFLOW_GRAPHIFY = """---
name: graphify
description: Membangun knowledge graph navigasi untuk direktori proyek.
---

# Workflow: graphify
Jalankan perintah: python vibe_tools/graphify_sync.py
"""

# ==============================================================================
# KONTEN SKRIP OTOMASI PYTHON
# ==============================================================================

KONTEN_GRAPHIFY_MAP = '''"""
Modul pembuat peta file (graphify_map.py) untuk .agents/MAP.md.
Memindai kode proyek, lalu menyusun ulang MAP.md dengan aturan:
- Deskripsi yang sudah ada di MAP.md DIPERTAHANKAN (edit manual aman).
- File baru otomatis diisi dari docstring modul (atau penanda "(no description yet)").
- File yang sudah tidak ada otomatis dihapus dari peta.
- Jumlah baris diperbarui setiap kali dijalankan.
"""
import ast
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(BASE_DIR, ".agents", "MAP.md")

EKSTENSI_KODE = (".py", ".gs", ".bas", ".html", ".js", ".ts", ".jsx", ".tsx")
FOLDER_ABAIKAN = {
    ".git", ".vscode", ".agents", "__pycache__", "python_portable", "pw-browsers",
    "Arsip", "graphify-out", "hasil_foto_whatsapp", "node_modules", "venv", ".venv",
    "build_temp", "build", "dist",
}
BELUM_ADA_DESKRIPSI = "(no description yet)"
JUDUL_ROOT = "Root entry points (slim facades, never add implementation here)"

HEADER = (
    "# File Map (read this first, then open only the file you need)\\n\\n"
    "One line per module. Prefer `grep_search` + sliced `view_file` over reading whole files.\\n"
    "For relationships and call paths use `graphify-out/wiki/index.md` or `graphify query`.\\n"
    "Auto-maintained by `python graphify_update.py`: existing descriptions are kept, "
    "new files get a docstring-based line, deleted files are dropped.\\n"
)

NON_CODE = (
    "## Non-code (do not read)\\n"
    "`*.db`, `*.sqlite`, `*.log`, `graphify-out/graph.*`, `node_modules/`, `venv/`, `.venv/`\\n"
)

POLA_ITEM = re.compile(r"^- `([^`]+)`(?: \\(~?\\d+(?: lines)?\\))?(?: - (.*))?$")


def _hitung_baris(path: str) -> int:
    """Menghitung jumlah baris file teks (dibulatkan ke puluhan terdekat agar stabil)."""
    try:
        with open(path, "rb") as f:
            n = f.read().count(b"\\n") + 1
    except Exception:
        return 0
    return int(round(n / 10.0)) * 10


def _docstring_baris_pertama(path: str, nama: str) -> str:
    """Mengambil baris pertama docstring modul .py sebagai deskripsi awal."""
    if not path.endswith(".py"):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = ast.get_docstring(ast.parse(f.read())) or ""
    except Exception:
        return ""
    baris = doc.strip().splitlines()[0].strip() if doc.strip() else ""
    baris = re.sub(r"\\s*\\([^)]*\\.py\\)\\s*", " ", baris).strip(" .-")
    sisa = re.sub(r"(?i)^(modul|script|entry point root)\\s*:?\\s*", "", baris).strip()
    if not sisa or sisa.replace(".py", "").lower() == nama.replace(".py", "").lower():
        return ""
    return baris[:100]


def _baca_peta_lama() -> dict:
    """Membaca MAP.md lama: mempertahankan deskripsi manual yang sudah ada."""
    deskripsi, judul, urutan = {}, {}, []
    if not os.path.exists(MAP_PATH):
        return {"desk": deskripsi, "judul": judul, "urutan": urutan}
    seksi = None
    with open(MAP_PATH, "r", encoding="utf-8") as f:
        for baris in f.read().splitlines():
            if baris.startswith("## "):
                teks = baris[3:].strip()
                if teks.startswith("Root"):
                    seksi = ""
                    judul[""] = teks
                elif teks.startswith(("Non-code", "Launchers", "Other")):
                    seksi = None if not teks.startswith("Other") else ""
                else:
                    kunci = teks.split(" - ")[0].strip("`/ ").replace("\\\\", "/")
                    seksi = kunci
                    judul[kunci] = teks
                if seksi is not None and seksi not in urutan:
                    urutan.append(seksi)
                continue
            m = POLA_ITEM.match(baris)
            if m and seksi is not None and m.group(2):
                nama = m.group(1).replace("\\\\", "/")
                if nama.endswith("/") or m.group(2) == BELUM_ADA_DESKRIPSI:
                    continue
                rel = f"{seksi}/{nama}" if seksi else nama
                deskripsi[rel] = m.group(2)
    return {"desk": deskripsi, "judul": judul, "urutan": urutan}


def _pindai_kode() -> dict:
    """Memindai file kode proyek. Mengembalikan {seksi: [path relatif, ...]}."""
    hasil = {}
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        dirnames[:] = [d for d in dirnames if d not in FOLDER_ABAIKAN]
        rel_dir = os.path.relpath(dirpath, BASE_DIR).replace("\\\\", "/")
        rel_dir = "" if rel_dir == "." else rel_dir
        seksi = rel_dir.split("/")[0] if rel_dir else ""
        for nama in sorted(filenames):
            if not nama.lower().endswith(EKSTENSI_KODE) or nama == "__init__.py":
                continue
            if rel_dir == "" and not nama.endswith(".py"):
                continue
            rel = f"{rel_dir}/{nama}" if rel_dir else nama
            hasil.setdefault(seksi, []).append(rel)
    return hasil


def bangun_peta() -> tuple:
    """Menyusun teks MAP.md baru secara rapi dan modular."""
    lama = _baca_peta_lama()
    pindai = _pindai_kode()

    semua_baru = {p for daftar in pindai.values() for p in daftar}
    baru = sorted(p for p in semua_baru if p not in lama["desk"])
    dihapus = sorted(p for p in lama["desk"] if p not in semua_baru)

    urutan = [s for s in lama["urutan"] if s in pindai]
    urutan += sorted(s for s in pindai if s not in urutan)
    if "" in urutan:
        urutan.remove("")
    urutan.insert(0, "")

    baris_out = [HEADER.rstrip("\\n"), ""]
    tanpa_deskripsi = []
    for seksi in urutan:
        if seksi not in pindai:
            continue
        judul = lama["judul"].get(seksi) or (JUDUL_ROOT if seksi == "" else f"{seksi}/")
        baris_out.append(f"## {judul}")
        for rel in sorted(pindai[seksi]):
            nama = rel[len(seksi) + 1:] if seksi else rel
            desk = lama["desk"].get(rel) or _docstring_baris_pertama(
                os.path.join(BASE_DIR, rel.replace("/", os.sep)), os.path.basename(rel)
            )
            if not desk:
                desk = BELUM_ADA_DESKRIPSI
                tanpa_deskripsi.append(rel)
            n = _hitung_baris(os.path.join(BASE_DIR, rel.replace("/", os.sep)))
            info = f" (~{n} lines)" if n >= 300 else ""
            baris_out.append(f"- `{nama}`{info} - {desk}")
        baris_out.append("")

    baris_out.append(NON_CODE.rstrip("\\n"))
    bat = sorted(f for f in os.listdir(BASE_DIR) if f.lower().endswith(".bat"))
    if bat:
        baris_out.append("")
        baris_out.append("## Launchers")
        baris_out.append(", ".join(f"`{b}`" for b in bat))
    baris_out.append("")

    ringkasan = {"baru": baru, "dihapus": dihapus, "tanpa_deskripsi": tanpa_deskripsi}
    return "\\n".join(baris_out), ringkasan


def perbarui_peta() -> dict:
    """Menulis MAP.md hasil bangun_peta()."""
    teks, ringkasan = bangun_peta()
    os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
    with open(MAP_PATH, "w", encoding="utf-8", newline="\\n") as f:
        f.write(teks)
    return ringkasan


if __name__ == "__main__":
    r = perbarui_peta()
    print(f"[Peta] Berhasil diperbarui (.agents/MAP.md). Baru: {len(r['baru'])}, Dihapus: {len(r['dihapus'])}")
'''

KONTEN_GRAPHIFY_UPDATE = '''"""
Skrip sekali klik untuk memperbarui knowledge graph (graphify), wiki, dan peta file.
Urutan: graphify update . -> graphify export wiki -> update .agents/MAP.md -> verifikasi wiki
        -> rapikan folder arsip (maks 2 terbaru).
Jalankan dengan klik ganda atau: python graphify_update.py [--no-pause]
"""
import json
import os
import re
import shutil
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "graphify-out")
MAKS_ARSIP = 2

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def cari_perintah_graphify() -> list:
    """Mencari executable graphify di PATH atau fallback python -m graphify."""
    exe = shutil.which("graphify")
    if exe:
        return [exe]
    return [sys.executable, "-m", "graphify"]


def jalankan(langkah: str, args: list) -> bool:
    """Menjalankan langkah perintah sub-proses."""
    print(f"\\n=== {langkah} ===")
    print("$ " + " ".join(args))
    try:
        hasil = subprocess.run(args, cwd=BASE_DIR)
    except FileNotFoundError:
        print("[ERROR] graphify tidak ditemukan. Instal dulu: pip install -q graphifyy")
        return False
    if hasil.returncode != 0:
        print(f"[ERROR] Langkah '{langkah}' gagal (exit code {hasil.returncode}).")
        return False
    return True


def rapikan_arsip():
    """Menghapus folder arsip bertanggal lama di graphify-out/, menyisakan MAKS_ARSIP."""
    if not os.path.isdir(OUT_DIR):
        return
    pola = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")
    arsip = sorted(
        d for d in os.listdir(OUT_DIR)
        if pola.match(d) and os.path.isdir(os.path.join(OUT_DIR, d))
    )
    lama = arsip[:-MAKS_ARSIP] if len(arsip) > MAKS_ARSIP else []
    for nama in lama:
        try:
            shutil.rmtree(os.path.join(OUT_DIR, nama))
            print(f"[Arsip] Dihapus: graphify-out/{nama}")
        except Exception as e:
            print(f"[Arsip] Gagal menghapus {nama}: {e}")
    if not lama:
        print(f"[Arsip] Tidak ada arsip yang perlu dihapus ({len(arsip)} arsip).")


def perbarui_peta_file() -> bool:
    """Memperbarui .agents/MAP.md."""
    print("\\n=== 3/3 Update peta file (.agents/MAP.md) ===")
    try:
        from graphify_map import perbarui_peta
        r = perbarui_peta()
    except Exception as e:
        print(f"[ERROR] Gagal memperbarui MAP.md: {e}")
        return False
    print(f"[Peta] Baru: {len(r['baru'])} | Dihapus: {len(r['dihapus'])}")
    for p in r["baru"]:
        print(f"   + {p}")
    for p in r["dihapus"]:
        print(f"   - {p}")
    return True


def verifikasi_wiki() -> bool:
    """Memastikan sinkronisasi wiki dengan graph.json."""
    graph_path = os.path.join(OUT_DIR, "graph.json")
    index_path = os.path.join(OUT_DIR, "wiki", "index.md")
    if not (os.path.exists(graph_path) and os.path.exists(index_path)):
        print("[Verifikasi] graph.json atau wiki/index.md belum ada (akan terbentuk saat update pertama).")
        return True
    try:
        with open(graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        n_graph = len(data.get("nodes", []))
        with open(index_path, "r", encoding="utf-8") as f:
            m = re.search(r"\\*\\*(\\d+) nodes", f.read())
        n_wiki = int(m.group(1)) if m else -1
    except Exception:
        return True
    sinkron = n_graph == n_wiki
    segar = os.path.getmtime(index_path) >= os.path.getmtime(graph_path)
    print(f"[Verifikasi] Node graph={n_graph} | Node wiki={n_wiki} | Wiki sinkron={sinkron}")
    return sinkron and segar


def main():
    gf = cari_perintah_graphify()
    sukses = jalankan("1/3 Update graph (AST-only)", gf + ["update", "."])
    if sukses:
        sukses = jalankan("2/3 Export wiki", gf + ["export", "wiki"])
    if sukses:
        sukses = perbarui_peta_file()
    if sukses:
        print("\\n=== Verifikasi wiki ===")
        verifikasi_wiki()
        print("\\n=== Rapikan arsip ===")
        rapikan_arsip()
        print("\\n[OK] Graph, wiki, dan .agents/MAP.md berhasil diperbarui!")
    else:
        print("\\n[CATATAN] Pembaruan graphify dilewati/gagal. MAP.md tetap diperbarui jika file kode ada.")
        perbarui_peta_file()

    if "--no-pause" not in sys.argv and sys.stdin and sys.stdin.isatty():
        input("\\nTekan Enter untuk menutup...")
    sys.exit(0 if sukses else 1)


if __name__ == "__main__":
    main()
'''

KONTEN_PUSH_GITHUB = '''"""
Script: push_github.py
Deskripsi: Script otomasi git add, commit, dan push manual ke GitHub secara aman.
Dijalankan dengan perintah: python push_github.py
"""
import os
import subprocess
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_git(args, capture_output=True, check=True):
    """Menjalankan perintah git di direktori proyek."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=BASE_DIR,
            capture_output=capture_output,
            text=True,
            check=check,
            encoding="utf-8",
            errors="replace"
        )
        return res.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        err = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(err)


def is_git_repo():
    """Mengecek apakah direktori sudah diinisialisasi git."""
    return os.path.exists(os.path.join(BASE_DIR, ".git"))


def get_remote_url():
    """Mengecek remote origin url."""
    try:
        return run_git(["remote", "get-url", "origin"])
    except Exception:
        return None


def bersihkan_desktop_ini_git():
    """Membersihkan file desktop.ini di .git yang sering dibuat otomatis oleh Google Drive."""
    git_dir = os.path.join(BASE_DIR, ".git")
    if os.path.exists(git_dir):
        import stat
        import pathlib
        for p in pathlib.Path(git_dir).rglob("*"):
            if p.name.lower() == "desktop.ini":
                try:
                    os.chmod(p, stat.S_IWRITE)
                    os.remove(p)
                except Exception:
                    pass


def main():
    print("=" * 65)
    print("      GIT PUSH MANUAL KE GITHUB")
    print("=" * 65)
    print(f"Direktori: {BASE_DIR}\\n")

    bersihkan_desktop_ini_git()

    if not is_git_repo():
        print("[INFO] Repository Git belum diinisialisasi.")
        konfirm = input("Inisialisasi git sekarang? (y/n) [default: y]: ").strip().lower()
        if konfirm in ["", "y", "yes"]:
            run_git(["init"], capture_output=False)
            run_git(["branch", "-M", "main"], capture_output=False)
            print("[SUCCESS] Git init berhasil (Branch: main).\\n")
        else:
            print("[INFO] Dibatalkan.")
            return

    remote_url = get_remote_url()
    if not remote_url:
        print("[WARNING] Remote origin belum terdaftar.")
        url_input = input("Masukkan URL GitHub (misal https://github.com/USER/REPO.git): ").strip()
        if not url_input:
            print("[ERROR] URL kosong. Dibatalkan.")
            return
        run_git(["remote", "add", "origin", url_input], capture_output=False)
        print(f"[SUCCESS] Remote ditambahkan: {url_input}\\n")
    else:
        print(f"Remote URL: {remote_url}\\n")

    status_output = run_git(["status", "--short"])
    if not status_output:
        print("[INFO] Tidak ada perubahan berkas yang perlu di-commit.")
        try:
            unpushed = run_git(["log", "origin/main..HEAD", "--oneline"])
            if unpushed:
                print(f"[INFO] Ditemukan commit lokal yang belum terkirim:\\n{unpushed}")
                tanya_push = input("Push commit tersebut ke GitHub sekarang? (y/n) [default: y]: ").strip().lower()
                if tanya_push in ["", "y", "yes"]:
                    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=BASE_DIR, check=True)
                    print("\\n[SUCCESS] Berhasil push ke GitHub!")
                return
        except Exception:
            pass
        print("Workspace Anda sudah up-to-date!")
        return

    print("Daftar berkas yang berubah:")
    print("-" * 45)
    for line in status_output.splitlines()[:25]:
        print(f"  {line}")
    if len(status_output.splitlines()) > 25:
        print(f"  ... dan {len(status_output.splitlines()) - 25} berkas lainnya.")
    print("-" * 45)

    waktu_skrg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pesan_default = f"Update code: {waktu_skrg}"
    print(f"\\nPesan commit default: '{pesan_default}'")
    pesan_input = input("Masukkan pesan commit (Enter untuk default): ").strip()
    pesan_commit = pesan_input if pesan_input else pesan_default

    print("\\n[1/3] Menambahkan berkas ke staging (git add .) ...")
    run_git(["add", "."], capture_output=False)

    print(f"[2/3] Membuat commit: '{pesan_commit}' ...")
    try:
        run_git(["commit", "-m", pesan_commit], capture_output=False)
    except Exception as e:
        print(f"[WARNING] Kendala commit: {e}")

    print("[3/3] Mengunggah ke GitHub (git push origin main) ...")
    try:
        res = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=BASE_DIR)
        if res.returncode == 0:
            print("\\n" + "=" * 65)
            print("  [SUCCESS] KODE BERHASIL DI-PUSH KE GITHUB SECARA TUNTAS!")
            print("=" * 65)
        else:
            print(f"\\n[ERROR] Gagal push (Exit code: {res.returncode}).")
    except Exception as e:
        print(f"\\n[ERROR] Gagal push ke remote: {e}")


if __name__ == "__main__":
    main()
'''


# ==============================================================================
# SCHEMA DEFAULT MCP SERVER ANTIGRAVITY (FALLBACK)
# ==============================================================================

KONTEN_SCHEMA_HERMES = r'''{
  "name": "delegasikan_ke_hermes",
  "description": "Kirim tugas ke Hermes Agent lokal (background worker mandiri). Hermes dapat mengeksekusi terminal command/test, membaca & menyisir file luas, mencari regex di direktori kerja, scraping web, atau eksplorasi kode secara otonom dengan model reasoning DeepSeek R1 tanpa membuang token Claude/GPT. Hasil akan otomatis diringkas padat agar efisien di context window.",
  "parameters": {
    "properties": {
      "direktori_kerja": {
        "default": "",
        "title": "Direktori Kerja",
        "type": "string"
      },
      "model": {
        "default": "deepseek/deepseek-r1",
        "title": "Model",
        "type": "string"
      },
      "tugas": {
        "title": "Tugas",
        "type": "string"
      }
    },
    "required": [
      "tugas"
    ],
    "title": "delegasikan_ke_hermesArguments",
    "type": "object"
  }
}'''

KONTEN_SCHEMA_TANYA_OR = r'''{
  "name": "tanya_openrouter",
  "description": "Mengirim pertanyaan atau tugas ke berbagai model AI melalui OpenRouter API. Mendukung alias cerdas seperti 'r1', 'claude', 'sonnet', 'deepseek', 'v3', 'gpt4o', 'qwen', 'free', dsb. Dilengkapi pengaman batas pengeluaran harian $1/hari.",
  "parameters": {
    "properties": {
      "model": {
        "default": "deepseek",
        "title": "Model",
        "type": "string"
      },
      "prompt": {
        "title": "Prompt",
        "type": "string"
      },
      "system_prompt": {
        "default": "",
        "title": "System Prompt",
        "type": "string"
      }
    },
    "required": [
      "prompt"
    ],
    "title": "tanya_openrouterArguments",
    "type": "object"
  }
}'''

KONTEN_SCHEMA_DAFTAR_OR = r'''{
  "name": "daftar_model_rekomendasi",
  "description": "Menampilkan katalog model AI unggulan, alias pendek yang didukung, serta perkiraan biaya per 1 juta token.",
  "parameters": {
    "properties": {},
    "title": "daftar_model_rekomendasiArguments",
    "type": "object"
  }
}'''

KONTEN_SCHEMA_CEK_OR = r'''{
  "name": "cek_koneksi_openrouter",
  "description": "Mengecek validitas API Key OpenRouter serta status saldo, limit pemakaian, dan kuota rate limit akun.",
  "parameters": {
    "properties": {},
    "title": "cek_koneksi_openrouterArguments",
    "type": "object"
  }
}'''


def pasang_dependensi_python():
    """
[ID]: Memeriksa dan menginstal secara otomatis seluruh pustaka Python yang dibutuhkan ekosistem:
    - mcp (untuk server FastMCP / MCPServer Antigravity)
    - requests (untuk klien OpenRouter)
    - graphifyy (untuk visualisasi dan ekstraksi knowledge graph)
    - Dependensi inti Hermes Agent (ruamel.yaml, psutil, rich, tomli-w, dll.)

[EN]: Checks and automatically installs all required Python libraries for the ecosystem:
    - mcp (for FastMCP / MCPServer Antigravity)
    - requests (for OpenRouter client)
    - graphifyy (for knowledge graph visualization and extraction)
    - Core dependencies of Hermes Agent (ruamel.yaml, psutil, rich, tomli-w, etc.)
"""
    print("\n[INFO] Memeriksa paket Python esensial...")
    paket_wajib = [
        ("mcp", "mcp"),
        ("requests", "requests"),
        ("graphify", "graphifyy"),
        ("ruamel.yaml", "ruamel.yaml"),
        ("psutil", "psutil"),
        ("rich", "rich"),
        ("tomli_w", "tomli-w"),
        ("fire", "fire"),
        ("tenacity", "tenacity"),
        ("jinja2", "jinja2"),
        ("markdown", "markdown"),
        ("tzdata", "tzdata"),
        ("prompt_toolkit", "prompt_toolkit"),
        ("croniter", "croniter"),
        ("pathspec", "pathspec"),
        ("snowballstemmer", "snowballstemmer"),
    ]
    kurang = []
    for modul, pkg in paket_wajib:
        try:
            __import__(modul)
        except ImportError:
            kurang.append(pkg)

    if kurang:
        print(f"[AUTO-INSTALL] Memasang paket Python yang belum ada ({len(kurang)} paket): {', '.join(kurang)}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + kurang, check=True)
            print("[OK] Seluruh paket Python berhasil dipasang otomatis.")
        except Exception as e:
            print(f"[WARNING] Gagal memasang otomatis via pip: {e}")
            print(f"          Silakan pasang manual: pip install {' '.join(kurang)}")
    else:
        print("[OK] Seluruh paket Python esensial (mcp, requests, graphifyy, hermes deps) sudah lengkap.")


def sinkronkan_openrouter_api_key(gemini_dir, gemini_config_dir) -> str:
    """
[ID]: Mendeteksi OpenRouter API Key dari berbagai sumber lokal.
    Jika ditemukan di salah satu sumber, otomatis menyinkronkannya ke semua sumber lain:
    1. Environment Variable: OPENROUTER_API_KEY
    2. ~/.gemini/openrouter_key.txt
    3. ~/.gemini/config/mcp_config.json
    4. %LOCALAPPDATA%/hermes/.env

[EN]: Detects OpenRouter API Key from various local sources.
If found in any source, automatically synchronizes it to all other sources:
1. Environment Variable: OPENROUTER_API_KEY
2. ~/.gemini/openrouter_key.txt
3. ~/.gemini/config/mcp_config.json
4. %LOCALAPPDATA%/hermes/.env
"""
    from pathlib import Path
    key_ditemukan = ""

    # 1. Cek ENV
    env_k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_k and env_k.startswith("sk-or-v1-"):
        key_ditemukan = env_k

    # 2. Cek openrouter_key.txt
    key_file = gemini_dir / "openrouter_key.txt"
    if not key_ditemukan and key_file.exists():
        try:
            for l in key_file.read_text(encoding="utf-8").splitlines():
                l = l.strip()
                if l.startswith("sk-or-v1-"):
                    key_ditemukan = l
                    break
        except Exception:
            pass

    # 3. Cek mcp_config.json
    mcp_json = gemini_config_dir / "mcp_config.json"
    if not key_ditemukan and mcp_json.exists():
        try:
            import json
            cfg = json.loads(mcp_json.read_text(encoding="utf-8"))
            k = cfg.get("mcpServers", {}).get("openrouter", {}).get("env", {}).get("OPENROUTER_API_KEY", "").strip()
            if k.startswith("sk-or-v1-"):
                key_ditemukan = k
        except Exception:
            pass

    # 4. Cek hermes .env
    hermes_env = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "hermes" / ".env"
    if not key_ditemukan and hermes_env.exists():
        try:
            for l in hermes_env.read_text(encoding="utf-8").splitlines():
                l = l.strip()
                if l.startswith("OPENROUTER_API_KEY="):
                    val = l.split("=", 1)[1].strip()
                    if val.startswith("sk-or-v1-"):
                        key_ditemukan = val
                        break
        except Exception:
            pass

    # Jika belum ada di mana-mana, tanyakan secara interaktif jika di terminal
    if not key_ditemukan and sys.stdin and sys.stdin.isatty():
        print("\n[?] OpenRouter API Key belum terdeteksi di sistem.")
        print("    Kunci ini diperlukan untuk model Deep Reasoning (DeepSeek-R1 / Claude Sonnet).")
        try:
            user_input = input("    Masukkan OpenRouter API Key (sk-or-v1-...) [Tekan Enter untuk lewati]: ").strip()
            if user_input.startswith("sk-or-v1-"):
                key_ditemukan = user_input
        except Exception:
            pass

    # Sinkronisasi ke semua tempat jika ada key
    if key_ditemukan:
        try:
            key_file.write_text(f"# OpenRouter API Key\n{key_ditemukan}\n", encoding="utf-8")
        except Exception:
            pass
        try:
            hermes_env.parent.mkdir(parents=True, exist_ok=True)
            hermes_env.write_text(f"OPENROUTER_API_KEY={key_ditemukan}\n", encoding="utf-8")
        except Exception:
            pass
        print(f"[OK] OpenRouter API Key tersinkronisasi ({key_ditemukan[:14]}...{key_ditemukan[-4:]}).")
    else:
        print("[INFO] OpenRouter API Key dilewati. Anda dapat mengisinya nanti di ~/.gemini/openrouter_key.txt.")

    return key_ditemukan


def konfigurasi_root_gemini(api_key: str):
    """
[ID]: Mengonfigurasi direktori root Antigravity IDE (~/.gemini) secara 100% dinamis dan portabel:
    - Memasang script server openrouter_mcp.py & hermes_mcp.py
    - Memasang schema MCP Antigravity di ~/.gemini/antigravity-ide/mcp/
    - Memasang global skill graphify di ~/.gemini/config/skills/graphify/SKILL.md
    - Mendaftarkan mcpServers di ~/.gemini/config/mcp_config.json dengan path Python dinamis.

[EN]: Configures the Antigravity IDE root directory (~/.gemini) to be 100% dynamic and portable:
    - Installs server scripts openrouter_mcp.py & hermes_mcp.py
    - Installs Antigravity MCP schema in ~/.gemini/antigravity-ide/mcp/
    - Installs global skill graphify in ~/.gemini/config/skills/graphify/SKILL.md
    - Registers mcpServers in ~/.gemini/config/mcp_config.json with dynamic Python paths.
"""
    import json
    import shutil
    from pathlib import Path

    print("\n[INFO] Mengonfigurasi Root Antigravity IDE (~/.gemini)...")

    user_home = Path.home()
    gemini_dir = user_home / ".gemini"
    gemini_config_dir = gemini_dir / "config"
    antigravity_mcp_dir = gemini_dir / "antigravity-ide" / "mcp"
    skills_dir = gemini_config_dir / "skills" / "graphify"

    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_config_dir.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)
    (antigravity_mcp_dir / "hermes_agent").mkdir(parents=True, exist_ok=True)
    (antigravity_mcp_dir / "openrouter").mkdir(parents=True, exist_ok=True)

    vibe_tools_dir = Path(BASE_DIR) / "vibe_tools"

    # 1. Pasang MCP server scripts
    for script_name in ["openrouter_mcp.py", "hermes_mcp.py"]:
        src = vibe_tools_dir / script_name
        dest = gemini_dir / script_name
        if src.exists():
            shutil.copy2(src, dest)
            print(f"[SALIN] {script_name} -> {dest}")

    # 2. Pasang MCP Tool Schemas
    schema_map = {
        "hermes_agent/delegasikan_ke_hermes.json": KONTEN_SCHEMA_HERMES,
        "openrouter/tanya_openrouter.json": KONTEN_SCHEMA_TANYA_OR,
        "openrouter/daftar_model_rekomendasi.json": KONTEN_SCHEMA_DAFTAR_OR,
        "openrouter/cek_koneksi_openrouter.json": KONTEN_SCHEMA_CEK_OR,
    }
    for rel_path, default_konten in schema_map.items():
        src = vibe_tools_dir / "mcp_schemas" / rel_path
        dest = antigravity_mcp_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dest)
        elif not dest.exists():
            dest.write_text(default_konten.strip(), encoding="utf-8")
        print(f"[SCHEMA] {dest.name} aktif di IDE.")

    # 3. Pasang Global Skill Graphify
    skill_dest = skills_dir / "SKILL.md"
    skill_src = vibe_tools_dir / "graphify_SKILL.md"
    if skill_src.exists():
        shutil.copy2(skill_src, skill_dest)
        print(f"[SKILL] Global /graphify skill terpasang di {skill_dest}")

    # 4. Daftarkan ke mcp_config.json dengan path Python dinamis
    mcp_config_file = gemini_config_dir / "mcp_config.json"
    cfg = {"mcpServers": {}}
    if mcp_config_file.exists():
        try:
            cfg = json.loads(mcp_config_file.read_text(encoding="utf-8"))
            if "mcpServers" not in cfg:
                cfg["mcpServers"] = {}
        except Exception:
            cfg = {"mcpServers": {}}

    python_bin = sys.executable.replace("\\", "/")
    or_script_path = (gemini_dir / "openrouter_mcp.py").as_posix()
    hermes_script_path = (gemini_dir / "hermes_mcp.py").as_posix()

    cfg["mcpServers"]["openrouter"] = {
        "command": python_bin,
        "args": [or_script_path],
        "env": {
            "OPENROUTER_API_KEY": api_key or "TEMPEL_API_KEY_DISINI",
            "OPENROUTER_DAILY_LIMIT": "1.00"
        },
        "disabled": False
    }

    cfg["mcpServers"]["hermes_agent"] = {
        "command": python_bin,
        "args": [hermes_script_path],
        "disabled": False
    }

    mcp_config_file.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] mcp_config.json berhasil dikonfigurasi (OpenRouter & Hermes Agent aktif).")


def pasang_atau_sinkronkan_hermes(api_key: str):
    """
[ID]: Memeriksa ketersediaan Hermes Agent CLI.
    Jika belum ada, otomatis clone repositori resmi dan pasang via pip install -e .
    Mengonfigurasi default model ke 'deepseek/deepseek-chat' dan kredensial API.

[EN]: Checks the availability of the Hermes Agent CLI.
If not present, automatically clones the official repository and installs via `pip install -e .`.
Configures the default model to 'deepseek/deepseek-chat' and sets up API credentials.
"""
    import shutil
    from pathlib import Path

    print("\n[INFO] Memeriksa status instalasi Hermes Agent CLI...")

    hermes_bin = shutil.which("hermes") or shutil.which("hermes.exe")
    if not hermes_bin:
        script_candidate = Path(sys.executable).parent / "Scripts" / "hermes.exe"
        if script_candidate.exists():
            hermes_bin = str(script_candidate)

    if not hermes_bin:
        print("[AUTO-SETUP] Hermes Agent belum terpasang. Memasang otomatis...")
        user_home = Path.home()
        target_dir = Path("C:/hermes_env") if Path("C:/").exists() else (user_home / "hermes_env")
        repo_dir = target_dir / "hermes-agent"
        target_dir.mkdir(parents=True, exist_ok=True)

        if not repo_dir.exists():
            print(f"  Cloning repositori NousResearch/hermes-agent ke {repo_dir}...")
            try:
                subprocess.run(f'git clone https://github.com/NousResearch/hermes-agent.git "{repo_dir}"', shell=True, check=True)
                print("  [OK] Clone berhasil.")
            except Exception as e:
                print(f"  [WARNING] Gagal clone hermes-agent: {e}. Lewati pemasangan CLI.")
                return

        if repo_dir.exists():
            print("  Memasang package hermes-agent via pip...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=str(repo_dir), check=True)
                print("  [OK] Package hermes-agent berhasil dipasang.")
                hermes_bin = shutil.which("hermes") or str(Path(sys.executable).parent / "Scripts" / "hermes.exe")
            except Exception as e:
                print(f"  [WARNING] Gagal pip install hermes: {e}")

    if hermes_bin:
        print(f"[OK] Hermes Agent CLI siap: {hermes_bin}")
        try:
            subprocess.run([hermes_bin, "config", "set", "model", "deepseek/deepseek-chat"], check=True, capture_output=True)
            print("[OK] Model default Hermes disetel ke 'deepseek/deepseek-chat'.")
        except Exception:
            pass

    if api_key:
        local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        hermes_env_file = local_app_data / "hermes" / ".env"
        hermes_env_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            hermes_env_file.write_text(f"OPENROUTER_API_KEY={api_key}\n", encoding="utf-8")
        except Exception:
            pass


def main():
    from pathlib import Path
    print("=" * 65)
    print("  MEMASANG EKOSISTEM VIBE CODING & AGENT CUSTOMIZATION")
    print("=" * 65)
    print(f"Target Direktori: {BASE_DIR}")
    print(f"Python Runtime   : {sys.executable}\n")

    user_home = Path.home()
    gemini_dir = user_home / ".gemini"
    gemini_config_dir = gemini_dir / "config"

    # 1. Konfigurasi Workspace .agents (idempoten & non-destruktif)
    pasang_agents_md()
    buat_berkas(".agents/workflows/graphify.md", KONTEN_WORKFLOW_GRAPHIFY)

    # 2. Skrip Python Otomasi & Panduan Ekosistem AI
    buat_berkas("vibe_tools/sync_universal.py", baca_skrip_lokal("sync_universal.py"))
    buat_berkas("vibe_tools/graphify_sync.py", baca_skrip_lokal("graphify_sync.py"))
    buat_berkas("vibe_tools/push_to_github.py", baca_skrip_lokal("push_to_github.py") or KONTEN_PUSH_GITHUB)
    buat_berkas("vibe_tools/install_hermes_antigravity.py", baca_skrip_lokal("install_hermes_antigravity.py"))
    buat_berkas("vibe_tools/install_openrouter_mcp.py", baca_skrip_lokal("install_openrouter_mcp.py"))
    buat_berkas("vibe_tools/PANDUAN_HERMES_ANTIGRAVITY.md", baca_skrip_lokal("PANDUAN_HERMES_ANTIGRAVITY.md"))
    buat_berkas("vibe_tools/OPENROUTER_MCP_GUIDE.md", baca_skrip_lokal("OPENROUTER_MCP_GUIDE.md"))
    buat_berkas("vibe_tools/Prompt_AI.md", baca_skrip_lokal("Prompt_AI.md"))
    buat_berkas("vibe_tools/PANDUAN_SETUP_VIBE_CODING_BARU.md", baca_skrip_lokal("PANDUAN_SETUP_VIBE_CODING_BARU.md"))
    buat_berkas("vibe_tools/TUTORIAL_TESTING_ASK_QUESTION.md", baca_skrip_lokal("TUTORIAL_TESTING_ASK_QUESTION.md"))
    buat_berkas("vibe_tools/graphify_SKILL.md", baca_skrip_lokal("graphify_SKILL.md"))
    buat_berkas("vibe_tools/openrouter_mcp.py", baca_skrip_lokal("openrouter_mcp.py"))
    buat_berkas("vibe_tools/hermes_mcp.py", baca_skrip_lokal("hermes_mcp.py"))
    buat_berkas("vibe_tools/cost_estimator.py", baca_skrip_lokal("cost_estimator.py"))
    buat_berkas("vibe_tools/docstring_translator.py", baca_skrip_lokal("docstring_translator.py"))
    buat_berkas("vibe_tools/TUTORIAL_DOCSTRING_TRANSLATOR.md", baca_skrip_lokal("TUTORIAL_DOCSTRING_TRANSLATOR.md"))
    buat_berkas("vibe_tools/install_rea_mcp.py", baca_skrip_lokal("install_rea_mcp.py"))
    buat_berkas("vibe_tools/PANDUAN_REA_MCP.md", baca_skrip_lokal("PANDUAN_REA_MCP.md"))
    buat_berkas("vibe_tools/README.md", baca_skrip_lokal("README.md"))
    buat_berkas("vibe_tools/README_EN.md", baca_skrip_lokal("README_EN.md"))
    buat_berkas("vibe_tools/TUTORIAL_SINKRONISASI_VIBE_TOOLS.md", baca_skrip_lokal("TUTORIAL_SINKRONISASI_VIBE_TOOLS.md"))
    buat_berkas("vibe_tools/patch_continue_autonomous.py", baca_skrip_lokal("patch_continue_autonomous.py"))
    buat_berkas("vibe_tools/setup_roo_hybrid.py", baca_skrip_lokal("setup_roo_hybrid.py"))

    # 2b. Pasang REA MCP (opsional, jika Node.js tersedia)
    import shutil as _shutil
    if _shutil.which("npx") or _shutil.which("node"):
        print("\n[INFO] Node.js terdeteksi - mencoba memasang REA MCP (Reverse Engineer Anything)...")
        _rea_installer = os.path.join(BASE_DIR, "vibe_tools", "install_rea_mcp.py")
        if os.path.exists(_rea_installer):
            subprocess.run([sys.executable, _rea_installer], cwd=BASE_DIR)
        else:
            print("[SKIP] vibe_tools/install_rea_mcp.py belum ada di folder ini - skip REA MCP.")
    else:
        print("[SKIP] Node.js tidak ditemukan di PATH - skip pemasangan REA MCP.")

    # 3. Auto-Install seluruh dependensi Python yang belum terpasang
    pasang_dependensi_python()

    # 4. Sinkronisasi API Key OpenRouter dari berbagai sumber lokal
    api_key = sinkronkan_openrouter_api_key(gemini_dir, gemini_config_dir)

    # 5. Konfigurasi Root Antigravity IDE (~/.gemini) secara 100% dinamis & portabel
    konfigurasi_root_gemini(api_key)

    # 5b. Sinkronisasi Universal Skills & Rules via NTFS Junction ke ~/.gemini/config
    try:
        sys.path.insert(0, os.path.join(BASE_DIR, "vibe_tools"))
        import sync_universal
        sync_universal.sinkronisasi_universal()
        import setup_roo_hybrid
        setup_roo_hybrid.pasang_roo_hybrid(target_path=BASE_DIR, setup_ollama=False)
    except Exception as e:
        print(f"[WARNING] Sinkronisasi universal otomatis dilewati: {e}")

    # 6. Pasang atau verifikasi Hermes Agent CLI
    pasang_atau_sinkronkan_hermes(api_key)

    # 7. Jalankan pemetaan awal .agents/MAP.md
    print("\n[INFO] Membangun peta berkas awal (.agents/MAP.md)...")
    try:
        sys.path.insert(0, os.path.join(BASE_DIR, "vibe_tools"))
        import graphify_sync
        r = graphify_sync.perbarui_peta(BASE_DIR)
        print(f"[OK] Peta awal terbentuk dengan {len(r.get('baru', []))} entri berkas.")
    except Exception as e:
        print(f"[WARNING] Belum dapat memetakan berkas secara otomatis: {e}")

    print("\n" + "=" * 65)
    print("  [SELESAI] SELURUH EKOSISTEM VIBE CODING SIAP DIGUNAKAN 100%!")
    print("  (Restart Antigravity IDE sekali agar semua tool MCP terdeteksi)")
    print("=" * 65)


if __name__ == "__main__":
    main()
