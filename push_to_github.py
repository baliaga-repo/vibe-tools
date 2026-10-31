# -*- coding: utf-8 -*-
"""
Skrip Otomasi Git Staging, Commit & Push untuk Repositori 'vibe_tools'.
Fitur: Khusus mengelola 'vibe_tools', pengaman berkas rahasia & berkas besar (>50MB/100MB),
pembersihan desktop.ini, penanganan submodule/standalone, serta sinkronisasi remote origin.
"""

import os
import sys
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Memastikan output terminal Windows menggunakan encoding UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BATAS_UKURAN_PERINGATAN_MB = 50
BATAS_UKURAN_MAKSIMAL_MB = 100
REPO_DIR = Path(__file__).resolve().parent

POLA_RAHASIA = [
    (re.compile(r"sk-or-v1-[0-9a-zA-Z]{32,}"), "OpenRouter API Key"),
    (re.compile(r"sk-[0-9a-zA-Z]{32,}"), "OpenAI / Anthropic API Key"),
    (re.compile(r"ghp_[0-9a-zA-Z]{36,}"), "GitHub Personal Access Token"),
    (re.compile(r"github_pat_[0-9a-zA-Z_]{60,}"), "GitHub Fine-Grained Token"),
    (re.compile(r"AIzaSy[0-9a-zA-Z_-]{30,}"), "Google API Key"),
]
NAMA_FILE_BERBAHAYA = (".env", "openrouter_api_key.txt", "id_rsa", "id_ed25519", "credentials.json", "secret.json")


def cetak_garis(karakter: str = "=", panjang: int = 60) -> None:
    """Mencetak garis pemisah untuk format CLI."""
    print(karakter * panjang)


def siapkan_lingkungan_git(repo_dir: Path) -> dict:
    """Menyiapkan env GIT jika target submodule (.git bertipe file) untuk mencegah error chdir."""
    env = os.environ.copy()
    git_item = repo_dir / ".git"
    if git_item.is_file():
        try:
            konten = git_item.read_text(encoding="utf-8").strip()
            if konten.startswith("gitdir:"):
                gitdir_path = (repo_dir / konten.split(":", 1)[1].strip()).resolve()
                if gitdir_path.exists():
                    env["GIT_DIR"] = str(gitdir_path)
                    env["GIT_WORK_TREE"] = str(repo_dir.resolve())
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
                item.unlink(missing_ok=True)
                total += 1
        except Exception:
            pass
    return total


def cek_prasyarat(repo_dir: Path = REPO_DIR) -> None:
    """Memverifikasi Git terpasang dan target adalah repositori Git yang sah."""
    kode, _, _ = jalankan_perintah("git --version", repo_dir=repo_dir)
    if kode != 0:
        print("[GAGAL] Git tidak terdeteksi di sistem PATH."); sys.exit(1)
    kode, out, _ = jalankan_perintah("git rev-parse --is-inside-work-tree", repo_dir=repo_dir)
    if kode != 0 or out != "true":
        print(f"[GAGAL] Target ({repo_dir}) bukan repositori Git."); sys.exit(1)
    bersihkan_desktop_ini(repo_dir)


def dapatkan_branch_aktif(repo_dir: Path = REPO_DIR) -> str:
    """Mengambil nama branch git aktif."""
    kode, out, _ = jalankan_perintah("git branch --show-current", repo_dir=repo_dir)
    if kode == 0 and out:
        return out
    kode, out, _ = jalankan_perintah("git rev-parse --abbrev-ref HEAD", repo_dir=repo_dir)
    return out if kode == 0 and out else "main"


def dapatkan_remote_info(nama_remote: str = "origin", repo_dir: Path = REPO_DIR) -> str:
    """Mengambil URL remote origin."""
    kode, out, _ = jalankan_perintah(f"git remote get-url {nama_remote}", repo_dir=repo_dir)
    return out if kode == 0 else ""


