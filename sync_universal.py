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
import re
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


def buat_junction(sumber_asli: str, target_link: str, nama_komponen: str) -> bool:
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


def sanitasi_frontmatter_rules(rule_dirs: list[str]) -> int:
    """[ID]: Men-sanitasi YAML frontmatter pada seluruh file rule (.md) agar bebas unmarshal error."""
    diperbaiki = 0
    pola_globs_seq = re.compile(r"^(\s*globs\s*:\s*)\[(.*?)\]\s*$", re.MULTILINE)

    for rdir in rule_dirs:
        if not os.path.isdir(rdir):
            continue
        for fname in sorted(os.listdir(rdir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(rdir, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    teks_asli = f.read()
            except Exception:
                continue

            teks = teks_asli
            lines = teks.splitlines()

            # 1. Pastikan memiliki YAML frontmatter pembuka di baris pertama
            if not lines or lines[0].strip() != "---":
                judul = fname.replace(".md", "").replace("-", " ").title()
                body_aman = "\n".join("***" if ln.strip() == "---" else ln for ln in lines)
                teks = (
                    f"---\ntrigger: always_on\ndescription: Custom rule for {judul}.\n---\n\n{body_aman}\n"
                )
            else:
                end_idx = None
                for idx in range(1, len(lines)):
                    if lines[idx].strip() == "---":
                        end_idx = idx
                        break
                if end_idx is not None:
                    fm_block = "\n".join(lines[1:end_idx])

                    def _ubah_seq_ke_str(match: re.Match) -> str:
                        prefix = match.group(1)
                        isi = [x.strip().strip("\"'") for x in match.group(2).split(",") if x.strip()]
                        return f'{prefix}"{", ".join(isi)}"'

                    fm_baru = pola_globs_seq.sub(_ubah_seq_ke_str, fm_block)
                    if "trigger:" not in fm_baru:
                        fm_baru = "trigger: always_on\n" + fm_baru
                    body_lines = ["***" if ln.strip() == "---" else ln for ln in lines[end_idx + 1 :]]
                    if fm_baru != fm_block or any(ln.strip() == "---" for ln in lines[end_idx + 1 :]):
                        teks = "---\n" + fm_baru + "\n---\n" + "\n".join(body_lines) + "\n"

            if teks != teks_asli:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(teks)
                diperbaiki += 1
                print(f"[SANITASI] Frontmatter diperbaiki otomatis: {fpath}")

    return diperbaiki


def sinkronkan_memori_hermes() -> bool:
    """
    [ID]: Menyinkronkan aturan self-learning universal dari vibe_tools/rules/universal-self-learning.md
    ke memori jangka panjang Hermes Agent (~/.hermes/memories/MEMORY.md) agar lintas perangkat selalu identik.
    """
    sumber_rule = os.path.join(LOCAL_RULES_DIR, "universal-self-learning.md")
    if not os.path.isfile(sumber_rule):
        return False

    hermes_mem_dir = os.path.expanduser(r"~\.hermes\memories")
    hermes_mem_file = os.path.join(hermes_mem_dir, "MEMORY.md")

    try:
        with open(sumber_rule, "r", encoding="utf-8") as f:
            teks = f.read()

        # Hilangkan blok YAML frontmatter di baris awal jika ada untuk kebersihan MEMORY.md Hermes
        lines = teks.splitlines()
        if lines and lines[0].strip() == "---":
            for idx in range(1, len(lines)):
                if lines[idx].strip() == "---":
                    teks = "\n".join(lines[idx + 1 :]).lstrip() + "\n"
                    break

        os.makedirs(hermes_mem_dir, exist_ok=True)
        with open(hermes_mem_file, "w", encoding="utf-8") as f:
            f.write(teks)
        print(f"[OK] Memori Hermes disinkronkan: {hermes_mem_file}")
        return True
    except Exception as e:
        print(f"[WARN] Gagal menyinkronkan memori Hermes: {e}")
        return False


def sinkronisasi_universal():
    """[ID]: Titik masuk utama sinkronisasi ekosistem universal."""
    print("=" * 70)
    print("🚀 SINKRONISASI UNIVERSAL VIBE TOOLS -> ANTIGRAVITY GLOBAL")
    print(f"Master Path : {VIBE_TOOLS_DIR}")
    print(f"Global Root : {GLOBAL_CONFIG_DIR}")
    print("=" * 70)

    # 0. Sanitasi otomatis YAML frontmatter di vibe_tools/rules dan .agents/rules workspace
    workspace_rules_dir = os.path.join(os.path.dirname(VIBE_TOOLS_DIR), ".agents", "rules")
    sanitasi_frontmatter_rules([LOCAL_RULES_DIR, workspace_rules_dir])

    # 1. Hubungkan Skills
    ok_skills = buat_junction(LOCAL_SKILLS_DIR, GLOBAL_SKILLS_DIR, "Skills")

    # 2. Hubungkan Rules
    ok_rules = buat_junction(LOCAL_RULES_DIR, GLOBAL_RULES_DIR, "Rules")

    # 3. Sinkronkan Memori Jangka Panjang Hermes Agent (~/.hermes/memories/MEMORY.md)
    sinkronkan_memori_hermes()

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
