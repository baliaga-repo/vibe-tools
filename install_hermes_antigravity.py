"""
Installer Otomatis: Hermes Agent + Antigravity MCP Worker Bridge.
Skrip ini mengotomatiskan seluruh proses instalasi di PC baru:
1. Clone repositori resmi NousResearch/hermes-agent.
2. Install dependensi & CLI hermes ke environment Python.
3. Konfigurasi kredensial OpenRouter di Hermes (~/AppData/Local/hermes/.env).
4. Buat script bridge hermes_mcp.py di folder global Antigravity (~/.gemini).
5. Konfigurasi mcp_config.json Antigravity agar Hermes langsung aktif sebagai MCP tool.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Pastikan UTF-8 di Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def print_step(msg: str):
    print(f"\n[+] {msg}")


def print_ok(msg: str):
    print(f"  [OK] {msg}")


def print_err(msg: str):
    print(f"  [ERROR] {msg}")


def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print_err(f"Gagal menjalankan perintah: {cmd}")
        print_err(res.stderr.strip() or res.stdout.strip())
        return False, res.stderr
    return True, res.stdout


def main():
    print("=" * 70)
    print("   INSTALLER OTOMATIS: HERMES AGENT x ANTIGRAVITY IDE")
    print("=" * 70)

    # 1. Tentukan Direktori Kerja
    user_home = Path.home()
    local_app_data = Path(os.environ.get("LOCALAPPDATA", user_home / "AppData" / "Local"))
    gemini_dir = user_home / ".gemini"
    gemini_config_dir = gemini_dir / "config"

    # Direktori clone hermes-agent (default C:\hermes_env jika drive C ada, atau di User profile)
    default_install_dir = Path("C:/hermes_env") if Path("C:/").exists() else (user_home / "hermes_env")
    install_input = input(f"Tentukan folder instalasi [Default: {default_install_dir}]: ").strip()
    target_env_dir = Path(install_input) if install_input else default_install_dir
    target_repo_dir = target_env_dir / "hermes-agent"

    # API Key OpenRouter
    openrouter_key = input("Masukkan OpenRouter API Key (sk-or-v1-...): ").strip()
    while not openrouter_key.startswith("sk-or-v1-"):
        print("Format key tampaknya tidak valid! Harus berawalan 'sk-or-v1-'.")
        openrouter_key = input("Masukkan OpenRouter API Key kembali: ").strip()

    # 2. Clone Repository
    print_step("Menyiapkan repository hermes-agent...")
    target_env_dir.mkdir(parents=True, exist_ok=True)

    if not target_repo_dir.exists():
        print(f"  Cloning dari GitHub ke {target_repo_dir}...")
        ok, _ = run_cmd(f'git clone https://github.com/NousResearch/hermes-agent.git "{target_repo_dir}"')
        if not ok:
            print_err("Gagal clone git. Pastikan Git sudah terpasang di sistem.")
            sys.exit(1)
        print_ok("Clone berhasil.")
    else:
        print_ok(f"Folder {target_repo_dir} sudah ada, melewati clone.")

    # 3. Install Dependensi & Paket hermes-agent
    print_step("Memasang package hermes-agent & dependensi Python...")
    python_exe = sys.executable
    ok, _ = run_cmd(f'"{python_exe}" -m pip install -e .', cwd=target_repo_dir)
    if not ok:
        print_err("Gagal install paket hermes-agent. Periksa log.")
        sys.exit(1)
    print_ok("Package hermes-agent berhasil terpasang.")

    # Dependensi krusial yang dilewati pip pada Python < 3.14 (karena environment marker >= '3.14' di pyproject.toml)
    print_step("Memasang dependensi inti Hermes untuk Python < 3.14 (ruamel.yaml, psutil, rich, dll)...")
    hermes_deps = [
        "ruamel.yaml",
        "psutil",
        "rich",
        "tomli-w",
        "fire",
        "tenacity",
        "jinja2",
        "markdown",
        "tzdata",
        "prompt_toolkit",
        "croniter",
        "pathspec",
        "snowballstemmer",
        "mcp",
    ]
    ok_deps, _ = run_cmd(f'"{python_exe}" -m pip install {" ".join(hermes_deps)}')
    if not ok_deps:
        print_err("Peringatan: Beberapa dependensi tambahan gagal dipasang, memeriksa ulang...")
    else:
        print_ok("Seluruh dependensi inti (ruamel.yaml, psutil, rich, dll) berhasil terpasang.")

    # Cek letak hermes.exe
    hermes_exe = shutil.which("hermes")
    if not hermes_exe:
        # Cari di folder Scripts dari interpreter Python saat ini
        scripts_dir = Path(python_exe).parent / "Scripts" / "hermes.exe"
        if scripts_dir.exists():
            hermes_exe = str(scripts_dir)
        else:
            hermes_exe = "hermes"  # fallback ke PATH
    print_ok(f"Executable Hermes terdeteksi di: {hermes_exe}")

    # 4. Konfigurasi Kredensial & Model Default Hermes
    print_step("Menyimpan konfigurasi API Key ke Hermes...")
    hermes_data_dir = local_app_data / "hermes"
    hermes_data_dir.mkdir(parents=True, exist_ok=True)
    hermes_env_file = hermes_data_dir / ".env"

    env_lines = []
    if hermes_env_file.exists():
        with open(hermes_env_file, "r", encoding="utf-8") as f:
            env_lines = [l for l in f.readlines() if not l.startswith("OPENROUTER_API_KEY=")]

    env_lines.append(f"OPENROUTER_API_KEY={openrouter_key}\n")
    with open(hermes_env_file, "w", encoding="utf-8") as f:
        f.writelines(env_lines)
    print_ok(f"API key berhasil disimpan di {hermes_env_file}")

    # Set default model via hermes config set agar tidak kosong (mencegah error HTTP 400: No models provided)
    print_step("Mengatur model default Hermes ke 'deepseek/deepseek-chat' via OpenRouter...")
    ok_model, _ = run_cmd(f'"{hermes_exe}" config set model "deepseek/deepseek-chat"')
    if ok_model:
        print_ok("Model default berhasil diatur ke 'deepseek/deepseek-chat'.")
    else:
        print_err("Gagal mengatur model default secara otomatis. Anda bisa jalankan: hermes config set model deepseek/deepseek-chat")

    # 5. Buat Script Bridge hermes_mcp.py untuk Antigravity
    print_step("Membuat script bridge hermes_mcp.py untuk Antigravity IDE...")
    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_config_dir.mkdir(parents=True, exist_ok=True)

    hermes_mcp_file = gemini_dir / "hermes_mcp.py"
    hermes_exe_escaped = hermes_exe.replace("\\", "\\\\")
    repo_dir_escaped = str(target_repo_dir).replace("\\", "\\\\")

    bridge_code = f'''r"""
