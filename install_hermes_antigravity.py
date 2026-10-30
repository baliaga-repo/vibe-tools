"""[ID]: Installer Otomatis: Hermes Agent + Antigravity MCP Worker Bridge.
Mengotomatiskan clone Hermes Agent, instalasi CLI, pengaturan OpenRouter API,
dan penyalinan bridge hermes_mcp.py ke ~/.gemini/ secara ringkas.

[EN]: Automatic Installer: Hermes Agent + Antigravity MCP Worker Bridge.
Automates cloning Hermes Agent, CLI installation, OpenRouter API setup,
and copying hermes_mcp.py bridge to ~/.gemini/ concisely.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Pastikan UTF-8 di Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def print_step(msg: str):
    print(f"\n[+] {msg}")


def print_ok(msg: str):
    print(f"  [OK] {msg}")


def print_err(msg: str):
    print(f"  [ERROR] {msg}")


def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print_err(f"Gagal: {cmd}")
        print_err(res.stderr.strip() or res.stdout.strip())
        return False, res.stderr
    return True, res.stdout


def main():
    print("=" * 70)
    print("   INSTALLER OTOMATIS: HERMES AGENT x ANTIGRAVITY IDE")
    print("=" * 70)

    user_home = Path.home()
    local_app_data = Path(os.environ.get("LOCALAPPDATA", user_home / "AppData" / "Local"))
    gemini_dir = user_home / ".gemini"
    gemini_config_dir = gemini_dir / "config"
    default_install_dir = Path("C:/hermes_env")

    # 1. Tentukan Direktori Instalasi
    print_step("Memeriksa direktori instalasi Hermes Agent...")
    inp = input(f"Tentukan folder instalasi [default: {default_install_dir}]: ").strip()
    target_base = Path(inp) if inp else default_install_dir
    target_repo_dir = target_base / "hermes-agent"
    target_base.mkdir(parents=True, exist_ok=True)
    print_ok(f"Target folder: {target_repo_dir}")

    # 2. Clone atau Update Hermes Agent
    print_step("Mengunduh / memperbarui repositori Hermes Agent dari GitHub...")
    if not target_repo_dir.exists():
        ok, _ = run_cmd(f'git clone https://github.com/NousResearch/hermes-agent.git "{target_repo_dir}"')
        if not ok:
            print_err("Gagal clone repositori Hermes Agent.")
            return
        print_ok("Clone repositori selesai.")
    else:
        run_cmd("git pull origin main", cwd=str(target_repo_dir))
        print_ok("Repositori lokal sudah ada dan diperbarui.")

    # 3. Install Dependensi & CLI Hermes
    print_step("Menginstal paket dan dependensi Hermes Agent...")
    pip_cmd = (
        f'"{sys.executable}" -m pip install -q -e "{target_repo_dir}"'
    )
    ok_pip, _ = run_cmd(pip_cmd)
    if not ok_pip:
        print_err("Gagal menginstal paket hermes-agent.")
        return

    # Dependensi esensial untuk Python < 3.14
    dep_list = "ruamel.yaml psutil rich tomli-w fire tenacity jinja2 markdown tzdata prompt_toolkit croniter pathspec snowballstemmer mcp"
    run_cmd(f'"{sys.executable}" -m pip install -q {dep_list}')
    print_ok("Seluruh dependensi Python terpasang.")

    # 4. Konfigurasi OpenRouter API Key
    print_step("Konfigurasi kredensial OpenRouter untuk Hermes...")
    hermes_env_dir = local_app_data / "hermes"
    hermes_env_dir.mkdir(parents=True, exist_ok=True)
    hermes_env_file = hermes_env_dir / ".env"

    existing_key = ""
    openrouter_key_file = gemini_dir / "openrouter_key.txt"
    if openrouter_key_file.exists():
        existing_key = openrouter_key_file.read_text(encoding="utf-8").strip()

    if not existing_key or existing_key == "TEMPEL_API_KEY_DISINI":
        existing_key = input("Masukkan OpenRouter API Key (sk-or-v1-...) [Enter untuk isi nanti]: ").strip()

    if existing_key and existing_key != "TEMPEL_API_KEY_DISINI":
        hermes_env_file.write_text(f"OPENROUTER_API_KEY={existing_key}\n", encoding="utf-8")
        print_ok(f"API Key disimpan ke: {hermes_env_file}")

    # Atur model default
    hermes_exe = shutil.which("hermes") or str(Path(sys.executable).parent / "Scripts" / "hermes.exe")
    run_cmd(f'"{hermes_exe}" config set model "deepseek/deepseek-chat"')
    print_ok("Model default Hermes diatur ke: deepseek/deepseek-chat")

    # 5. Salin hermes_mcp.py ke ~/.gemini
    print_step("Memasang skrip bridge hermes_mcp.py...")
    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_config_dir.mkdir(parents=True, exist_ok=True)
    hermes_mcp_dest = gemini_dir / "hermes_mcp.py"
    src_bridge = Path(__file__).resolve().parent / "hermes_mcp.py"

    if src_bridge.exists():
        shutil.copy2(src_bridge, hermes_mcp_dest)
        print_ok(f"Bridge script disalin dari: {src_bridge} -> {hermes_mcp_dest}")
    else:
        print_err(f"Berkas sumber {src_bridge} tidak ditemukan.")
        return

    # 6. Daftarkan ke mcp_config.json
    print_step("Mendaftarkan server hermes_agent ke mcp_config.json Antigravity...")
    mcp_config_path = gemini_config_dir / "mcp_config.json"
    config_data = {"mcpServers": {}}
    if mcp_config_path.exists():
        try:
            config_data = json.loads(mcp_config_path.read_text(encoding="utf-8"))
        except Exception:
            config_data = {"mcpServers": {}}

    if "mcpServers" not in config_data:
        config_data["mcpServers"] = {}

    python_exe = sys.executable.replace("\\", "/")
    config_data["mcpServers"]["hermes_agent"] = {
        "command": python_exe,
        "args": [str(hermes_mcp_dest).replace("\\", "/")],
        "disabled": False
    }

    mcp_config_path.write_text(json.dumps(config_data, indent=2), encoding="utf-8")
    print_ok(f"Server hermes_agent terdaftar di: {mcp_config_path}")

    print("\n" + "=" * 70)
    print("   [SELESAI] HERMES AGENT BERHASIL DIPASANG!")
    print("=" * 70)
    print("Restart Antigravity IDE Anda untuk memuat MCP server baru.")


if __name__ == "__main__":
    main()
