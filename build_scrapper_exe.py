"""
[ID]: Modul Pembuat Executable Mandiri (.EXE) untuk Scrapper ACMT.
Mengemas aplikasi ke dalam format folder portabel (PyInstaller --onedir),
menyertakan PyInstaller hooks khusus untuk Playwright, dan menyiapkan
seluruh launcher serta berkas panduan deployment PC klien.

[EN]: Standalone executable (.EXE) builder module for the ACMT Scrapper.
Packages the application into a portable folder format (PyInstaller --onedir),
includes custom PyInstaller hooks for Playwright, and prepares
all launchers and client PC deployment guide files.
"""

import os
import sys
import shutil
import subprocess

# Pastikan konfigurasi UTF-8 console output aman di Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def pastikan_pyinstaller():
    """
[ID]: Memastikan paket PyInstaller tersedia di environment Python saat ini.
[EN]: Ensure the PyInstaller package is available in the current Python environment.
"""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("[INFO] PyInstaller belum terpasang. Memasang PyInstaller via pip...")
        res = subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"])
        return res.returncode == 0


def buat_launcher_bat(target_dir):
    """
[ID]: Membuat file batch pendamping ramah pengguna di folder hasil build.
[EN]: Create a user-friendly companion batch file in the build output folder.
"""
    launcher_path = os.path.join(target_dir, "START_ACMT.bat")
    content = """@echo off
title Scrapper ACMT Runner
cd /d "%~dp0"

:: Set path penyimpanan browser Chromium lokal ke subfolder pw-browsers
set "PLAYWRIGHT_BROWSERS_PATH=%~dp0pw-browsers"

:: Jalankan biner aplikasi utama
start "" "%~dp0scrapper_runner.exe" %*
exit
"""
    try:
        with open(launcher_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Launcher dibuat: {launcher_path}")
    except Exception as e:
        print(f"[WARNING] Gagal membuat launcher batch: {e}")


def buat_updater_bat(target_dir):
    """
    [ID]: Membuat file batch updater mandiri di folder klien untuk mengunduh update dari GitHub Releases.
    """
    updater_path = os.path.join(target_dir, "UPDATE_APLIKASI.bat")
    content = """@echo off
title Update ACMT Scrapper
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo =================================================================
echo             PEMBARUAN APLIKASI ACMT SCRAPPER (GITHUB)
echo =================================================================
echo Direktori Aplikasi: %CD%
echo.

:: 1. Deteksi token GitHub
set "TOKEN="
if exist "%~dp0github_token.txt" (
    set /p TOKEN=<"%~dp0github_token.txt"
)
if not defined TOKEN if defined GITHUB_TOKEN (
    set "TOKEN=%GITHUB_TOKEN%"
)

if not defined TOKEN (
    echo [ERROR] Token GitHub tidak ditemukan di github_token.txt.
    echo Silakan isi token GitHub Anda terlebih dahulu.
    echo.
    pause
    exit /b 1
)

:: 2. Jalankan PowerShell untuk cek rilis terbaru dan unduh
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference = 'Stop'; " ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "$token = '%TOKEN%'.Trim(); " ^
    "$repo = 'baliaga-repo/Scrapper_new_acmt'; " ^
    "$headers = @{ 'Authorization' = \\"Bearer $token\\"; 'User-Agent' = 'ACMT-Updater/1.0'; 'Accept' = 'application/vnd.github.v3+json' }; " ^
    "Write-Host '🔍 Memeriksa rilis terbaru di GitHub...' -ForegroundColor Cyan; " ^
    "try { $release = Invoke-RestMethod -Uri \\"https://api.github.com/repos/$repo/releases/latest\\" -Headers $headers -Method Get; } " ^
    "catch { Write-Host \\"❌ Gagal menghubungi GitHub API: $_\\" -ForegroundColor Red; exit 1 }; " ^
    "$tag = $release.tag_name; " ^
    "$name = $release.name; " ^
    "Write-Host \\"👉 Versi Rilis Terbaru : $tag ($name)\\" -ForegroundColor Green; " ^
    "$asset = $release.assets | Where-Object { $_.name -like '*ACMT_Scrapper*.zip' } | Select-Object -First 1; " ^
    "if (-not $asset) { Write-Host '❌ Aset ACMT_Scrapper.zip tidak ditemukan pada rilis ini!' -ForegroundColor Red; exit 1 }; " ^
    "Write-Host ('📦 Ukuran Aset       : {0:N1} MB' -f ($asset.size / 1MB)) -ForegroundColor Yellow; " ^
    "$confirm = Read-Host 'Apakah Anda ingin mengunduh dan menerapkan pembaruan ini? (Y/T)'; " ^
    "if ($confirm -notmatch '^[Yy]') { Write-Host 'Pembaruan dibatalkan oleh pengguna.' -ForegroundColor Gray; exit 0 }; " ^
    "Write-Host '⏳ Mengunduh arsip rilis terbaru...' -ForegroundColor Cyan; " ^
    "$tempZip = [System.IO.Path]::Combine($env:TEMP, 'ACMT_Scrapper_update.zip'); " ^
    "$downloadHeaders = @{ 'Authorization' = \\"Bearer $token\\"; 'User-Agent' = 'ACMT-Updater/1.0'; 'Accept' = 'application/octet-stream' }; " ^
    "Invoke-WebRequest -Uri $asset.url -Headers $downloadHeaders -OutFile $tempZip; " ^
    "Write-Host '✅ Unduhan selesai!' -ForegroundColor Green; " ^
    "Write-Host '🔄 Menutup proses scrapper yang berjalan...' -ForegroundColor Cyan; " ^
    "Stop-Process -Name 'scrapper_runner' -Force -ErrorAction SilentlyContinue; " ^
    "Start-Sleep -Seconds 1; " ^
    "Write-Host '📦 Menerapkan pembaruan...' -ForegroundColor Cyan; " ^
    "$extractDir = [System.IO.Path]::Combine($env:TEMP, 'acmt_extract_temp'); " ^
    "if (Test-Path $extractDir) { Remove-Item $extractDir -Recurse -Force }; " ^
    "Expand-Archive -Path $tempZip -DestinationPath $extractDir -Force; " ^
    "$srcFolder = [System.IO.Path]::Combine($extractDir, 'ACMT_Scrapper'); " ^
    "if (-not (Test-Path $srcFolder)) { $srcFolder = $extractDir }; " ^
    "Copy-Item -Path \\"$srcFolder\\*\\" -Destination '%~dp0' -Recurse -Force -Exclude 'konfigurasi.py','last_config.json','github_token.txt'; " ^
    "Remove-Item $tempZip -Force -ErrorAction SilentlyContinue; " ^
    "Remove-Item $extractDir -Recurse -Force -ErrorAction SilentlyContinue; " ^
    "Write-Host '🎉 PEMBARUAN BERHASIL DITERAPKAN!' -ForegroundColor Green; " ^
    "Write-Host 'Silakan jalankan kembali aplikasi menggunakan START_ACMT.bat.' -ForegroundColor Cyan"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Proses pembaruan gagal atau dibatalkan.
) else (
    echo.
    echo =================================================================
    echo [SELESAI] Aplikasi berhasil diperbarui ke versi terbaru!
    echo =================================================================
)
pause
"""
    try:
        with open(updater_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Updater dibuat: {updater_path}")
    except Exception as e:
        print(f"[WARNING] Gagal membuat updater batch: {e}")


def buat_arsip_zip(source_dir, zip_path):
    """
    [ID]: Mengompresi seluruh isi direktori rilis ke dalam file arsip ZIP untuk distribusi GitHub Releases.
    """
    import zipfile
    print(f"\n📦 Mengompresi direktori rilis ke arsip ZIP...")
    print(f"👉 Target File: {zip_path}")

    temp_zip = zip_path + ".tmp"
    if os.path.exists(temp_zip):
        try:
            os.remove(temp_zip)
        except Exception:
            pass

    total_files = sum(len(files) for _, _, files in os.walk(source_dir))
    diproses = 0

    with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))
                zf.write(file_path, arcname)
                diproses += 1
                if diproses % 50 == 0 or diproses == total_files:
                    persen = (diproses / total_files) * 100
                    print(f"\r⏳ Mengompresi berkas: {diproses}/{total_files} ({persen:.1f}%)", end="", flush=True)

    print()
    if os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except Exception:
            pass
    os.rename(temp_zip, zip_path)
    ukuran_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ Arsip ZIP rilis berhasil dibuat ({ukuran_mb:.1f} MB): {zip_path}")