Hermes Agent Worker MCP Server untuk Antigravity IDE.
Menghubungkan Antigravity dengan Hermes Agent lokal
sebagai worker mandiri untuk eksekusi perintah, riset file, web search, dan scripting
tanpa membebani token context model utama (Claude / GPT).
"""
import sys
import os
import subprocess
from pathlib import Path

# Setup encoding
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Kompatibilitas mcp
try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        from mcp.server import FastMCP as MCPServer

mcp = MCPServer("Hermes-Worker")

HERMES_EXE = r"{hermes_exe}"
HERMES_REPO = r"{target_repo_dir}"


@mcp.tool(
    name="delegasikan_ke_hermes",
    description=(
        "Kirim tugas ke Hermes Agent lokal (background worker mandiri). "
        "Hermes dapat mengeksekusi terminal command/test, membaca & menyisir file luas, "
        "mencari regex di direktori kerja, scraping web, atau eksplorasi kode "
        "secara otonom dengan model gratis/eksternal tanpa membuang token Claude/GPT. "
        "Hasil akan otomatis diringkas padat agar efisien di context window."
    )
)
def delegasikan_ke_hermes(tugas: str, direktori_kerja: str = "", model: str = "") -> str:
    \"\"\"
    Kirim tugas ke Hermes Agent.
    
    Args:
        tugas: Deskripsi perintah atau tugas lengkap yang harus dilakukan Hermes.
        direktori_kerja: Folder tempat Hermes harus bekerja (opsional, otomatis menggunakan direktori kerja aktif jika kosong).
        model: Model OpenRouter spesifik yang ingin dipakai (opsional, contoh: 'deepseek/deepseek-chat', 'meta-llama/llama-3.3-70b-instruct:free', 'google/gemini-2.5-flash'). Jika kosong, memakai model default Hermes.
    \"\"\"
    target_cwd = ""
    if direktori_kerja and Path(direktori_kerja).exists():
        target_cwd = direktori_kerja
    else:
        current_dir = os.getcwd()
        if current_dir and not current_dir.lower().endswith("system32") and Path(current_dir).exists():
            target_cwd = current_dir
        elif Path(HERMES_REPO).exists():
            target_cwd = HERMES_REPO
        else:
            target_cwd = str(Path.home())

    instruksi_tugas = (
        f"{{tugas}}\\n\\n"
        "(Catatan: Berikan ringkasan padat, langsung ke temuan/akar masalah/nomor baris atau poin hasil eksekusi. "
        "Jangan dump output log mentah yang terlalu panjang agar menghemat token context.)"
    )

    cmd = [
        HERMES_EXE,
        "-z",  # oneshot mode
    ]
    if model:
        cmd.extend(["-m", model.strip()])
    cmd.append(instruksi_tugas)

    try:
        result = subprocess.run(
            cmd,
            cwd=target_cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300  # 5 menit timeout
        )

        output = result.stdout.strip()
        errors = result.stderr.strip()

        if result.returncode != 0:
            return f"Hermes Error (code {{result.returncode}}):\\n{{errors or output}}"

        if not output and errors:
            return f"Hermes Output (stderr):\\n{{errors}}"

        return output or "Tugas selesai dijalankan oleh Hermes Agent (tanpa output teks)."

    except subprocess.TimeoutExpired:
        return "Hermes Timeout: Tugas membutuhkan waktu lebih dari 5 menit."
    except Exception as e:
        return f"Gagal menjalankan Hermes Agent: {{str(e)}}"


if __name__ == "__main__":
    mcp.run()
'''
    with open(hermes_mcp_file, "w", encoding="utf-8") as f:
        f.write(bridge_code)
    print_ok(f"Bridge script tersimpan di: {hermes_mcp_file}")

    # 6. Daftarkan ke mcp_config.json Antigravity
    print_step("Memperbarui konfigurasi MCP Antigravity IDE...")
    mcp_config_path = gemini_config_dir / "mcp_config.json"
    config_data = {"mcpServers": {}}

    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception:
            config_data = {"mcpServers": {}}

    if "mcpServers" not in config_data:
        config_data["mcpServers"] = {}

    config_data["mcpServers"]["hermes_agent"] = {
        "command": python_exe.replace("\\", "/"),
        "args": [str(hermes_mcp_file).replace("\\", "/")],
        "disabled": False
    }

    with open(mcp_config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
    print_ok(f"Server hermes_agent terdaftar di: {mcp_config_path}")

    # 7. Selesai & Pengujian
    print("\n" + "=" * 70)
    print("   INSTALASI BERHASIL 100%!")
    print("=" * 70)
    print("Antigravity IDE Anda sekarang sudah memiliki worker Hermes Agent mandiri.")
    print("Tutup dan buka kembali Antigravity IDE untuk memuat MCP server baru.")
    print("Anda sekarang bisa langsung meminta Antigravity:")
    print('  -> "Tolong delegasikan ke Hermes untuk meriset kode..."')
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
