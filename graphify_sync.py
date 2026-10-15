"""
[ID]: Skrip Terpadu Knowledge Graph & Peta Berkas Proyek (graphify_sync.py).
Menggabungkan pembaruan Knowledge Graph (graphify) dan generator AST .agents/MAP.md menjadi 1 tool portabel.

Penggunaan:
    python graphify_sync.py                # Full pipeline (graph -> wiki -> MAP.md -> verifikasi -> rapikan)
    python graphify_sync.py --map-only     # Hanya perbarui peta .agents/MAP.md (sangat cepat, tanpa graphify)
    python graphify_sync.py --graph-only   # Hanya perbarui graphify & ekspor wiki
    python graphify_sync.py --no-pause     # Tanpa jeda tekan Enter di akhir

[EN]: Integrated Knowledge Graph & Project File Map Script (graphify_sync.py).
Combines Knowledge Graph updates (graphify) and AST generator .agents/MAP.md into a single portable tool.

Usage:
    python graphify_sync.py                # Full pipeline (graph -> wiki -> MAP.md -> verify -> clean)
    python graphify_sync.py --map-only     # Update only the .agents/MAP.md map (very fast, no graphify)
    python graphify_sync.py --graph-only   # Update only graphify & export wiki
    python graphify_sync.py --no-pause     # Skip Enter key pause at the end
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys

# Konfigurasi encoding konsol Windows agar aman UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

EKSTENSI_KODE = (".py", ".gs", ".bas", ".html")
FOLDER_ABAIKAN = {
    ".git", ".vscode", ".agents", "__pycache__", "python_portable", "pw-browsers",
    "Arsip", "graphify-out", "hasil_foto_whatsapp", "node_modules", "venv", ".venv",
    "Scrapper_new_acmt", "ITO", "build_temp", "build", "dist",
}
BELUM_ADA_DESKRIPSI = "(no description yet)"
JUDUL_ROOT = "Root entry points (slim facades, never add implementation here)"
HEADER = (
    "# File Map (read this first, then open only the file you need)\n\n"
    "One line per module. Prefer `grep_search` + sliced `view_file` over reading whole files.\n"
    "For relationships and call paths use `graphify-out/wiki/index.md` or `graphify query`.\n"
    "Auto-maintained by `graphify_sync.py`: existing descriptions are kept, "
    "new files get a docstring-based line, deleted files are dropped.\n"
)
NON_CODE = (
    "## Non-code (do not read)\n"
    "`LPB.json` (48 MB), `LPB.xls(x)`, `*.db`, `graphify-out/graph.*`, `monitor/monitor_cache.db`,\n"
    "`python_portable/`, `pw-browsers/`, `Arsip/`, `hasil_foto_whatsapp/`\n"
)
POLA_ITEM = re.compile(r"^- `([^`]+)`(?: \(~?\d+(?: lines)?\))?(?: - (.*))?$")
MAKS_ARSIP = 2


def deteksi_root_proyek(arg_root: str = None) -> str:
    """
[ID]: Mendeteksi direktori root proyek secara otomatis dan portabel.
[EN]: Automatically and portably detects the project root directory.
"""
    if arg_root and os.path.isdir(arg_root):
        return os.path.abspath(arg_root)
    cwd = os.path.abspath(os.getcwd())
    if os.path.exists(os.path.join(cwd, ".agents")) or os.path.exists(os.path.join(cwd, ".git")):
        return cwd
    skrip_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(skrip_dir)
    if os.path.exists(os.path.join(skrip_dir, ".agents")) or os.path.exists(os.path.join(skrip_dir, ".git")):
        return skrip_dir
    if os.path.exists(os.path.join(parent_dir, ".agents")) or os.path.exists(os.path.join(parent_dir, ".git")):
        return parent_dir
    return parent_dir if os.path.basename(skrip_dir) == "vibe_tools" else skrip_dir


# ==================== PEMETAAN BERKAS (.agents/MAP.md) ====================

def _hitung_baris(path: str) -> int:
    """
[ID]: Menghitung jumlah baris file teks (dibulatkan ke puluhan terdekat agar stabil).
[EN]: Calculates the number of lines in a text file (rounded to the nearest ten for stability).
"""
    try:
        with open(path, "rb") as f:
            n = f.read().count(b"\n") + 1
    except Exception:
        return 0
    return int(round(n / 10.0)) * 10


def _docstring_baris_pertama(path: str, nama: str) -> str:
    """
[ID]: Mengambil baris pertama docstring modul .py sebagai deskripsi awal.
[EN]: Retrieves the first line of the .py module's docstring as the initial description.
"""
    if not path.endswith(".py"):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = ast.get_docstring(ast.parse(f.read())) or ""
    except Exception:
        return ""
    baris = doc.strip().splitlines()[0].strip() if doc.strip() else ""
    baris = re.sub(r"\s*\([^)]*\.py\)\s*", " ", baris).strip(" .-")
    sisa = re.sub(r"(?i)^(modul|script|entry point root)\s*:?\s*", "", baris).strip()
    if not sisa or sisa.replace(".py", "").lower() == nama.replace(".py", "").lower():
        return ""
    return baris[:100]


def _baca_peta_lama(map_path: str) -> dict:
    """