def dapatkan_daftar_perubahan(repo_dir: Path = REPO_DIR):
    """Mengambil daftar berkas yang mengalami perubahan."""
    kode, out, _ = jalankan_perintah("git status --porcelain", repo_dir=repo_dir)
    if kode != 0 or not out:
        return []
    return [(b[:2].strip(), b[3:].strip().strip('"')) for b in out.splitlines() if len(b) >= 4]


def cek_file_berukuran_besar(daftar_perubahan, repo_dir: Path = REPO_DIR):
    """Mengecek berkas yang melebihi batas ukuran GitHub (>50MB / >100MB)."""
    file_besar = []
    for _, pf in daftar_perubahan:
        p = repo_dir / (pf.split(" -> ")[-1].strip() if " -> " in pf else pf)
        if p.is_file():
            try:
                mb = p.stat().st_size / (1024 * 1024)
                if mb >= BATAS_UKURAN_PERINGATAN_MB:
                    file_besar.append((pf, mb))
            except Exception:
                pass
    return file_besar


def cek_kebocoran_rahasia(daftar_perubahan, repo_dir: Path = REPO_DIR):
    """Mendeteksi berkas rahasia atau token API yang tidak sengaja ter-stage."""
    temuan = []
    for _, pf in daftar_perubahan:
        p = repo_dir / (pf.split(" -> ")[-1].strip() if " -> " in pf else pf)
        nb = p.name.lower()
        if nb in NAMA_FILE_BERBAHAYA or nb.startswith(".env."):
            temuan.append((pf, "Kredensial Sensitif", p.name)); continue
        if p.is_file() and p.stat().st_size <= 1024 * 1024:
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
                for reg, lbl in POLA_RAHASIA:
                    for c in reg.findall(txt):
                        if not any(k in c.lower() for k in ("xxxx", "tempel", "placeholder", "...")):
                            temuan.append((pf, f"Token {lbl}", c[:10] + "..." + c[-4:]))
            except Exception:
                pass
    return temuan


def cek_unpushed_commits(branch: str, repo_dir: Path = REPO_DIR):
    """Memeriksa daftar commit lokal yang belum dikirim ke origin."""
    kode, out, _ = jalankan_perintah(f"git log origin/{branch}..HEAD --oneline", repo_dir=repo_dir)
    return out.splitlines() if kode == 0 and out else []


def tampilkan_ringkasan(branch: str, remote_url: str, perubahan, unpushed) -> bool:
    """Menampilkan ringkasan status repositori vibe_tools."""
    cetak_garis("=")
    print(f" RINGKASAN STATUS GITHUB (vibe_tools) -> Branch: {branch}")
    print(f" Remote URL: {remote_url or '(Belum ada remote origin)'}")
    cetak_garis("-")
    if not perubahan and not unpushed:
        print("[INFO] Repositori bersih! Tidak ada perubahan berkas atau commit tertunda.")
        cetak_garis("="); return False
    if perubahan:
        print(f"Perubahan Berkas ({len(perubahan)} berkas):")
        for st, f in perubahan:
            tag = "[MODIFIED]" if st == "M" else "[UNTRACKED]" if st == "??" else f"[{st}]"
            print(f"  {tag:<12} {f}")
    if unpushed:
        cetak_garis("-")
        print(f"Commit Lokal Belum Di-Push ({len(unpushed)} commit):")
        for c in unpushed:
            print(f"  * {c}")
    cetak_garis("="); return True


def tanya_konfirmasi(pertanyaan: str, default_ya: bool = True) -> bool:
    """Meminta konfirmasi dari pengguna (y/n)."""
    pilihan = "[Y/n]" if default_ya else "[y/N]"
    while True:
        jawab = input(f"{pertanyaan} {pilihan}: ").strip().lower()
        if not jawab: return default_ya
        if jawab in ("y", "ya", "yes"): return True
        if jawab in ("n", "tidak", "no"): return False
        print("Harap ketik 'y' atau 'n'.")


