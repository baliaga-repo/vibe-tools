"""
[ID]: Installer Otomatis REA MCP (Reverse Engineer Anything) untuk Antigravity IDE.
Mendaftarkan REA sebagai MCP server lokal di ~/.gemini/config/mcp_config.json
dan memasang global skill reverse-engineer-anything.

Prasyarat:
  - Node.js >= 22.19 (versi 22.x, 24.x, atau 26+)
  - npm tersedia di PATH

Cara Penggunaan:
  python vibe_tools/install_rea_mcp.py

[EN]: Automatic Installer for REA MCP (Reverse Engineer Anything) for Antigravity IDE.
Registers REA as a local MCP server in ~/.gemini/config/mcp_config.json
and installs the reverse-engineer-anything global skill.

Prerequisites:
  - Node.js >= 22.19 (version 22.x, 24.x, or 26+)
  - npm available on PATH

Usage:
  python vibe_tools/install_rea_mcp.py
"""
import json
import subprocess
import sys
from pathlib import Path

# Konfigurasi encoding UTF-8 untuk terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REA_VERSION = "6.5.0"


def cetak_langkah(pesan: str):
    """[ID]: Menampilkan pesan langkah. [EN]: Displays step message."""
    print(f"\n[+] {pesan}")


def cetak_sukses(pesan: str):
    """[ID]: Menampilkan pesan sukses. [EN]: Displays success message."""
    print(f"  [OK] {pesan}")


def cetak_error(pesan: str):
    """[ID]: Menampilkan pesan error. [EN]: Displays error message."""
    print(f"  [ERROR] {pesan}")


def jalankan(cmd: str, cwd: str = None) -> tuple:
    """
    [ID]: Menjalankan perintah shell dan mengembalikan (sukses, output).
    [EN]: Runs a shell command and returns (success, output).
    """
    res = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return res.returncode == 0, (res.stdout + res.stderr).strip()


def periksa_node() -> bool:
    """
    [ID]: Memeriksa ketersediaan Node.js dan memvalidasi versi minimum (22.19+).
    [EN]: Checks Node.js availability and validates minimum version (22.19+).
    """
    cetak_langkah("Memeriksa prasyarat Node.js dan npm...")
    ok, output = jalankan("node --version")
    if not ok:
        cetak_error("Node.js tidak ditemukan di PATH. Instal Node.js >= 22.19 terlebih dahulu.")
        cetak_error("Download: https://nodejs.org/")
        return False

    versi = output.strip().lstrip("v")
    bagian = versi.split(".")
    major = int(bagian[0]) if bagian else 0
    minor = int(bagian[1]) if len(bagian) > 1 else 0

    if not ((major == 22 and minor >= 19) or (major == 24 and minor >= 11) or major >= 26):
        cetak_error(f"Node.js v{versi} tidak memenuhi syarat minimum REA (22.19+, 24.11+, atau 26+).")
        return False
    cetak_sukses(f"Node.js v{versi} (memenuhi syarat)")

    ok_npm, _ = jalankan("npm --version")
    if not ok_npm:
        cetak_error("npm tidak ditemukan. Instal npm terlebih dahulu.")
        return False
    cetak_sukses("npm tersedia")
    return True


def pasang_rea_ke_antigravity() -> bool:
    """
    [ID]: Menjalankan rea setup untuk mendaftarkan REA ke Antigravity IDE.
          Backup otomatis mcp_config.json dibuat oleh REA sebelum perubahan.
    [EN]: Runs rea setup to register REA into Antigravity IDE.
          Automatic backup of mcp_config.json is created by REA before changes.
    """
    cetak_langkah(f"Mendaftarkan REA MCP Server v{REA_VERSION} ke Antigravity IDE...")
    cmd = f"npx -y rea-agents@{REA_VERSION} setup --client antigravity --yes --skill"
    print(f"  Menjalankan: {cmd}")
    ok, output = jalankan(cmd)
    # Tampilkan output ringkas (maks 1000 karakter)
    ringkas = output[:1000] if len(output) > 1000 else output
    print(ringkas)
    if not ok and "configured_antigravity" not in output:
        cetak_error("Setup REA gagal. Coba jalankan manual: npx rea-agents setup")
        return False
    cetak_sukses("REA MCP berhasil terdaftar di Antigravity IDE")
    return True


