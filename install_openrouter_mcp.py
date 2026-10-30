"""[ID]: Installer Otomatis: OpenRouter MCP Server untuk Antigravity IDE.
Mengotomatiskan penyalinan server openrouter_mcp.py, konfigurasi openrouter_key.txt,
dan pendaftaran ke mcp_config.json secara mandiri dan cepat.

[EN]: Automatic Installer: OpenRouter MCP Server for Antigravity IDE.
Automates copying openrouter_mcp.py, configuring openrouter_key.txt,
and registering to mcp_config.json quickly and cleanly.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

# Pastikan UTF-8 di terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def cetak_langkah(pesan: str):
    print(f"\n[+] {pesan}")


def cetak_sukses(pesan: str):
    print(f"  [OK] {pesan}")


def cetak_error(pesan: str):
    print(f"  [ERROR] {pesan}")


def jalankan(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        cetak_error(f"Gagal: {cmd}")
        cetak_error(res.stderr.strip() or res.stdout.strip())
        return False, res.stderr
    return True, res.stdout


def main():
    print("=" * 65)
    print("   INSTALLER OTOMATIS: OPENROUTER MCP x ANTIGRAVITY IDE")
    print("=" * 65)

    user_home = Path.home()
    gemini_dir = user_home / ".gemini"
    gemini_config_dir = gemini_dir / "config"
    mcp_config_file = gemini_config_dir / "mcp_config.json"
    key_file = gemini_dir / "openrouter_key.txt"
    server_script = gemini_dir / "openrouter_mcp.py"

    # 1. Pastikan direktori global .gemini ada
    cetak_langkah("1. Memeriksa direktori konfigurasi global Antigravity...")
    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_config_dir.mkdir(parents=True, exist_ok=True)
    cetak_sukses(f"Direktori siap: {gemini_dir}")

    # 2. Instal pustaka pendukung (mcp saja, tanpa requests karena openrouter_mcp sudah pakai urllib)
    cetak_langkah("2. Menginstal pustaka Python yang dibutuhkan (mcp)...")
    ok, _ = jalankan(f'"{sys.executable}" -m pip install -q mcp')
    if ok:
        cetak_sukses("Pustaka mcp berhasil diverifikasi/terpasang.")
    else:
        cetak_error("Gagal menginstal dependensi mcp. Cek koneksi internet.")

    # 3. Salin berkas server openrouter_mcp.py ke ~/.gemini
    cetak_langkah("3. Memasang server bridge openrouter_mcp.py...")
    src_file = Path(__file__).resolve().parent / "openrouter_mcp.py"
    if src_file.exists():
        shutil.copy2(src_file, server_script)
        cetak_sukses(f"Skrip server disalin dari: {src_file} -> {server_script}")
    else:
        cetak_error(f"Berkas sumber tidak ditemukan di: {src_file}")
        return

    # 4. Tangani API Key
    cetak_langkah("4. Menyiapkan OpenRouter API Key...")
    if not key_file.exists() or not key_file.read_text(encoding="utf-8").strip():
        api_input = input("Masukkan OpenRouter API Key Anda (sk-or-v1-...) [atau tekan Enter untuk isi nanti]: ").strip()
        if api_input:
            key_file.write_text(api_input + "\n", encoding="utf-8")
            cetak_sukses("API Key berhasil disimpan ke openrouter_key.txt")
        else:
            key_file.write_text("TEMPEL_API_KEY_DISINI\n", encoding="utf-8")
            print(f"  [INFO] Berkas dibuat. Silakan tempelkan kunci Anda nanti di:\n         {key_file}")
    else:
        cetak_sukses(f"API Key sudah ada di: {key_file}")

    # 5. Konfigurasi mcp_config.json
    cetak_langkah("5. Mengonfigurasi mcp_config.json Antigravity...")
    cfg = {}
    if mcp_config_file.exists():
        try:
            cfg = json.loads(mcp_config_file.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}

    if "mcpServers" not in cfg:
        cfg["mcpServers"] = {}

    python_exe = sys.executable.replace("\\", "/")
    script_path = str(server_script.resolve()).replace("\\", "/")

    cfg["mcpServers"]["openrouter"] = {
        "command": python_exe,
        "args": [script_path]
    }

    mcp_config_file.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    cetak_sukses(f"Konfigurasi MCP tersimpan di: {mcp_config_file}")

    # 6. Selesai
    print("\n" + "=" * 65)
    print("   [SELESAI] OPENROUTER MCP SERVER BERHASIL DIPASANG!")
    print("=" * 65)
    print("Langkah selanjutnya:")
    print("1. Pastikan API Key di ~/.gemini/openrouter_key.txt sudah valid.")
    print("2. Restart Antigravity IDE.")
    print("3. Tool 'tanya_openrouter' & 'cek_koneksi_openrouter' langsung aktif!")


if __name__ == "__main__":
    main()
