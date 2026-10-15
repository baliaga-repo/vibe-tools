# -*- coding: utf-8 -*-
"""
Skrip Otomasi Git Push ke GitHub
Dibuat untuk memudahkan proses staging, commit, dan push repositori ke GitHub secara interaktif atau otomatis.
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

# Batas peringatan ukuran file sebelum di-push (GitHub menolak file > 100MB)
BATAS_UKURAN_PERINGATAN_MB = 50
BATAS_UKURAN_MAKSIMAL_MB = 100


def cetak_garis(karakter="=", panjang=60):
    """Mencetak garis pemisah untuk mempercantik tampilan CLI."""
    print(karakter * panjang)


def jalankan_perintah(perintah, tangkap_output=True, cek_error=False):
    """
    Menjalankan perintah shell/proses secara aman menggunakan subprocess.
    Dapat menerima string atau list argumen perintah.
    Mengembalikan tuple: (kode_keluar, stdout, stderr).
    """
    try:
        use_shell = isinstance(perintah, str)
        hasil = subprocess.run(
            perintah,
            shell=use_shell,
            capture_output=tangkap_output,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        stdout = hasil.stdout or ""
        stderr = hasil.stderr or ""
        if cek_error and hasil.returncode != 0:
            print(f"[ERROR] Perintah gagal: {perintah}")
            print(f"[ERROR DETAIL] {stderr.strip()}")
        return hasil.returncode, stdout, stderr
    except Exception as e:
        return -1, "", str(e)


def cek_prasyarat(target_dir=None):
    """Memverifikasi bahwa Git terpasang dan folder target adalah repositori Git."""
    if target_dir:
        p = Path(target_dir).resolve()
        if p.exists() and p.is_dir():
            try:
                os.chdir(p)
            except Exception as e:
                print(f"[GAGAL] Tidak dapat berpindah ke direktori target '{p}': {e}")
                sys.exit(1)
        else:
            print(f"[GAGAL] Direktori target tidak ditemukan: {target_dir}")
            sys.exit(1)

    # 1. Cek git command
    kode, stdout, _ = jalankan_perintah("git --version")
    if kode != 0:
        print("[GAGAL] Git tidak terdeteksi di sistem PATH Anda.")
        print("Silakan pastikan Git sudah diinstal: https://git-scm.com/")
        sys.exit(1)

    # 2. Cek apakah di dalam repository git
    kode, stdout, _ = jalankan_perintah("git rev-parse --is-inside-work-tree")
    if kode != 0 or stdout.strip() != "true":
        print(f"[GAGAL] Direktori saat ini ({os.getcwd()}) bukan repositori Git.")
        print("Jalankan 'git init' terlebih dahulu atau pindah ke folder proyek yang tepat.")
        sys.exit(1)

    # 3. Otomatis berpindah direktori ke root repositori git agar semua path sinkron
    kode, stdout, _ = jalankan_perintah("git rev-parse --show-toplevel")
    if kode == 0 and stdout.strip():
        try:
            os.chdir(stdout.strip())
        except Exception:
            pass


def dapatkan_branch_aktif():
    """Mengambil nama branch git yang sedang aktif."""
    kode, stdout, _ = jalankan_perintah("git branch --show-current")
    if kode == 0 and stdout.strip():
        return stdout.strip()
    # Fallback untuk versi git lama atau status detached HEAD
    kode, stdout, _ = jalankan_perintah("git rev-parse --abbrev-ref HEAD")
    return stdout.strip() if kode == 0 and stdout.strip() else "main"


def dapatkan_remote_info(nama_remote="origin"):
    """Mengambil URL dari remote git."""
    kode, stdout, _ = jalankan_perintah(f"git remote get-url {nama_remote}")
    return stdout.strip() if kode == 0 and stdout.strip() else None


def dapatkan_daftar_perubahan():
    """
    Mengambil daftar file yang mengalami perubahan (modified, added, deleted, untracked).
    Mengembalikan list of tuple: (kode_status, nama_file).
    Format porcelain Git: 2 karakter status, diikuti spasi, diikuti nama file.
    """
    kode, stdout, _ = jalankan_perintah("git status --porcelain")
    if kode != 0 or not stdout:
        return []

    perubahan = []
    for baris in stdout.splitlines():
        if len(baris) >= 4:
            status_simbol = baris[:2]
            nama_file = baris[3:].strip().strip('"')
            perubahan.append((status_simbol, nama_file))
    return perubahan


def cek_file_berukuran_besar(daftar_perubahan):
    """
    Memeriksa apakah ada file yang akan di-commit yang melebihi batas ukuran GitHub.
    Mengembalikan daftar file yang terlalu besar.
    """
    file_besar = []
    for _, path_file in daftar_perubahan:
        # Jika ada rename (ditandai ' -> ')
        if " -> " in path_file:
            path_file = path_file.split(" -> ")[-1].strip()

        p = Path(path_file)
        if p.is_file():
            try:
                ukuran_mb = p.stat().st_size / (1024 * 1024)
                if ukuran_mb >= BATAS_UKURAN_PERINGATAN_MB:
                    file_besar.append((str(p), ukuran_mb))
            except Exception:
                pass
    return file_besar


# Pola regex deteksi rahasia / API Key yang tidak boleh lolos ke repositori publik
POLA_RAHASIA = [
    (re.compile(r"sk-or-v1-[0-9a-zA-Z]{32,}"), "OpenRouter API Key"),
    (re.compile(r"sk-[0-9a-zA-Z]{32,}"), "OpenAI / Anthropic API Key"),
    (re.compile(r"ghp_[0-9a-zA-Z]{36,}"), "GitHub Personal Access Token"),
    (re.compile(r"github_pat_[0-9a-zA-Z_]{60,}"), "GitHub Fine-Grained Token"),
    (re.compile(r"sk-ant-api[0-9a-zA-Z_-]{30,}"), "Anthropic API Key"),
    (re.compile(r"AIzaSy[0-9a-zA-Z_-]{30,}"), "Google API Key"),
]

NAMA_FILE_BERBAHAYA = (
    ".env",
    "openrouter_api_key.txt",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secret.json",
)


def cek_kebocoran_rahasia(daftar_perubahan):
    """
    Memeriksa secara otomatis dan proaktif apakah ada berkas rahasia (.env, file key)
    atau teks token / API key aktif di dalam berkas yang akan di-commit.
    Mengembalikan daftar temuan: (nama_file, tipe_peringatan, cuplikan).
    """
    temuan = []
    for _, path_file in daftar_perubahan:
        if " -> " in path_file:
            path_file = path_file.split(" -> ")[-1].strip()

        p = Path(path_file)
        nama_bawah = p.name.lower()

        # 1. Cek nama berkas terlarang
        if (
            nama_bawah in NAMA_FILE_BERBAHAYA
            or nama_bawah.startswith(".env.")
            or (nama_bawah.endswith(".key") and not nama_bawah.endswith(".json"))
        ):
            temuan.append((str(p), "Berkas Kredensial / Variabel Lingkungan Sensitif", p.name))
            continue

        # 2. Cek isi berkas teks (< 1MB)
        if p.is_file():
            try:
                if p.stat().st_size <= 1024 * 1024:
                    teks = p.read_text(encoding="utf-8", errors="ignore")
                    for regex, label in POLA_RAHASIA:
                        cocok = regex.findall(teks)
                        for c in cocok:
                            # Abaikan placeholder dummy umum
                            if any(k in c.lower() for k in ("xxxx", "tempel", "placeholder", "...")):
                                continue
                            sensor = c[:10] + "..." + c[-4:]
                            temuan.append((str(p), f"Bocoran Token: {label}", sensor))
            except Exception:
                pass
    return temuan


def cek_unpushed_commits(branch):
    """Memeriksa jumlah commit lokal yang belum di-push ke remote origin."""
    kode, stdout, _ = jalankan_perintah(f"git log origin/{branch}..HEAD --oneline")
    if kode == 0 and stdout:
        return stdout.splitlines()
    return []


def tanya_konfirmasi(pertanyaan, default_ya=True):
    """Meminta konfirmasi dari pengguna (y/n)."""
    pilihan = "[Y/n]" if default_ya else "[y/N]"
    while True:
        jawaban = input(f"{pertanyaan} {pilihan}: ").strip().lower()
        if not jawaban:
            return default_ya
        if jawaban in ("y", "ya", "yes"):
            return True
        if jawaban in ("n", "tidak", "no"):
            return False
        print("Harap ketik 'y' atau 'n'.")


def tampilkan_ringkasan(branch, remote_url, daftar_perubahan, unpushed_commits):
    """Menampilkan ringkasan status repositori sebelum tindakan dilakukan."""
    cetak_garis("=")
    print("           RINGKASAN STATUS REPOSITORI GITHUB")
    cetak_garis("=")
    print(f" Branch Aktif : {branch}")
    print(f" Remote URL   : {remote_url or '(Belum ada remote origin yang terpasang)'}")
    cetak_garis("-")

    if not daftar_perubahan and not unpushed_commits:
        print("[INFO] Bersih! Tidak ada file yang diubah dan tidak ada commit tertunda.")
        cetak_garis("=")
        return False

    if daftar_perubahan:
        print(f"Perubahan Berkas ({len(daftar_perubahan)} berkas terdeteksi):")
        for status, file_path in daftar_perubahan:
            status_label = status.strip()
            if status_label == "M":
                label = "[MODIFIED] "
            elif status_label == "??":
                label = "[UNTRACKED]"
            elif status_label == "A":
                label = "[ADDED]    "
            elif status_label == "D":
                label = "[DELETED]  "
            elif status_label == "R":
                label = "[RENAMED]  "
            else:
                label = f"[{status_label}]       "
            print(f"  {label} {file_path}")
    else:
        print("[INFO] Semua file kerja bersih (tidak ada perubahan berkas baru).")

    if unpushed_commits:
        cetak_garis("-")
        print(f"Commit Lokal Yang Belum Di-Push ({len(unpushed_commits)} commit):")
        for commit in unpushed_commits:
            print(f"  * {commit}")

    cetak_garis("=")
    return True


def proses_git_push(pesan_commit=None, auto_confirm=True, lakukan_pull=True, target_dir=None):
    """
    Alur utama pelaksanaan git add, git commit, git pull --rebase, dan git push.
    Secara default auto_confirm bernilai True agar proses berjalan langsung tanpa konfirmasi manual.
    """
    cek_prasyarat(target_dir)
    branch = dapatkan_branch_aktif()
    remote_url = dapatkan_remote_info()

    if not remote_url:
        print("[PERINGATAN] Remote 'origin' belum dikonfigurasi.")
        if not auto_confirm:
            url_input = input("Masukkan URL repositori GitHub Anda (misal: https://github.com/user/repo.git): ").strip()
        else:
            url_input = ""
        if not url_input:
            print("[BATAL] URL remote tidak boleh kosong.")
            return False
        kode, _, err = jalankan_perintah(f"git remote add origin {url_input}")
        if kode != 0:
            print(f"[GAGAL] Gagal menambahkan remote: {err}")
            return False
        remote_url = url_input

    daftar_perubahan = dapatkan_daftar_perubahan()
    unpushed_commits = cek_unpushed_commits(branch)

    ada_tindakan = tampilkan_ringkasan(branch, remote_url, daftar_perubahan, unpushed_commits)
    if not ada_tindakan:
        print("Tidak ada yang perlu di-push ke GitHub. Selesai.")
        return True

    # Pengecekan file besar (> 50 MB / > 100 MB)
    file_besar = cek_file_berukuran_besar(daftar_perubahan)
    if file_besar:
        print("\n[PERINGATAN BESAR] Ditemukan berkas berukuran besar:")
        for path_file, ukuran in file_besar:
            print(f"  - {path_file}: {ukuran:.2f} MB")
            if ukuran >= BATAS_UKURAN_MAKSIMAL_MB:
                print("    ^ PERINGATAN: File di atas 100MB AKAN DITOLAK oleh GitHub!")

        print("\nSaran: Tambahkan file tersebut ke .gitignore sebelum melanjutkan.")
        if not auto_confirm:
            if not tanya_konfirmasi("Apakah Anda yakin ingin tetap melanjutkan penambahan file ini?", default_ya=False):
                print("[BATAL] Proses push dibatalkan untuk mencegah penolakan dari GitHub.")
                return False

    # Pengecekan keamanan kredensial & API key sebelum commit
    kebocoran = cek_kebocoran_rahasia(daftar_perubahan)
    if kebocoran:
        cetak_garis("!")
        print("   [BAHAYA KEAMANAN TINGGI] TERDETEKSI FILE / API KEY RAHASIA!")
        cetak_garis("!")
        print("Proses dihentikan seketika untuk melindungi privasi & keamanan Anda:")
        for path_file, label, info in kebocoran:
            print(f"  [X] {path_file}")
            print(f"      Penyebab : {label}")
            print(f"      Detail   : {info}")
        print("\nSolusi:")
        print("1. Tambahkan berkas tersebut ke file '.gitignore'.")
        print("2. Hapus token/API key asli dari berkas sebelum melakukan push.")
        print("3. Gunakan environment variable atau file profil lokal OS.")
        cetak_garis("!")
        return False

    # Tahap 1: Commit file jika ada perubahan berkas
    if daftar_perubahan:
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pesan_default = f"Pembaruan proyek: {waktu_sekarang}"
        if not pesan_commit:
            if not auto_confirm:
                print(f"\nMasukkan pesan commit (Tekan ENTER untuk default: '{pesan_default}'):")
                input_pesan = input("> ").strip()
                pesan_commit = input_pesan if input_pesan else pesan_default
            else:
                pesan_commit = pesan_default
                print(f"\n[INFO] Menggunakan pesan commit otomatis: \"{pesan_commit}\"")

        print("\n[1/4] Menjalankan: git add -A")
        kode, _, err = jalankan_perintah("git add -A")
        if kode != 0:
            print(f"[GAGAL] Gagal melakukan git add: {err}")
            return False

        print(f"[2/4] Menjalankan: git commit -m \"{pesan_commit}\"")
        kode, stdout, err = jalankan_perintah(["git", "commit", "-m", pesan_commit])
        if kode != 0:
            pesan_gabungan = (err + " " + stdout).lower()
            if "nothing to commit" in pesan_gabungan or "no changes added to commit" in pesan_gabungan:
                if "submodules" in pesan_gabungan or "untracked content" in pesan_gabungan or "modified content" in pesan_gabungan:
                    print("\n[PENJELASAN SUBMODULE]")
                    print("Ditemukan perubahan internal di dalam submodule (misal: vibe_tools).")
                    print("Git mengharuskan perubahan di dalam submodule di-commit terlebih dahulu.")
                    print("Jalankan perintah berikut untuk meng-commit & push submodule vibe_tools:")
                    print("  python vibe_tools/push_to_github.py --vibe-tools")
                else:
                    print("[INFO] Tidak ada perubahan yang perlu di-commit.")
            else:
                print(f"[GAGAL] Gagal membuat commit: {err or stdout}")
                return False
        else:
            print("      Commit berhasil dibuat.")
    else:
        print("\n[INFO] Melompati 'git add' dan 'git commit' (hanya mem-push commit yang sudah ada).")

    # Tahap 2: Sinkronisasi dengan Remote (Pull Rebase jika diaktifkan)
    if lakukan_pull:
        print(f"\n[3/4] Menjalankan: git pull --rebase origin {branch}")
        kode, stdout, err = jalankan_perintah(f"git pull --rebase origin {branch}")
        if kode != 0:
            print("[PERINGATAN] Gagal pull/rebase dari remote. Mungkin branch belum ada di remote atau ada konflik.")
            print(f"Detail: {err or stdout}")
            if not auto_confirm:
                lanjut = tanya_konfirmasi("Apakah Anda ingin tetap mencoba melakukan push?", default_ya=True)
                if not lanjut:
                    print("[BATAL] Proses push dihentikan.")
                    return False
        else:
            print("      Sinkronisasi remote selesai.")
    else:
        print("\n[3/4] Melompati git pull sesuai instruksi.")

    # Tahap 3: Konfirmasi Terakhir (jika bukan mode auto-confirm)
    if not auto_confirm:
        print()
        if not tanya_konfirmasi(f"Kirimkan (push) perubahan ke GitHub branch '{branch}' sekarang?", default_ya=True):
            print("[BATAL] Push dibatalkan oleh pengguna. Perubahan commit lokal Anda tetap tersimpan.")
            return True

    # Tahap 4: Eksekusi Git Push
    print(f"\n[4/4] Mengirim commit ke GitHub: git push -u origin {branch} ...")
    kode, stdout, err = jalankan_perintah(f"git push -u origin {branch}")

    if kode == 0:
        print("\n" + "=" * 60)
        print("          BERHASIL! REPOSITORI TELAH DI-PUSH KE GITHUB")
        print("=" * 60)
        if stdout.strip():
            print(stdout.strip())
        elif err.strip():
            # Git push umumnya menuliskan ringkasan transmisi ke stderr
            print(err.strip())
        return True
    else:
        print("\n" + "=" * 60)
        print("               [GAGAL] PUSH KE GITHUB GAGAL")
        print("=" * 60)
        print(err or stdout)
        print("\nPetunjuk Perbaikan:")
        print("1. Jika ditolak karena non-fast-forward: Jalankan 'git pull --rebase origin <branch>' lalu coba lagi.")
        print("2. Jika masalah autentikasi: Pastikan Anda telah login via GitHub CLI ('gh auth login') atau menggunakan Personal Access Token (PAT) / SSH Key.")
        print("3. Jika ada file > 100MB: Hapus file tersebut dari riwayat git atau gunakan Git LFS.")
        return False


def main():
    """Fungsi utama untuk menangani argumen baris perintah."""
    parser = argparse.ArgumentParser(
        description="Skrip Python otomatis untuk mem-push perubahan ke GitHub tanpa konfirmasi."
    )
    parser.add_argument(
        "-m", "--message",
        type=str,
        default=None,
        help="Pesan commit kustom. Jika tidak diisi, otomatis menggunakan timestamp."
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Aktifkan mode interaktif jika ingin konfirmasi manual."
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        default=True,
        help="Otomatis konfirmasi tanpa meminta persetujuan manual (default: aktif)."
    )
    parser.add_argument(
        "--no-pull",
        action="store_true",
        help="Jangan lakukan 'git pull --rebase' sebelum melakukan push."
    )
    parser.add_argument(
        "-s", "--status",
        action="store_true",
        help="Hanya tampilkan ringkasan status perubahan dan commit tanpa melakukan add/commit/push."
    )
    parser.add_argument(
        "-C", "--dir",
        type=str,
        default=None,
        help="Direktori target repositori Git (misal: 'vibe_tools' atau path repositori lain)."
    )
    parser.add_argument(
        "--vibe-tools",
        action="store_true",
        help="Otomatis menargetkan repositori submodule vibe_tools."
    )

    args = parser.parse_args()

    # Menentukan direktori target repositori
    target_dir = None
    if args.vibe_tools:
        target_dir = Path(__file__).resolve().parent
    elif args.dir:
        target_dir = Path(args.dir).resolve()

    # Mode hanya status
    if args.status:
        cek_prasyarat(target_dir)
        branch = dapatkan_branch_aktif()
        remote_url = dapatkan_remote_info()
        daftar_perubahan = dapatkan_daftar_perubahan()
        unpushed_commits = cek_unpushed_commits(branch)
        tampilkan_ringkasan(branch, remote_url, daftar_perubahan, unpushed_commits)
        return

    # Secara default tanpa konfirmasi apapun (langsung push), kecuali diberikan flag --interactive
    auto_confirm = not args.interactive

    # Mode eksekusi push
    sukses = proses_git_push(
        pesan_commit=args.message,
        auto_confirm=auto_confirm,
        lakukan_pull=not args.no_pull,
        target_dir=target_dir
    )

    if not sukses:
        sys.exit(1)


if __name__ == "__main__":
    main()
