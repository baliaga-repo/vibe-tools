# -*- coding: utf-8 -*-
"""
Skrip Otomasi Git Pull untuk Pembaruan Submodule 'vibe_tools'.
Fitur: Menarik pembaruan terbaru dari GitHub (origin main) dengan perlindungan --rebase --autostash,
pembersihan desktop.ini otomatis, dan integrasi opsional ke update_ecosystem.py.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Memastikan output terminal Windows menggunakan encoding UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_DIR = Path(__file__).resolve().parent
PARENT_PROJECT_DIR = REPO_DIR.parent


def cetak_garis(karakter: str = "=", panjang: int = 60) -> None:
    """Mencetak garis pemisah untuk format CLI."""
    print(karakter * panjang)


def siapkan_lingkungan_git(repo_dir: Path) -> dict:
    """Menyiapkan env GIT jika target submodule (.git bertipe file) untuk mencegah error chdir."""
    env = os.environ.copy()
    git_item = repo_dir / ".git"
    if git_item.is_file():
        try:
            k = git_item.read_text(encoding="utf-8").strip()
            if k.startswith("gitdir:"):
                g_path = (repo_dir / k.split(":", 1)[1].strip()).resolve()
                if g_path.exists():
                    env["GIT_DIR"], env["GIT_WORK_TREE"] = str(g_path), str(repo_dir.resolve())
        except Exception:
            pass
    return env


def jalankan_perintah(perintah, repo_dir: Path = REPO_DIR, tangkap_output: bool = True):
    """Menjalankan perintah Git pada repositori target."""
    try:
        hasil = subprocess.run(
            perintah,
            cwd=str(repo_dir),
            env=siapkan_lingkungan_git(repo_dir),
            shell=isinstance(perintah, str),
            capture_output=tangkap_output,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return hasil.returncode, (hasil.stdout or "").rstrip(), (hasil.stderr or "").strip()
    except Exception as e:
        return -1, "", str(e)


def bersihkan_desktop_ini(repo_dir: Path = REPO_DIR) -> int:
    """Membersihkan berkas desktop.ini dari repo dan folder .git."""
    total, targets = 0, [repo_dir]
    git_item = repo_dir / ".git"
    if git_item.is_dir():
        targets.append(git_item)
    elif git_item.is_file():
        try:
            k = git_item.read_text(encoding="utf-8").strip()
            if k.startswith("gitdir:"):
                targets.append((repo_dir / k.split(":", 1)[1].strip()).resolve())
        except Exception:
            pass

    for t in targets:
        try:
            for item in t.rglob("desktop.ini"):
                item.unlink(missing_ok=True); total += 1
        except Exception:
            pass
    return total


def cek_prasyarat(repo_dir: Path = REPO_DIR) -> None:
    """Memverifikasi Git terpasang dan target adalah repositori Git yang sah."""
    if jalankan_perintah("git --version", repo_dir=repo_dir)[0] != 0:
        print("[GAGAL] Git tidak terdeteksi di sistem PATH."); sys.exit(1)
    k, out, _ = jalankan_perintah("git rev-parse --is-inside-work-tree", repo_dir=repo_dir)
    if k != 0 or out != "true":
        print(f"[GAGAL] Target ({repo_dir}) bukan repositori Git."); sys.exit(1)
    bersihkan_desktop_ini(repo_dir)


def dapatkan_branch_aktif(repo_dir: Path = REPO_DIR) -> str:
    """Mengambil nama branch git aktif dengan fallback cerdas."""
    kode, out, _ = jalankan_perintah("git branch --show-current", repo_dir=repo_dir)
    if kode == 0 and out and out != "HEAD":
        return out

    git_dir = repo_dir / ".git"
    if git_dir.is_file():
        try:
            k = git_dir.read_text(encoding="utf-8").strip()
            if k.startswith("gitdir:"):
                git_dir = (repo_dir / k.split(":", 1)[1].strip()).resolve()
        except Exception:
            pass
    for r_dir in ("rebase-merge", "rebase-apply"):
        head_file = git_dir / r_dir / "head-name"
        if head_file.exists():
            try:
                ref = head_file.read_text(encoding="utf-8").strip()
                if ref.startswith("refs/heads/"):
                    return ref.replace("refs/heads/", "")
            except Exception:
                pass

    kode, out, _ = jalankan_perintah("git rev-parse --abbrev-ref origin/HEAD", repo_dir=repo_dir)
    return out.split("/", 1)[1].strip() if kode == 0 and out and "/" in out and not out.endswith("/HEAD") else "main"


def proses_git_pull(branch: str = None, sync_ecosystem: bool = True) -> bool:
    """Menarik pembaruan dari remote GitHub dan menyelaraskan ekosistem."""
    cek_prasyarat()
    target_branch = branch or dapatkan_branch_aktif()

    cetak_garis("=")
    print("       PEMBARUAN SUBMODULE GITHUB (vibe_tools)")
    cetak_garis("=")
    print(f" Direktori Target : {REPO_DIR}")
    print(f" Target Branch    : {target_branch}")
    print(f" Sinkron Ekosistem: {'Aktif' if sync_ecosystem else 'Nonaktif'}")
    cetak_garis("-")

    # Ambil hash commit sebelum pull
    _, head_sebelum, _ = jalankan_perintah("git rev-parse HEAD")

    print(f"\n[*] Menjalankan: git pull --rebase --autostash origin {target_branch} ...")
    kode, out, err = jalankan_perintah(f"git pull --rebase --autostash origin {target_branch}")

    if kode != 0:
        cetak_garis("!")
        print("          [GAGAL] PULL DARI GITHUB MENGALAMI KENDALA")
        cetak_garis("!")
        print(err or out)
        print("\nPetunjuk:")
        print("1. Pastikan komputer Anda terhubung ke internet.")
        print("2. Jika ada konflik rebase, selesaikan dengan 'git rebase --continue' atau batalkan dengan 'git rebase --abort'.")
        return False

    # Ambil hash commit setelah pull
    _, head_sesudah, _ = jalankan_perintah("git rev-parse HEAD")

    cetak_garis("=")
    print("      BERHASIL! SUBMODULE vibe_tools TELAH DIPERBARUI")
    cetak_garis("=")
    if out:
        print(out)

    if head_sebelum != head_sesudah:
        print(f"\n[INFO] Pembaruan commit terdeteksi ({head_sebelum[:7]} -> {head_sesudah[:7]}):")
        _, log_out, _ = jalankan_perintah(f"git log --oneline {head_sebelum}..{head_sesudah}")
        if log_out:
            for baris in log_out.splitlines():
                print(f"  * {baris}")
    else:
        print("\n[INFO] Submodule sudah berada pada versi paling mutakhir.")

    # Sinkronisasi ke seluruh proyek (update_ecosystem.py) jika diaktifkan
    if sync_ecosystem:
        skrip_updater = REPO_DIR / "update_ecosystem.py"
        if skrip_updater.is_file():
            print("\n" + "-" * 60)
            print(" [*] Menjalankan penyelarasan aturan AI via update_ecosystem.py ...")
            print("-" * 60)
            subprocess.run([sys.executable, str(skrip_updater)], cwd=str(PARENT_PROJECT_DIR))

    return True


def main():
    """Fungsi utama CLI."""
    parser = argparse.ArgumentParser(description="Otomasi penarikan pembaruan Git khusus submodule vibe_tools.")
    parser.add_argument("-b", "--branch", type=str, default=None, help="Nama branch remote target (default: auto-detect/main).")
    parser.add_argument("--no-sync", action="store_true", help="Lewati eksekusi update_ecosystem.py setelah pull.")
    args = parser.parse_args()

    sukses = proses_git_pull(branch=args.branch, sync_ecosystem=not args.no_sync)
    if not sukses:
        sys.exit(1)


if __name__ == "__main__":
    main()