[ID]: Membaca MAP.md lama: mempertahankan deskripsi yang sudah ada.
[EN]: Reads the old MAP.md: preserves existing descriptions.
"""
    deskripsi, judul, urutan = {}, {}, []
    if not os.path.exists(map_path):
        return {"desk": deskripsi, "judul": judul, "urutan": urutan}
    seksi = None
    with open(map_path, "r", encoding="utf-8") as f:
        for baris in f.read().splitlines():
            if baris.startswith("## "):
                teks = baris[3:].strip()
                if teks.startswith("Root"):
                    seksi = ""
                    judul[""] = teks
                elif teks.startswith(("Non-code", "Launchers", "Other")):
                    seksi = None if not teks.startswith("Other") else ""
                else:
                    kunci = teks.split(" - ")[0].strip("`/ ").replace("\\", "/")
                    seksi = kunci
                    judul[kunci] = teks
                if seksi is not None and seksi not in urutan:
                    urutan.append(seksi)
                continue
            m = POLA_ITEM.match(baris)
            if m and seksi is not None and m.group(2):
                nama = m.group(1).replace("\\", "/")
                if nama.endswith("/") or m.group(2) == BELUM_ADA_DESKRIPSI:
                    continue
                rel = f"{seksi}/{nama}" if seksi else nama
                deskripsi[rel] = m.group(2)
    return {"desk": deskripsi, "judul": judul, "urutan": urutan}


def _pindai_kode(base_dir: str) -> dict:
    """
[ID]: Memindai seluruh file kode proyek. Mengembalikan {seksi: [path relatif, ...]}.
[EN]: Scans all project code files. Returns {section: [relative path, ...]}.
"""
    hasil = {}
    for dirpath, dirnames, filenames in os.walk(base_dir):
        dirnames[:] = [d for d in dirnames if d not in FOLDER_ABAIKAN]
        rel_dir = os.path.relpath(dirpath, base_dir).replace("\\", "/")
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


def perbarui_peta(base_dir: str) -> dict:
    """
[ID]: Menyusun dan menulis .agents/MAP.md secara non-destruktif.
[EN]: Compiles and writes .agents/MAP.md non-destructively.
"""
    map_path = os.path.join(base_dir, ".agents", "MAP.md")
    lama = _baca_peta_lama(map_path)
    pindai = _pindai_kode(base_dir)

    semua_baru = {p for daftar in pindai.values() for p in daftar}
    baru = sorted(p for p in semua_baru if p not in lama["desk"])
    dihapus = sorted(p for p in lama["desk"] if p not in semua_baru)

    urutan = [s for s in lama["urutan"] if s in pindai]
    urutan += sorted(s for s in pindai if s not in urutan)
    if "" in urutan:
        urutan.remove("")
    urutan.insert(0, "")

    baris_out = [HEADER.rstrip("\n"), ""]
    tanpa_deskripsi = []
    for seksi in urutan:
        if seksi not in pindai:
            continue
        judul = lama["judul"].get(seksi) or (JUDUL_ROOT if seksi == "" else f"{seksi}/")
        baris_out.append(f"## {judul}")
        for rel in sorted(pindai[seksi]):
            nama = rel[len(seksi) + 1:] if seksi else rel
            full_p = os.path.join(base_dir, rel.replace("/", os.sep))
            desk = lama["desk"].get(rel) or _docstring_baris_pertama(full_p, os.path.basename(rel))
            if not desk:
                desk = BELUM_ADA_DESKRIPSI
                tanpa_deskripsi.append(rel)
            n = _hitung_baris(full_p)
            info = f" (~{n} lines)" if n >= 300 else ""
            baris_out.append(f"- `{nama}`{info} - {desk}")
        baris_out.append("")

    baris_out.append(NON_CODE.rstrip("\n"))
    bat = sorted(f for f in os.listdir(base_dir) if f.lower().endswith(".bat"))
    if bat:
        baris_out.append("")
        baris_out.append("## Launchers")
        baris_out.append(", ".join(f"`{b}`" for b in bat))
    baris_out.append("")

    os.makedirs(os.path.dirname(map_path), exist_ok=True)
    with open(map_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(baris_out))

    return {"baru": baru, "dihapus": dihapus, "tanpa_deskripsi": tanpa_deskripsi}


# ==================== PIPELINE GRAPHIFY & PEMELIHARAAN ====================

def cari_perintah_graphify() -> list:
    """
[ID]: Mencari executable graphify di PATH atau fallback ke modul python.
[EN]: Searches for the graphify executable in PATH or falls back to the Python module.
"""
    exe = shutil.which("graphify")
    if exe:
        return [exe]
    return [sys.executable, "-m", "graphify"]


def jalankan(langkah: str, args: list, base_dir: str) -> bool:
    """
