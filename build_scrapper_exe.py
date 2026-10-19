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
    """Membuat file batch pendamping ramah pengguna di folder hasil build."""
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


def build_scrapper(console_mode=False):
    """
    Eksekutor utama proses compile PyInstaller Onedir untuk Scrapper ACMT.
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

    # Buat template file github_token.txt jika belum ada
    token_dest = os.path.join(app_output_dir, "github_token.txt")
    if not os.path.exists(token_dest):
        try:
            with open(token_dest, "w", encoding="utf-8") as f:
                f.write("")
            print("✅ File template github_token.txt disiapkan.")
        except Exception:
            pass

    print("\n" + "=" * 70)
    print("🎉 SUKSES! Executable ACMT Scrapper berhasil dibuat:")
    print(f"👉 Lokasi Rilis: {app_output_dir}")
    print(f"👉 File Eksekusi: {os.path.join(app_output_dir, 'START_ACMT.bat')}")
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
