# -*- coding: utf-8 -*-
"""
[ID]: Skrip Otomasi Publikasi Rilis Executable ke GitHub Releases (Alur 2).
Fitur utama:
- Deteksi token GitHub dari github_token.txt atau variabel environment.
- Deteksi repositori GitHub tujuan secara otomatis.
- Cek dan tampilkan riwayat rilis yang telah ada di GitHub.
- Saran otomatis tag versi baru berbasis semantik atau tanggal.
- Ekstraksi log commit terakhir secara otomatis sebagai catatan rilis (changelog).
- Verifikasi dan pengompresian otomatis dist_scrapper/ACMT_Scrapper ke ZIP.
- Pembuatan GitHub Release dan pengunggahan aset biner ZIP (>100MB) via GitHub API.
- Indikator progres interaktif (tqdm / streaming upload).
- Tautan unduhan langsung dan panduan pembaruan untuk PC klien.

[EN]: GitHub Releases Automation Script for Executable Distribution.
"""

import os
import sys
import re
import json
import time
import shutil
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

# Konfigurasi encoding UTF-8 untuk terminal Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Direktori dasar proyek
BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "dist_scrapper"
APP_DIR = DIST_DIR / "ACMT_Scrapper"
ZIP_FILE = DIST_DIR / "ACMT_Scrapper.zip"
DEFAULT_REPO = "baliaga-repo/Scrapper_new_acmt"


def cetak_header():
    """Mencetak banner informasi publikasi rilis."""
    print("=" * 72)
    print("          PUBLIKASI RILIS GITHUB - SCRAPPER ACMT (.ZIP)")
    print("                 Distribusi Executable (Alur 2)")
    print("=" * 72)
    print(f"📂 Direktori Proyek : {BASE_DIR}")
    print(f"📦 Arsip Target     : {ZIP_FILE}")
    print("=" * 72 + "\n")


def dapatkan_github_token():
    """
[ID]: Mengambil GitHub Personal Access Token dari berbagai sumber lokal.
    Prioritas:
    1. File 'github_token.txt' di direktori proyek
    2. Variabel environment GITHUB_TOKEN atau GH_TOKEN
    3. Input interaktif via terminal

[EN]: Retrieve GitHub Personal Access Token from various local sources.
    Priority:
    1. 'github_token.txt' file in the project directory
    2. GITHUB_TOKEN or GH_TOKEN environment variable
    3. Interactive input via terminal
"""
    token_file = BASE_DIR / "github_token.txt"
    if token_file.exists():
        try:
            with open(token_file, "r", encoding="utf-8") as f:
                token = f.read().strip()
                if token:
                    return token
        except Exception:
            pass

    token_env = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token_env and token_env.strip():
        return token_env.strip()

    print("⚠️  Token GitHub tidak ditemukan di 'github_token.txt' maupun environment.")
    token_input = input("👉 Masukkan Personal Access Token (PAT) GitHub Anda: ").strip()
    if token_input:
        simpan = input("Simpan token ini ke 'github_token.txt'? (y/n): ").strip().lower()
        if simpan == "y":
            try:
                with open(token_file, "w", encoding="utf-8") as f:
                    f.write(token_input)
                print("✅ Token berhasil disimpan ke 'github_token.txt'.\n")
            except Exception as e:
                print(f"[WARNING] Gagal menyimpan token ke file: {e}\n")
        return token_input

    return None


def dapatkan_info_repo():
    """Mendeteksi nama repositori GitHub (owner/repo) dari git remote."""
    try:
        hasil = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=False
        )
        url = (hasil.stdout or "").strip()
        if url:
            # Pola HTTPS: https://github.com/owner/repo.git
            m = re.search(r"github\.com[/:]([\w\.-]+)/([\w\.-]+?)(?:\.git)?$", url)
            if m:
                return f"{m.group(1)}/{m.group(2)}"
    except Exception:
        pass
    return DEFAULT_REPO


def ambil_daftar_rilis(repo, token):
    """Mengambil daftar rilis yang sudah ada di repositori GitHub."""
    import urllib.request
    import urllib.error

    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "ACMT-Scrapper-ReleaseBot/1.0"
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            if res.status == 200:
                data = json.loads(res.read().decode("utf-8"))
                return data, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return None, str(e)
    return [], None