def proses_git_push(pesan_commit: str = None, auto_confirm: bool = True, lakukan_pull: bool = True) -> bool:
    """Alur eksekusi git add, commit, pull rebase, dan push untuk vibe_tools."""
    cek_prasyarat()
    branch, remote_url = dapatkan_branch_aktif(), dapatkan_remote_info()
    if not remote_url:
        print("[PERINGATAN] Remote 'origin' belum terpasang."); return False

    perubahan, unpushed = dapatkan_daftar_perubahan(), cek_unpushed_commits(branch)
    if not tampilkan_ringkasan(branch, remote_url, perubahan, unpushed):
        return True

    file_besar = cek_file_berukuran_besar(perubahan)
    if file_besar:
        print("\n[PERINGATAN] Berkas berukuran besar terdeteksi:")
        for pf, uk in file_besar:
            print(f"  - {pf}: {uk:.2f} MB")
            if uk >= BATAS_UKURAN_MAKSIMAL_MB:
                print("    ^ DIBLOKIR: File >100MB dilarang oleh GitHub."); return False

    kebocoran = cek_kebocoran_rahasia(perubahan)
    if kebocoran:
        cetak_garis("!")
        print("   [BAHAYA KEAMANAN] TERDETEKSI KREDENSIAL / API KEY RAHASIA!")
        for pf, lbl, inf in kebocoran:
            print(f"  [X] {pf} ({lbl}: {inf})")
        cetak_garis("!"); return False

    if perubahan:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pesan_default = f"Pembaruan modul vibe_tools: {waktu}"
        if not pesan_commit:
            pesan_commit = pesan_default if auto_confirm else (input(f"\nPesan commit [{pesan_default}]: ").strip() or pesan_default)

        print("\n[1/3] Menambahkan berkas: git add -A")
        kode, _, err = jalankan_perintah("git add -A")
        if kode != 0:
            print(f"[GAGAL] git add: {err}"); return False

        print(f"[2/3] Membuat commit: git commit -m \"{pesan_commit}\"")
        kode, out, err = jalankan_perintah(["git", "commit", "-m", pesan_commit])
        if kode != 0 and "nothing to commit" not in (err + out).lower():
            print(f"[GAGAL] git commit: {err or out}"); return False

    if lakukan_pull:
        print(f"\n[*] Sinkronisasi remote: git pull --rebase origin {branch}")
        jalankan_perintah(f"git pull --rebase origin {branch}")

    if not auto_confirm and not tanya_konfirmasi(f"\nKirim commit vibe_tools ke GitHub branch '{branch}'?", default_ya=True):
        print("[BATAL] Push dibatalkan."); return True

    print(f"\n[3/3] Mengirim ke GitHub: git push -u origin {branch} ...")
    kode, out, err = jalankan_perintah(f"git push -u origin {branch}")
    if kode == 0:
        cetak_garis("=")
        print("     BERHASIL! vibe_tools TELAH DI-PUSH KE GITHUB")
        cetak_garis("="); return True
    print(f"\n[GAGAL] Push vibe_tools gagal:\n{err or out}"); return False


def main():
    """Fungsi utama CLI."""
    parser = argparse.ArgumentParser(description="Otomasi Git commit & push khusus modul vibe_tools.")
    parser.add_argument("-m", "--message", type=str, default=None, help="Pesan commit kustom.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Mode konfirmasi manual.")
    parser.add_argument("-y", "--yes", action="store_true", default=True, help="Auto konfirmasi (default: aktif).")
    parser.add_argument("--no-pull", action="store_true", help="Lewati git pull --rebase.")
    parser.add_argument("-s", "--status", action="store_true", help="Hanya tampilkan status.")
    args = parser.parse_args()

    if args.status:
        cek_prasyarat()
        b = dapatkan_branch_aktif()
        tampilkan_ringkasan(b, dapatkan_remote_info(), dapatkan_daftar_perubahan(), cek_unpushed_commits(b))
        return

    if not proses_git_push(pesan_commit=args.message, auto_confirm=not args.interactive, lakukan_pull=not args.no_pull):
        sys.exit(1)


if __name__ == "__main__":
    main()