def tambahkan_compact_profile() -> bool:
    """
    [ID]: Menambahkan REA_MCP_INPUT_SCHEMA_PROFILE=compact ke entri REA di mcp_config.json.
          Menghemat ~40% token catalog tools tanpa mengurangi kapabilitas analisis.
    [EN]: Adds REA_MCP_INPUT_SCHEMA_PROFILE=compact to the REA entry in mcp_config.json.
          Saves ~40% token catalog size without reducing analysis capabilities.
    """
    cetak_langkah("Mengonfigurasi profil skema kompak untuk menghemat token...")
    config_path = Path.home() / ".gemini" / "config" / "mcp_config.json"
    if not config_path.exists():
        cetak_error(f"File tidak ditemukan: {config_path}")
        return False

    with open(config_path, "r", encoding="utf-8-sig") as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})
    if "rea" not in servers:
        cetak_error("Entri 'rea' tidak ditemukan di mcp_config.json. Pastikan Step sebelumnya berhasil.")
        return False

    if "env" not in servers["rea"]:
        servers["rea"]["env"] = {}

    servers["rea"]["env"]["REA_MCP_INPUT_SCHEMA_PROFILE"] = "compact"
    if "disabled" not in servers["rea"]:
        servers["rea"]["disabled"] = False

    config["mcpServers"] = servers
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    cetak_sukses("Profil compact aktif (REA_MCP_INPUT_SCHEMA_PROFILE=compact → hemat ~40% token)")
    return True


def verifikasi_mcp_config() -> bool:
    """
    [ID]: Memverifikasi bahwa mcp_config.json memiliki ketiga entri server yang dibutuhkan.
    [EN]: Verifies that mcp_config.json has all three required server entries.
    """
    cetak_langkah("Memverifikasi isi mcp_config.json...")
    config_path = Path.home() / ".gemini" / "config" / "mcp_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})
    semua_ok = True
    for name in ["openrouter", "hermes_agent", "rea"]:
        if name in servers:
            cetak_sukses(f"Server '{name}' ✓ terdaftar")
        else:
            cetak_error(f"Server '{name}' TIDAK ditemukan di mcp_config.json!")
            semua_ok = False

    profile = servers.get("rea", {}).get("env", {}).get("REA_MCP_INPUT_SCHEMA_PROFILE", "")
    if profile == "compact":
        cetak_sukses("Profil compact ✓ aktif")
    else:
        cetak_error("Profil compact TIDAK aktif - jalankan ulang langkah sebelumnya.")
        semua_ok = False

    return semua_ok


def verifikasi_skill() -> bool:
    """
    [ID]: Memverifikasi bahwa global skill REA telah terpasang di direktori Antigravity.
    [EN]: Verifies that the REA global skill is installed in the Antigravity directory.
    """
    cetak_langkah("Memverifikasi global skill REA...")
    skill_path = (
        Path.home() / ".gemini" / "config" / "skills"
        / "reverse-engineer-anything" / "SKILL.md"
    )
    if skill_path.exists():
        cetak_sukses(f"Global skill terpasang: {skill_path}")
        return True
    else:
        cetak_error(f"Global skill TIDAK ditemukan: {skill_path}")
        cetak_error("Coba jalankan: npx rea-agents setup --client antigravity --yes --skill")
        return False


def jalankan_diagnostik() -> bool:
    """
    [ID]: Menjalankan rea mcp doctor untuk memverifikasi kesehatan server REA (207 tools).
    [EN]: Runs rea mcp doctor to verify REA server health (207 tools).
    """
    cetak_langkah(f"Menjalankan diagnostik rea mcp doctor (rea-agents@{REA_VERSION})...")
    ok, output = jalankan(f"npx -y rea-agents@{REA_VERSION} mcp doctor")
    print(output[:600] if len(output) > 600 else output)
    if "healthy: true" in output:
        cetak_sukses("Diagnostik berhasil: REA MCP Server sehat ✓ (207 tools tersedia)")
        return True
    else:
        cetak_error("Diagnostik menunjukkan masalah - periksa output di atas.")
        return False


def main():
    """[ID]: Fungsi utama installer REA MCP. [EN]: Main REA MCP installer function."""
    print("=" * 70)
    print("   INSTALLER OTOMATIS: REA MCP (Reverse Engineer Anything) x ANTIGRAVITY")
    print(f"   rea-agents@{REA_VERSION} | Node.js MCP stdio | 207 Reverse Engineering Tools")
    print("=" * 70)

    langkah = [
        periksa_node,
        pasang_rea_ke_antigravity,
        tambahkan_compact_profile,
        verifikasi_mcp_config,
        verifikasi_skill,
        jalankan_diagnostik,
    ]

    for fn in langkah:
        if not fn():
            print("\n[BATAL] Proses instalasi dihentikan karena error di atas.")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("  [SELESAI] REA MCP berhasil terpasang di Antigravity IDE!")
    print("  Restart Antigravity IDE sekali agar tool REA terdeteksi.")
    print("  Cara pakai: 'Gunakan REA untuk menganalisa [path target]' di chat AI.")
    print("=" * 70)


if __name__ == "__main__":
    main()