def ambil_log_commit_terakhir(jumlah=5):
    """Mengambil pesan commit git terakhir sebagai draf catatan perubahan."""
    try:
        hasil = subprocess.run(
            ["git", "log", f"-n{jumlah}", "--pretty=format:* %s (%h)"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=False
        )
        if hasil.returncode == 0 and hasil.stdout.strip():
            return hasil.stdout.strip()
    except Exception:
        pass
    return "- Pembaruan performa, perbaikan antarmuka, dan optimasi stabilitas."


def kompres_ke_zip(folder_sumber, file_zip):
    """Mengompresi folder distribusi ke dalam arsip ZIP."""
    print(f"\n📦 Mengompresi {folder_sumber.name} ke format ZIP...")
    temp_zip = file_zip.with_suffix(".tmp")
    if temp_zip.exists():
        try:
            temp_zip.unlink()
        except Exception:
            pass

    semua_file = []
    for root, _, files in os.walk(folder_sumber):
        for f in files:
            semua_file.append(Path(root) / f)

    total_files = len(semua_file)
    if total_files == 0:
        print("❌ Tidak ada berkas di dalam folder untuk dikompresi!")
        return False

    with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, file_path in enumerate(semua_file, 1):
            arcname = file_path.relative_to(folder_sumber.parent)
            zf.write(file_path, arcname)
            if idx % 50 == 0 or idx == total_files:
                persen = (idx / total_files) * 100
                print(f"\r⏳ Mengompresi: {idx}/{total_files} berkas ({persen:.1f}%)", end="", flush=True)

    print()
    if file_zip.exists():
        try:
            file_zip.unlink()
        except Exception:
            pass
    temp_zip.rename(file_zip)
    ukuran_mb = file_zip.stat().st_size / (1024 * 1024)
    print(f"✅ Arsip ZIP berhasil dibuat: {file_zip.name} ({ukuran_mb:.1f} MB)")
    return True


def pastikan_berkas_zip():
    """Memastikan berkas ACMT_Scrapper.zip siap untuk diunggah."""
    if not APP_DIR.exists():
        print(f"❌ Direktori biner '{APP_DIR}' belum ditemukan.")
        print("💡 Silakan jalankan 'BUILD_EXE.bat' terlebih dahulu untuk melakukan kompilasi PyInstaller.")
        return False

    if not ZIP_FILE.exists():
        print(f"ℹ️  Berkas arsip '{ZIP_FILE.name}' belum ada. Memulai kompresi otomatis...")
        return kompres_ke_zip(APP_DIR, ZIP_FILE)

    # Cek apakah folder biner lebih baru dibanding ZIP yang ada
    waktu_folder = max((f.stat().st_mtime for f in APP_DIR.rglob("*")), default=0)
    waktu_zip = ZIP_FILE.stat().st_mtime

    if waktu_folder > waktu_zip:
        print("⚠️  Folder 'ACMT_Scrapper' memiliki perubahan yang lebih baru dibanding berkas ZIP.")
        pilihan = input("Apakah Anda ingin memperbarui (re-compress) berkas ZIP sebelum diunggah? (Y/n): ").strip().lower()
        if pilihan != "n":
            return kompres_ke_zip(APP_DIR, ZIP_FILE)

    return True


def buat_rilis_github(repo, token, tag_name, judul, catatan, draft=False, prerelease=False):
    """
    Membuat draft atau rilis baru di GitHub menggunakan REST API.
    Mengembalikan data rilis (dict) atau None jika gagal.
    """
    import urllib.request
    import urllib.error

    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "ACMT-Scrapper-ReleaseBot/1.0"
    }

    payload = {
        "tag_name": tag_name,
        "target_commitish": "main",
        "name": judul,
        "body": catatan,
        "draft": draft,
        "prerelease": prerelease
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            if res.status in (200, 201):
                return json.loads(res.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        pesan_err = e.read().decode("utf-8", errors="replace")
        return None, f"HTTP Error {e.code}: {pesan_err}"
    except Exception as e:
        return None, str(e)

    return None, "Respon tidak dikenal dari GitHub API."


def hapus_aset_lama_jika_ada(repo, token, release_data, nama_aset):
    """Menghapus aset lama dengan nama yang sama jika rilis sudah pernah dibuat."""
    import urllib.request
    import urllib.error

    assets = release_data.get("assets", [])
    for asset in assets:
        if asset.get("name") == nama_aset:
            asset_id = asset.get("id")
            del_url = f"https://api.github.com/repos/{repo}/releases/assets/{asset_id}"
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "ACMT-Scrapper-ReleaseBot/1.0"
            }
            req = urllib.request.Request(del_url, headers=headers, method="DELETE")
            try:
                with urllib.request.urlopen(req, timeout=15) as res:
                    if res.status in (200, 204):
                        print(f"🗑️  Aset lama '{nama_aset}' (ID: {asset_id}) dihapus dari rilis.")
            except Exception as e:
                print(f"[WARNING] Gagal menghapus aset lama: {e}")


def unggah_aset_rilis(upload_url_template, token, file_path):
    """
    Mengunggah berkas biner ZIP ke GitHub Release Asset Endpoint.
    Mendukung tampilan progres unggah interaktif via tqdm atau requests streaming.
    """
    nama_berkas = file_path.name
    ukuran_berkas = file_path.stat().st_size
    ukuran_mb = ukuran_berkas / (1024 * 1024)

    # Bersihkan pola URI template {?name,label}
    upload_url = re.sub(r"\{.*?\}", "", upload_url_template)
    upload_url = f"{upload_url}?name={nama_berkas}"

    print(f"\n🚀 Mengunggah aset: {nama_berkas} ({ukuran_mb:.1f} MB)...")
    print(f"👉 Target URL: {upload_url}")

    # Coba gunakan requests dan tqdm untuk progres streaming jika tersedia
    try:
        import requests
        from tqdm import tqdm

        class ProgressFileReader:
            def __init__(self, filepath, pbar):
                self._f = open(filepath, "rb")
                self._pbar = pbar

            def read(self, size=-1):
                chunk = self._f.read(size)
                if chunk:
                    self._pbar.update(len(chunk))
                return chunk

            def __len__(self):
                return ukuran_berkas

            def close(self):
                self._f.close()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/zip",
            "Content-Length": str(ukuran_berkas),
            "User-Agent": "ACMT-Scrapper-ReleaseBot/1.0"
        }

        with tqdm(total=ukuran_berkas, unit="B", unit_scale=True, unit_divisor=1024, desc="Upload") as pbar:
            reader = ProgressFileReader(file_path, pbar)
            try:
                response = requests.post(upload_url, data=reader, headers=headers, timeout=600)
            finally:
                reader.close()

        if response.status_code in (200, 201):
            print("✅ Unggahan aset berhasil diselesaikan!")
            return response.json(), None
        else:
            return None, f"HTTP Error {response.status_code}: {response.text}"

    except ImportError:
        # Fallback menggunakan urllib standar
        import urllib.request
        import urllib.error

        print("⏳ Membaca dan mengirim data biner via urllib (mohon tunggu)...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/zip",
            "Content-Length": str(ukuran_berkas),
            "User-Agent": "ACMT-Scrapper-ReleaseBot/1.0"
        }

        with open(file_path, "rb") as f:
            data = f.read()

        req = urllib.request.Request(upload_url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=600) as res:
                if res.status in (200, 201):
                    hasil = json.loads(res.read().decode("utf-8"))
                    print("✅ Unggahan aset berhasil diselesaikan!")
                    return hasil, None
        except urllib.error.HTTPError as e:
            return None, f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='replace')}"
        except Exception as e:
            return None, str(e)

    return None, "Gagal mengunggah aset."


