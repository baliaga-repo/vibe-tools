# -*- coding: utf-8 -*-
"""
[ID]: Installer & Konfigurator Portabel Aider Hybrid Free Tier (setup_aider_hybrid.py).
Memasang Aider secara terisolasi (aider-install / uv), mengarsipkan aset legacy Zoo/Roo,
dan menyalin konfigurasi Aider generik ke proyek target secara non-destruktif.

Penggunaan:
    python vibe_tools/setup_aider_hybrid.py
    python vibe_tools/setup_aider_hybrid.py --target "D:/ProjectLain" --setup-ollama
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VIBE_TOOLS_DIR: Path = Path(__file__).resolve().parent
TEMPLATE_CONF: Path = VIBE_TOOLS_DIR / "templates" / "aider" / ".aider.conf.example.yml"
DEFAULT_AIDERIGNORE: str = (
    "**/*cookies*\n**/*_key.txt\n**/*token*.json\n*.env\n*.key\n*.pem\n"
    "cache/\n_cache/\nbackup script/\ngraphify-out/\n*.log\n"
)
DEFAULT_CONVENTIONS: str = (
    "# Project Coding Conventions\n"
    "- Write Python docstrings, comments, and logs in Indonesian.\n"
    "- Keep modules under 300 lines, stdlib-first, with explicit type hints.\n"
    "- Run `python -m py_compile <files>` after edits. NEVER run git commit/push.\n"
)


def tentukan_target_proyek(arg_target: str = "") -> Path:
    """[ID]: Menentukan direktori root proyek target pemasangan."""
    if arg_target:
        return Path(arg_target).expanduser().resolve()
    cwd = Path.cwd().resolve()
    return cwd.parent if cwd.name == "vibe_tools" else cwd


def _temukan_aider_exe() -> str | None:
    """[ID]: Mencari executable aider di PATH atau ~/.local/bin."""
    exe = shutil.which("aider")
    if exe:
        return exe
    kandidat = Path.home() / ".local" / "bin" / ("aider.exe" if sys.platform.startswith("win") else "aider")
    return str(kandidat) if kandidat.is_file() else None


def cek_atau_pasang_aider() -> bool:
    """[ID]: Memastikan Aider terpasang di venv terisolasi via aider-install (uv)."""
    if _temukan_aider_exe():
        print("[OK] Aider CLI sudah tersedia di lingkungan terisolasi.")
        return True
    print("[INFO] Memasang Aider terisolasi via aider-install (tanpa menyentuh Python global)...")
    try:
        res_pip = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "aider-install"], capture_output=True, text=True)
        if res_pip.returncode != 0:
            print(f"[ERROR] Gagal memasang aider-install: {res_pip.stderr.strip()}")
            return False
        inst_exe = shutil.which("aider-install") or str(Path(sys.executable).parent / "Scripts" / "aider-install.exe")
        cmd = [inst_exe] if Path(inst_exe).exists() else [sys.executable, "-m", "aider_install"]
        res_inst = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res_inst.returncode != 0 or not _temukan_aider_exe():
            print(f"[ERROR] aider-install gagal: {res_inst.stderr.strip() or res_inst.stdout.strip()}")
            return False
        print("[OK] Aider berhasil dipasang secara terisolasi.")
        return True
    except Exception as err:
        print(f"[ERROR] Gagal proses instalasi Aider: {err}")
        return False


def arsipkan_legacy_zoo_roo(target_root: Path) -> list[str]:
    """[ID]: Memindahkan aset legacy .zoo/.roo ke backup script/legacy_zoo_code/ & perbarui .gitignore."""
    arsip_dir = target_root / "backup script" / "legacy_zoo_code"
    dipindah: list[str] = []
    for nama in (".zoo", ".zoomodes", ".roo", ".roomodes"):
        src = target_root / nama
        if src.exists():
            arsip_dir.mkdir(parents=True, exist_ok=True)
            dst = arsip_dir / nama
            if dst.exists():
                shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
            shutil.move(str(src), str(dst))
            dipindah.append(nama)
    gi_path = target_root / ".gitignore"
    isi_gi = gi_path.read_text(encoding="utf-8") if gi_path.exists() else ""
    tambahan = [x for x in (".zoo/", ".zoomodes", ".roo/", ".roomodes", ".aider.tags.cache.v*", ".aider.chat.history.md", ".aider.input.history") if x not in isi_gi]
    if tambahan:
        prefix = "" if (not isi_gi or isi_gi.endswith("\n")) else "\n"
        gi_path.write_text(isi_gi + prefix + "\n".join(tambahan) + "\n", encoding="utf-8")
    return dipindah


def _tulis_non_destruktif(target: Path, isi: str, sumber_file: Path | None = None) -> None:
    """[ID]: Menulis berkas konfigurasi hanya jika belum ada di proyek target."""
    if target.exists():
        print(f"[SKIP] {target.name} sudah ada (dipertahankan).")
        return
    if sumber_file and sumber_file.is_file():
        shutil.copy2(sumber_file, target)
    else:
        target.write_text(isi, encoding="utf-8", newline="\n")
    print(f"[BUAT] {target.name}")


def pasang_aider_hybrid(target_path: str = "", setup_ollama: bool = False, archive_zoo: bool = True) -> Path:
    """[ID]: Memasang Aider terisolasi & menyalin konfigurasi standar ke proyek target."""
    target_root = tentukan_target_proyek(target_path)
    if archive_zoo:
        dipindah = arsipkan_legacy_zoo_roo(target_root)
        if dipindah:
            print(f"[ARSIP] Legacy Zoo/Roo dipindahkan: {', '.join(dipindah)}")
    cek_atau_pasang_aider()
    _tulis_non_destruktif(target_root / ".aider.conf.yml", "", TEMPLATE_CONF)
    _tulis_non_destruktif(target_root / ".aiderignore", DEFAULT_AIDERIGNORE)
    _tulis_non_destruktif(target_root / "CONVENTIONS.md", DEFAULT_CONVENTIONS)
    if not (Path.home() / ".gemini" / "openrouter_key.txt").is_file() and not os.environ.get("OPENROUTER_API_KEY"):
        print("[PERINGATAN] OPENROUTER_API_KEY / ~/.gemini/openrouter_key.txt belum ditemukan.")
    if setup_ollama:
        st_ol = "tersedia" if shutil.which("ollama") else "belum terpasang"
        print(f"[OLLAMA] Status CLI: {st_ol}. Gunakan OLLAMA_KEEP_ALIVE=5m untuk hybrid GPU lokal.")
    return target_root


def main() -> None:
    """[ID]: Titik masuk CLI setup_aider_hybrid.py."""
    parser = argparse.ArgumentParser(description="Installer Portabel Aider Hybrid Free Tier")
    parser.add_argument("--target", default="", help="Path proyek target")
    parser.add_argument("--setup-ollama", action="store_true", help="Tampilkan cek & panduan opsi Ollama lokal")
    parser.add_argument("--no-archive-zoo", action="store_true", help="Lewati pengarsipan .zoo/.roo")
    args = parser.parse_args()
    pasang_aider_hybrid(args.target, setup_ollama=args.setup_ollama, archive_zoo=not args.no_archive_zoo)


if __name__ == "__main__":
    main()
