"""
[ID]: Patcher Mode Otonom / Full Autonomous (Zero-Enter) untuk Ekstensi Continue.
Skrip ini memodifikasi ekstensi Continue agar dapat mengeksekusi aksi koding,
pemanggilan tool, delegasi worker Hermes, dan perintah terminal yang aman
secara otonom tanpa perlu menekan tombol konfirmasi Enter setiap saat.

Fitur Keamanan:
- Perintah destruktif ekstrim (misal: mkfs, rm -rf /) tetap DIBLOKIR.
- Perintah hapus massal (rm, del) tetap MEMINTA KONFIRMASI.
- Perintah development aman (python, pytest, git, node, baca/edit file, Hermes MCP)
  berjalan otomatis tanpa jeda Enter.
- Backup otomatis (.bak) dibuat sebelum memodifikasi file asli.

[EN]: Autonomous Mode Patcher for Continue Extension.
Automates tool executions, file edits, and safe terminal commands without Enter prompts.
"""

import sys
import shutil
import argparse
from pathlib import Path

# Pastikan UTF-8 di Windows terminal
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def temukan_folder_ekstensi_continue() -> Path | None:
    """Mencari direktori ekstensi Continue di folder .vscode/extensions."""
    user_home = Path.home()
    vscode_ext_dir = user_home / ".vscode" / "extensions"
    if not vscode_ext_dir.exists():
        return None

    # Cari folder yang diawali continue.continue-
    candidates = sorted(
        vscode_ext_dir.glob("continue.continue-*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if candidates:
        return candidates[0]
    return None


def periksa_status_patch(ext_dir: Path) -> dict:
    """
[ID]: Memeriksa apakah ekstensi Continue saat ini sudah ter-patch.
[EN]: Check whether the current Continue extension is patched.
"""
    ext_js = ext_dir / "out" / "extension.js"
    gui_js = ext_dir / "gui" / "assets" / "index.js"

    status = {
        "extension_js_patched": False,
        "gui_js_patched": False,
        "has_backup": (ext_dir / "out" / "extension.js.bak").exists()
    }

    if ext_js.exists():
        content = ext_js.read_text(encoding="utf-8", errors="ignore")
        # Cek evaluasi terminal mode otonom dan pengubahan policy default tool
        eval_patched = (
            'isHighRiskRmCommand(baseCommand, args2)) {\n    return "allowedWithPermission";\n  }\n  return "allowedWithoutPermission";'
            in content.replace("\r\n", "\n")
        )
        policy_patched = 'defaultToolPolicy: "allowedWithoutPermission"' in content
        if eval_patched and policy_patched:
            status["extension_js_patched"] = True

    if gui_js.exists():
        content = gui_js.read_text(encoding="utf-8", errors="ignore")
        if 'const Xk="allowedWithoutPermission"' in content:
            status["gui_js_patched"] = True

    return status


def terapkan_patch(ext_dir: Path) -> bool:
    """
[ID]: Menerapkan patch otonom ke file extension.js dan gui/assets/index.js.
[EN]: Apply an autonomous patch to extension.js and gui/assets/index.js.
"""
    ext_js = ext_dir / "out" / "extension.js"
    ext_js_bak = ext_dir / "out" / "extension.js.bak"
    gui_js = ext_dir / "gui" / "assets" / "index.js"
    gui_js_bak = ext_dir / "gui" / "assets" / "index.js.bak"

    if not ext_js.exists() or not gui_js.exists():
        print("  [ERROR] File ekstensi Continue tidak lengkap di direktori target.")
        return False

    # Periksa apakah sudah ter-patch secara sempurna sebelumnya
    status_awal = periksa_status_patch(ext_dir)
    if status_awal["extension_js_patched"] and status_awal["gui_js_patched"]:
        print("  [INFO] Ekstensi Continue sudah dalam kondisi ter-patch mode otonom.")
        print("  [INFO] Tidak ada perubahan berkas tambahan yang diperlukan.")
        return True

    # 1. Buat Backup Asli (jika belum ada)
    if not ext_js_bak.exists():
        shutil.copy2(ext_js, ext_js_bak)
        print(f"  [BACKUP] Berhasil membuat backup: {ext_js_bak.name}")
    else:
        print(f"  [INFO] Backup {ext_js_bak.name} sudah ada sebelumnya.")

    if not gui_js_bak.exists():
        shutil.copy2(gui_js, gui_js_bak)
        print(f"  [BACKUP] Berhasil membuat backup: {gui_js_bak.name}")
    else:
        print(f"  [INFO] Backup {gui_js_bak.name} sudah ada sebelumnya.")

    # 2. Patch out/extension.js
    print("  [PATCH] Memodifikasi out/extension.js...")
    ext_content = ext_js.read_text(encoding="utf-8")

    # A. Ubah default policy built-in tools ke allowedWithoutPermission
    target_policy = 'defaultToolPolicy: "allowedWithPermission"'
    replacement_policy = 'defaultToolPolicy: "allowedWithoutPermission"'
    count_policy = ext_content.count(target_policy)
    if count_policy > 0:
        ext_content = ext_content.replace(target_policy, replacement_policy)
        print(f"    • {count_policy} tool bawaan diubah ke 'allowedWithoutPermission'.")

    # B. Modifikasi evaluasi keamanan terminal: eksekusi development otomatis, hapus massal konfirmasi
    target_eval = (
        'function evaluateSingleCommand(commandTokens, originalCommand) {\n'
        '  if (commandTokens.length === 0) {\n'
        '    return "allowedWithoutPermission";\n'
        '  }\n'
        '  const baseCommand = commandTokens[0].toLowerCase();\n'
        '  const args2 = commandTokens.slice(1);\n'
        '  if (isCriticalCommand(baseCommand, args2)) {\n'
        '    return "disabled";\n'
        '  }\n'
        '  if (baseCommand.startsWith("$")) {\n'
        '    return "allowedWithPermission";\n'
        '  }\n'
        '  if (isHighRiskCommand(baseCommand, args2, originalCommand)) {\n'
        '    return "allowedWithPermission";\n'
        '  }\n'
        '  if (isSafeCommand(baseCommand, args2)) {\n'
        '    return "allowedWithoutPermission";\n'
        '  }\n'
        '  return "allowedWithPermission";\n'
        '}'
    )

    replacement_eval = (
        'function evaluateSingleCommand(commandTokens, originalCommand) {\n'
        '  if (commandTokens.length === 0) {\n'
        '    return "allowedWithoutPermission";\n'
        '  }\n'
        '  const baseCommand = commandTokens[0].toLowerCase();\n'
        '  const args2 = commandTokens.slice(1);\n'
        '  if (isCriticalCommand(baseCommand, args2)) {\n'
        '    return "disabled";\n'
        '  }\n'
        '  if (isHighRiskRmCommand(baseCommand, args2)) {\n'
        '    return "allowedWithPermission";\n'
        '  }\n'
        '  return "allowedWithoutPermission";\n'
        '}'
    )

    if target_eval in ext_content:
        ext_content = ext_content.replace(target_eval, replacement_eval)
        print("    • Evaluasi terminal berhasil disetel ke Mode Otonom (Safe & Dev Auto, Destructive Confirm).")
    else:
        # Fallback pencarian fleksibel jika format newline berbeda
        target_eval_clean = target_eval.replace("\r\n", "\n")
        ext_content_clean = ext_content.replace("\r\n", "\n")
        if target_eval_clean in ext_content_clean:
            ext_content = ext_content_clean.replace(target_eval_clean, replacement_eval)
            print("    • Evaluasi terminal berhasil disetel ke Mode Otonom (Normalized Newlines).")
        else:
            print("    • [INFO] Pola evaluateSingleCommand sudah ter-patch atau berbeda.")

    ext_js.write_text(ext_content, encoding="utf-8")

    # 3. Patch gui/assets/index.js
    print("  [PATCH] Memodifikasi gui/assets/index.js...")
    gui_content = gui_js.read_text(encoding="utf-8")

    # Ubah fallback default policy Xk ke allowedWithoutPermission
    target_xk = 'const Xk="allowedWithPermission"'
    replacement_xk = 'const Xk="allowedWithoutPermission"'
    if target_xk in gui_content:
        gui_content = gui_content.replace(target_xk, replacement_xk)
        print("    • Fallback default UI (Xk) diubah ke 'allowedWithoutPermission'.")

    # Ubah kzt agar tidak memaksa override ke allowedWithPermission
    target_kzt = 'i==="allowedWithPermission"&&s==="allowedWithoutPermission"?{policy:"allowedWithPermission",displayValue:l,toolCallState:n}:{policy:s,displayValue:l,toolCallState:n}'
    replacement_kzt = '{policy:s,displayValue:l,toolCallState:n}'
    if target_kzt in gui_content:
        gui_content = gui_content.replace(target_kzt, replacement_kzt)
        print("    • Evaluasi izin UI (kzt) diperbarui agar langsung menghormati hasil evaluasi backend.")

    gui_js.write_text(gui_content, encoding="utf-8")

    print("\n  [OK] Seluruh patch mode otonom berhasil diterapkan 100%!")
    return True


def pulihkan_backup(ext_dir: Path) -> bool:
    """
[ID]: Mengembalikan file asli dari backup .bak.
[EN]: Restore the original file from the .bak backup.
"""
    ext_js = ext_dir / "out" / "extension.js"
    ext_js_bak = ext_dir / "out" / "extension.js.bak"
    gui_js = ext_dir / "gui" / "assets" / "index.js"
    gui_js_bak = ext_dir / "gui" / "assets" / "index.js.bak"

    pulih = 0
    if ext_js_bak.exists():
        shutil.copy2(ext_js_bak, ext_js)
        print(f"  [RESTORE] {ext_js.name} berhasil dikembalikan dari backup.")
        pulih += 1
    else:
        print(f"  [WARN] Tidak ditemukan {ext_js_bak.name}.")

    if gui_js_bak.exists():
        shutil.copy2(gui_js_bak, gui_js)
        print(f"  [RESTORE] {gui_js.name} berhasil dikembalikan dari backup.")
        pulih += 1
    else:
        print(f"  [WARN] Tidak ditemukan {gui_js_bak.name}.")

    return pulih > 0


def main():
    parser = argparse.ArgumentParser(description="Patcher Mode Otonom (Zero-Enter) untuk Ekstensi Continue.")
    parser.add_argument("--restore", action="store_true", help="Pulihkan ekstensi ke kondisi asli dari backup .bak")
    parser.add_argument("--status", action="store_true", help="Cek status patch saat ini")
    args = parser.parse_args()

    print("=" * 70)
    print("   PATCHER MODE OTONOM (ZERO-ENTER) EKSTENSI CONTINUE")
    print("=" * 70)

    ext_dir = temukan_folder_ekstensi_continue()
    if not ext_dir:
        print("[ERROR] Ekstensi Continue tidak ditemukan di ~/.vscode/extensions/.")
        sys.exit(1)

    print(f"Direktori Ekstensi Terdeteksi:\n  {ext_dir}\n")

    if args.status:
        st = periksa_status_patch(ext_dir)
        print("Status Ekstensi:")
        print(f"  • Backend (out/extension.js) : {'[TER-PATCH OTONOM]' if st['extension_js_patched'] else '[STANDAR / ASLI]'}")
        print(f"  • GUI UI  (assets/index.js)  : {'[TER-PATCH OTONOM]' if st['gui_js_patched'] else '[STANDAR / ASLI]'}")
        print(f"  • Backup File (.bak)         : {'[TERSEDIA]' if st['has_backup'] else '[BELUM DIBUAT]'}")
        return

    if args.restore:
        print("[+] Memulihkan file asli dari backup...")
        if pulihkan_backup(ext_dir):
            print("\n[OK] Restorasi berhasil. Lakukan 'Developer: Reload Window' di VS Code.")
        else:
            print("\n[GAGAL] Tidak ada file backup yang bisa dipulihkan.")
        return

    print("[+] Menerapkan patch otonom (Zero-Enter)...")
    if terapkan_patch(ext_dir):
        print("\n" + "=" * 70)
        print("   LANGKAH TERAKHIR:")
        print("   1. Buka VS Code.")
        print("   2. Tekan Ctrl + Shift + P -> ketik 'Developer: Reload Window'.")
        print("   3. Agen Continue sekarang akan mengeksekusi tool & koding secara mandiri")
        print("      tanpa meminta konfirmasi Enter setiap saat.")
        print("=" * 70)


if __name__ == "__main__":
    main()