def build_scrapper(console_mode=False):
    """
[ID]: Eksekutor utama proses compile PyInstaller Onedir untuk Scrapper ACMT.
[EN]: Main executor for the PyInstaller Onedir compilation process for Scrapper ACMT.
"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_script = os.path.join(root_dir, "scrapper_runner.py")
    hooks_dir = os.path.join(root_dir, "vibe_tools", "hooks")
    dist_dir = os.path.join(root_dir, "dist_scrapper")
    work_dir = os.path.join(root_dir, "build_temp_scrapper")
    app_output_dir = os.path.join(dist_dir, "ACMT_Scrapper")

    print("=" * 70)
    print("       BUILD EXECUTABLE PORTABEL (.EXE) - SCRAPPER ACMT")
    print("=" * 70)
    print(f"📂 Direktori Proyek : {root_dir}")
    print(f"📄 Skrip Target     : {target_script}")
    print(f"📦 Direktori Output : {app_output_dir}")
    print("=" * 70)

    if not os.path.exists(target_script):
        print(f"❌ File target {target_script} tidak ditemukan!")
        return 1

    if not pastikan_pyinstaller():
        print("❌ Gagal memasang atau mendeteksi PyInstaller!")
        return 1

    # Perintah argumen PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--name=scrapper_runner",
        f"--distpath={dist_dir}",
        f"--workpath={work_dir}",
        f"--additional-hooks-dir={hooks_dir}",
        "--hidden-import=playwright",
        "--hidden-import=playwright.sync_api",
        "--hidden-import=playwright._impl._driver",
        "--hidden-import=greenlet",
        "--hidden-import=openpyxl",
        "--hidden-import=cryptography",
        "--hidden-import=pyautogui",
        "--hidden-import=pyperclip",
        "--hidden-import=psutil",
        "--hidden-import=xlwt",
        "--hidden-import=win32com",
        "--hidden-import=win32com.client",
        "--hidden-import=pythoncom",
        "--hidden-import=runner.security_guard",
        "--hidden-import=scrapper_core",
        "--hidden-import=konfigurasi",
        "--hidden-import=ACMT.update_prabayar",
        "--hidden-import=ACMT.update_prabayar_server",
        "--exclude-module=pytest",
        "--exclude-module=IPython",
        "--exclude-module=matplotlib",
    ]

    # Console vs Windowed mode
    if not console_mode:
        cmd.append("--windowed")

    # Tambahkan file target
    cmd.append(target_script)

    print("\n🚀 Menjalankan proses kompilasi PyInstaller...")
    hasil = subprocess.run(cmd)

    if hasil.returncode != 0:
        print(f"\n❌ Proses build gagal dengan kode keluar: {hasil.returncode}")
        return hasil.returncode

    # Ubah nama folder dist dari scrapper_runner menjadi ACMT_Scrapper untuk estetika dan kerapian
    default_dist_folder = os.path.join(dist_dir, "scrapper_runner")
    if os.path.exists(default_dist_folder):
        if os.path.exists(app_output_dir):
            try:
                shutil.rmtree(app_output_dir)
            except Exception:
                pass
        try:
            os.rename(default_dist_folder, app_output_dir)
        except Exception:
            app_output_dir = default_dist_folder

    # Salin berkas pelengkap ke dalam folder hasil rilis
    print("\n📦 Menyiapkan berkas pendukung ke folder distribusi...")
    buat_launcher_bat(app_output_dir)

    panduan_src = os.path.join(root_dir, "PANDUAN_PC_KLIEN.txt")
    if os.path.exists(panduan_src):
        try:
            shutil.copy2(panduan_src, os.path.join(app_output_dir, "PANDUAN_PC_KLIEN.txt"))
            print("✅ Berkas panduan PANDUAN_PC_KLIEN.txt disalin.")
        except Exception as e:
            print(f"[WARNING] Gagal menyalin panduan: {e}")

    access_src = os.path.join(root_dir, "access_control.json")
    if os.path.exists(access_src):
        try:
            shutil.copy2(access_src, os.path.join(app_output_dir, "access_control.json"))
            print("✅ Berkas template kontrol akses access_control.json disalin.")
        except Exception as e:
            print(f"[WARNING] Gagal menyalin access_control.json: {e}")

    # Salin berkas konfigurasi.py agar executable dapat membaca dan menyimpan preferensi
    cfg_src = os.path.join(root_dir, "konfigurasi.py")
    if os.path.exists(cfg_src):
        try:
            shutil.copy2(cfg_src, os.path.join(app_output_dir, "konfigurasi.py"))
            print("✅ Berkas konfigurasi.py disalin ke folder rilis.")
        except Exception as e:
            print(f"[WARNING] Gagal menyalin konfigurasi.py: {e}")

    # Salin binary pendukung enkripsi AP2T jika tersedia
    enkripsi_src = os.path.join(root_dir, "ACMT", "enkripsi-new-ap2t_windows.exe")
    if os.path.exists(enkripsi_src):
        dest_acmt = os.path.join(app_output_dir, "ACMT")
        os.makedirs(dest_acmt, exist_ok=True)
        try:
            shutil.copy2(enkripsi_src, os.path.join(dest_acmt, "enkripsi-new-ap2t_windows.exe"))
            print("✅ Binary pendukung enkripsi-new-ap2t_windows.exe disalin.")
        except Exception as e:
            print(f"[WARNING] Gagal menyalin enkripsi-new-ap2t_windows.exe: {e}")

    # Buat template file github_token.txt jika belum ada
    token_dest = os.path.join(app_output_dir, "github_token.txt")
    if not os.path.exists(token_dest):
        try:
            with open(token_dest, "w", encoding="utf-8") as f:
                f.write("")
            print("✅ File template github_token.txt disiapkan.")
        except Exception:
            pass

    # Buat updater batch di dalam folder rilis klien
    buat_updater_bat(app_output_dir)

    # Otomatisasi kompresi ke format ZIP untuk GitHub Releases
    zip_output = os.path.join(dist_dir, "ACMT_Scrapper.zip")
    buat_arsip_zip(app_output_dir, zip_output)

    print("\n" + "=" * 70)
    print("🎉 SUKSES! Executable ACMT Scrapper berhasil dibuat dan dikemas:")
    print(f"👉 Direktori Rilis : {app_output_dir}")
    print(f"👉 File Eksekusi   : {os.path.join(app_output_dir, 'START_ACMT.bat')}")
    print(f"👉 Updater Klien   : {os.path.join(app_output_dir, 'UPDATE_APLIKASI.bat')}")
    print(f"📦 Arsip ZIP Rilis : {zip_output}")
    print("=" * 70 + "\n")
    return 0


def main():
    """
[ID]: Fungsi pembungkus utama CLI.
[EN]: Main CLI wrapper function.
"""
    console_mode = "--console" in sys.argv or "-c" in sys.argv
    return build_scrapper(console_mode=console_mode)


if __name__ == "__main__":
    sys.exit(main())
