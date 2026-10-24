"""
[ID]: Skrip Sinkronisasi Universal Vibe Tools ke Antigravity IDE Global Root (~/.gemini/config).
Menghubungkan folder 'skills/' dan 'rules/' di vibe_tools ke Global Customization Root
menggunakan Windows NTFS Junction (mklink /J), sehingga SELURUH project di komputer ini
langsung mewarisi semua skill & rules secara universal tanpa perlu copy-paste.

[EN]: Universal Vibe Tools Sync Script to Antigravity IDE Global Root (~/.gemini/config).
Links 'skills/' and 'rules/' directories in vibe_tools to Global Customization Root
using Windows NTFS Junction (mklink /J), so ALL projects on this machine immediately
inherit all skills & rules universally with zero copy-pasting.
"""

import os
import shutil
import subprocess
import sys

# Pastikan output terminal mendukung UTF-8 pada Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

VIBE_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL_CONFIG_DIR = os.path.expanduser(r"~\.gemini\config")
GLOBAL_SKILLS_DIR = os.path.join(GLOBAL_CONFIG_DIR, "skills")
GLOBAL_RULES_DIR = os.path.join(GLOBAL_CONFIG_DIR, "rules")

LOCAL_SKILLS_DIR = os.path.join(VIBE_TOOLS_DIR, "skills")
LOCAL_RULES_DIR = os.path.join(VIBE_TOOLS_DIR, "rules")


def is_junction_or_symlink(path: str) -> bool:
    """[ID]: Memeriksa apakah suatu path adalah symbolic link atau NTFS junction."""
    if not os.path.exists(path):
        return False
    try:
        # os.path.islink mendeteksi symlink dan junction di Python 3.8+ Windows
        if os.path.islink(path):
            return True
        # Alternatif deteksi via atribut Windows
        import ctypes
        FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        return bool(attrs != -1 and (attrs & FILE_ATTRIBUTE_REPARSE_POINT))
    except Exception:
        return False


def buat_junction(sumber_asli: str, target_link: str, nama_komponen: str):
    """
    [ID]: Membuat Windows NTFS Junction dari target_link mengarah ke sumber_asli.
    Tidak memerlukan hak akses Administrator.
    """
    if not os.path.exists(sumber_asli):
        print(f"[ERROR] Sumber asli {nama_komponen} tidak ditemukan: {sumber_asli}")
        return False

    os.makedirs(os.path.dirname(target_link), exist_ok=True)

    if os.path.exists(target_link):
        if is_junction_or_symlink(target_link):
            print(f"[OK] {nama_komponen} sudah terhubung sebagai Junction: {target_link}")
            return True
        else:
            # Jika folder biasa, backup atau migrasikan isinya
            backup_path = target_link + "_backup_old"
            print(f"[INFO] Folder lama ditemukan. Memindahkan ke {backup_path}...")
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path, ignore_errors=True)
            try:
                os.rename(target_link, backup_path)
            except Exception as e:
                print(f"[WARN] Gagal rename folder lama: {e}. Mencoba rmdir...")
                shutil.rmtree(target_link, ignore_errors=True)

    # Buat junction menggunakan perintah bawaan Windows
    cmd = f'cmd /c mklink /J "{target_link}" "{sumber_asli}"'
    hasil = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if hasil.returncode == 0 or is_junction_or_symlink(target_link):
        print(f"[SUKSES] Junction berhasil dibuat: {target_link} -> {sumber_asli}")
        return True
    else:
        print(f"[GAGAL] Gagal membuat junction: {hasil.stderr or hasil.stdout}")
        return False


def sinkronisasi_universal():
    """[ID]: Titik masuk utama sinkronisasi ekosistem universal."""
    print("=" * 70)
    print("🚀 SINKRONISASI UNIVERSAL VIBE TOOLS -> ANTIGRAVITY GLOBAL")
    print(f"Master Path : {VIBE_TOOLS_DIR}")
    print(f"Global Root : {GLOBAL_CONFIG_DIR}")
    print("=" * 70)

    # 1. Hubungkan Skills
    ok_skills = buat_junction(LOCAL_SKILLS_DIR, GLOBAL_SKILLS_DIR, "Skills")

    # 2. Hubungkan Rules
    ok_rules = buat_junction(LOCAL_RULES_DIR, GLOBAL_RULES_DIR, "Rules")

    print("-" * 70)
    if ok_skills and ok_rules:
        print("✅ Seluruh Skills & Rules berhasil terhubung secara UNIVERSAL!")
        print("\nDaftar Skill Aktif:")
        if os.path.exists(LOCAL_SKILLS_DIR):
            for item in sorted(os.listdir(LOCAL_SKILLS_DIR)):
                skill_path = os.path.join(LOCAL_SKILLS_DIR, item, "SKILL.md")
                if os.path.isfile(skill_path):
                    print(f"  • /{item}")

        print("\nDaftar Rules Aktif:")
        if os.path.exists(LOCAL_RULES_DIR):
            for item in sorted(os.listdir(LOCAL_RULES_DIR)):
                if item.endswith(".md"):
                    print(f"  • {item}")

        print("\n✨ STATUS: Siap digunakan di SEMUA proyek di komputer ini tanpa perlu copas!")
    else:
        print("⚠️ Sinkronisasi selesai dengan peringatan. Silakan periksa pesan di atas.")
    print("=" * 70)


if __name__ == "__main__":
    sinkronisasi_universal()