def main():
    """Fungsi eksekusi alur rilis GitHub secara interaktif."""
    cetak_header()

    # 1. Ambil Token
    token = dapatkan_github_token()
    if not token:
        print("❌ Operasi dibatalkan: Token GitHub diperlukan untuk mempublikasikan rilis.")
        return 1

    # 2. Ambil Info Repositori
    repo = dapatkan_info_repo()
    print(f"🔗 Target Repositori : {repo}")

    # 3. Cek Riwayat Rilis di GitHub
    print("🔍 Mengambil informasi rilis sebelumnya dari GitHub...")
    daftar_rilis, err = ambil_daftar_rilis(repo, token)
    if err:
        print(f"⚠️  Peringatan saat mengambil daftar rilis: {err}")
        daftar_rilis = []

    tag_terakhir = None
    if daftar_rilis:
        print("\n📋 3 Rilis Terakhir di Repositori:")
        for r in daftar_rilis[:3]:
            tgl = r.get("published_at", "")[:10]
            print(f"   • {r.get('tag_name')} - {r.get('name')} ({tgl})")
        tag_terakhir = daftar_rilis[0].get("tag_name")
    else:
        print("ℹ️  Belum ada rilis yang dipublikasikan di repositori ini.")

    # 4. Tentukan Tag Versi Baru
    sekarang = datetime.now()
    tag_saran = f"v{sekarang.strftime('%Y.%m.%d')}"
    if tag_terakhir:
        # Coba auto-increment jika format semantik vX.Y.Z
        m = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", tag_terakhir)
        if m:
            major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
            tag_saran = f"v{major}.{minor}.{patch + 1}"

    print(f"\n💡 Tag versi disarankan: {tag_saran}")
    tag_input = input(f"👉 Masukkan Tag Versi Rilis [{tag_saran}]: ").strip()
    tag_name = tag_input if tag_input else tag_saran
    if not tag_name.startswith("v"):
        tag_name = "v" + tag_name

    # 5. Tentukan Judul Rilis
    judul_default = f"ACMT Scrapper {tag_name}"
    judul_input = input(f"👉 Masukkan Judul Rilis [{judul_default}]: ").strip()
    judul_rilis = judul_input if judul_input else judul_default

    # 6. Tentukan Catatan Perubahan (Changelog)
    log_commit = ambil_log_commit_terakhir(5)
    catatan_default = f"### Pembaruan Rilis {tag_name} ({sekarang.strftime('%d-%m-%Y')})\n\n"
    catatan_default += f"**Daftar Perubahan:**\n{log_commit}\n\n"
    catatan_default += "**Instruksi untuk Klien:**\n"
    catatan_default += "1. Unduh file `ACMT_Scrapper.zip` di bawah ini.\n"
    catatan_default += "2. Ekstrak ke folder yang diinginkan atau jalankan `UPDATE_APLIKASI.bat` pada PC klien.\n"
    catatan_default += "3. Buka `START_ACMT.bat` untuk menjalankan aplikasi."

    print("\n📝 Catatan Perubahan (Draf Otomatis):")
    print("-" * 50)
    print(catatan_default)
    print("-" * 50)
    edit_catatan = input("Gunakan draf catatan di atas? (Y/n/custom): ").strip().lower()
    catatan_rilis = catatan_default
    if edit_catatan == "custom":
        catatan_kustom = input("👉 Masukkan catatan singkat rilis: ").strip()
        if catatan_kustom:
            catatan_rilis = f"### Pembaruan Rilis {tag_name}\n\n{catatan_kustom}\n\n" + catatan_default.split("**Instruksi untuk Klien:**")[-1]

    # 7. Pastikan Berkas ZIP Tersedia
    if not pastikan_berkas_zip():
        return 1

    ukuran_zip_mb = ZIP_FILE.stat().st_size / (1024 * 1024)

    # 8. Konfirmasi Final
    print("\n" + "=" * 72)
    print("                RINGKASAN PUBLIKASI RILIS")
    print("=" * 72)
    print(f"📦 Repositori   : {repo}")
    print(f"🏷️  Tag Versi    : {tag_name}")
    print(f"📌 Judul Rilis  : {judul_rilis}")
    print(f"📁 Berkas Aset  : {ZIP_FILE.name} ({ukuran_zip_mb:.1f} MB)")
    print("=" * 72)

    konfirmasi = input("\n👉 Siap mempublikasikan rilis ini ke GitHub? (Y/n): ").strip().lower()
    if konfirmasi == "n":
        print("❌ Publikasi rilis dibatalkan oleh pengguna.")
        return 0

    # 9. Cek apakah rilis dengan tag ini sudah ada
    release_target = None
    for r in daftar_rilis:
        if r.get("tag_name") == tag_name:
            release_target = r
            break

    if release_target:
        print(f"\nℹ️  Rilis dengan tag '{tag_name}' sudah ada (ID: {release_target.get('id')}).")
        hapus_aset_lama_jika_ada(repo, token, release_target, ZIP_FILE.name)
    else:
        print(f"\n🚀 Membuat entri rilis baru '{tag_name}' di GitHub...")
        release_target, err = buat_rilis_github(
            repo=repo,
            token=token,
            tag_name=tag_name,
            judul=judul_rilis,
            catatan=catatan_rilis
        )
        if err or not release_target:
            print(f"❌ Gagal membuat rilis di GitHub: {err}")
            return 1
        print(f"✅ Rilis berhasil dibuat! (ID: {release_target.get('id')})")

    # 10. Unggah Aset ZIP
    upload_url_template = release_target.get("upload_url", "")
    if not upload_url_template:
        print("❌ Gagal mendapatkan upload_url dari respon GitHub API.")
        return 1

    asset_result, err_upload = unggah_aset_rilis(upload_url_template, token, ZIP_FILE)
    if err_upload:
        print(f"❌ Gagal mengunggah aset biner: {err_upload}")
        return 1

    # 11. Tampilkan Informasi Berhasil
    html_url = release_target.get("html_url", f"https://github.com/{repo}/releases/tag/{tag_name}")
    download_url = f"https://github.com/{repo}/releases/download/{tag_name}/{ZIP_FILE.name}"
    latest_url = f"https://github.com/{repo}/releases/latest"

    print("\n" + "=" * 72)
    print("🎉 SUKSES BESAR! RILIS EXECUTABLE BERHASIL DIPUBLIKASIKAN KE GITHUB!")
    print("=" * 72)
    print(f"🌐 Halaman Rilis GitHub : {html_url}")
    print(f"📥 Unduh Aset ZIP       : {download_url}")
    print(f"🔄 URL Rilis Terbaru    : {latest_url}")
    print("-" * 72)
    print("💡 CARA PENGGUNAAN DI PC KLIEN:")
    print("1. Klien dapat menjalankan 'UPDATE_APLIKASI.bat' di folder ACMT_Scrapper untuk update otomatis.")
    print("2. Atau unduh 'ACMT_Scrapper.zip' dari halaman rilis dan ekstrak langsung.")
    print("=" * 72 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