[ID]: Menjalankan satu perintah sub-proses dan mencetak hasil.
[EN]: Executes a single subprocess command and prints the result.
"""
    print(f"\n=== {langkah} ===")
    print("$ " + " ".join(args))
    try:
        hasil = subprocess.run(args, cwd=base_dir)
    except FileNotFoundError:
        print("[ERROR] graphify tidak ditemukan. Instal dengan: pip install graphifyy")
        return False
    if hasil.returncode != 0:
        print(f"[ERROR] Langkah '{langkah}' gagal (exit code {hasil.returncode}).")
        return False
    return True


def rapikan_arsip(out_dir: str):
    """
[ID]: Menghapus folder arsip bertanggal lawas, menyisakan MAKS_ARSIP terbaru.
[EN]: Deletes dated archive folders, retaining only the latest MAKS_ARSIP.
"""
    if not os.path.isdir(out_dir):
        return
    pola = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    arsip = sorted(d for d in os.listdir(out_dir) if pola.match(d) and os.path.isdir(os.path.join(out_dir, d)))
    lama = arsip[:-MAKS_ARSIP] if len(arsip) > MAKS_ARSIP else []
    for nama in lama:
        try:
            shutil.rmtree(os.path.join(out_dir, nama))
            print(f"[Arsip] Dihapus: graphify-out/{nama}")
        except Exception as e:
            print(f"[Arsip] Gagal menghapus {nama}: {e}")
    if not lama:
        print(f"[Arsip] Bersih ({len(arsip)} arsip dipertahankan).")


def verifikasi_wiki(out_dir: str) -> bool:
    """
[ID]: Memverifikasi sinkronisasi antara graph.json dan wiki/index.md.
[EN]: Verifies synchronization between graph.json and wiki/index.md.
"""
    graph_path = os.path.join(out_dir, "graph.json")
    index_path = os.path.join(out_dir, "wiki", "index.md")
    if not (os.path.exists(graph_path) and os.path.exists(index_path)):
        print("[Verifikasi] graph.json atau wiki/index.md belum ada.")
        return False
    try:
        with open(graph_path, "r", encoding="utf-8") as f:
            n_graph = len(json.load(f).get("nodes", []))
        with open(index_path, "r", encoding="utf-8") as f:
            m = re.search(r"\*\*(\d+) nodes", f.read())
        n_wiki = int(m.group(1)) if m else -1
    except Exception as e:
        print(f"[Verifikasi] Gagal membaca graph/wiki: {e}")
        return False
    sinkron = n_graph == n_wiki
    segar = os.path.getmtime(index_path) >= os.path.getmtime(graph_path)
    print(f"[Verifikasi] Nodes graph={n_graph} | wiki={n_wiki} | Wiki mutakhir={segar}")
    return sinkron and segar


def main():
    root_dir = deteksi_root_proyek()
    out_dir = os.path.join(root_dir, "graphify-out")

    # Mode opsi cepat CLI
    map_only = "--map-only" in sys.argv or "-m" in sys.argv
    graph_only = "--graph-only" in sys.argv or "-g" in sys.argv

    print("=" * 60)
    print("  GRAPHIFY SYNC & FILE MAP GENERATOR")
    print(f"  Direktori Proyek: {root_dir}")
    print("=" * 60)

    sukses = True
    gf = cari_perintah_graphify()

    if not map_only:
        sukses = jalankan("1/3 Update graph (AST-only)", gf + ["update", "."], root_dir)
        if sukses:
            sukses = jalankan("2/3 Export wiki", gf + ["export", "wiki"], root_dir)

    if sukses and not graph_only:
        print("\n=== Update peta file (.agents/MAP.md) ===")
        try:
            r = perbarui_peta(root_dir)
            print(f"[Peta] Baru: {len(r['baru'])} | Dihapus: {len(r['dihapus'])}")
            for p in r["baru"]:
                print(f"   + {p}")
            for p in r["dihapus"]:
                print(f"   - {p}")
            if r["tanpa_deskripsi"]:
                print(f"[Peta] Belum ada deskripsi ({len(r['tanpa_deskripsi'])} file):")
                for p in r["tanpa_deskripsi"]:
                    print(f"   ? {p}")
        except Exception as e:
            print(f"[ERROR] Gagal memperbarui MAP.md: {e}")
            sukses = False

    if sukses and not map_only:
        print("\n=== Verifikasi wiki ===")
        verifikasi_wiki(out_dir)
        print("\n=== Rapikan arsip ===")
        rapikan_arsip(out_dir)

    print("\n" + ("=" * 60))
    if sukses:
        print("[SUKSES] Sinkronisasi Knowledge Graph & Peta Selesai!")
    else:
        print("[PERINGATAN] Terjadi kesalahan dalam proses sinkronisasi.")
    print("=" * 60)

    if "--no-pause" not in sys.argv and sys.stdin and sys.stdin.isatty():
        input("\nTekan Enter untuk menutup...")
    sys.exit(0 if sukses else 1)


if __name__ == "__main__":
    main()
