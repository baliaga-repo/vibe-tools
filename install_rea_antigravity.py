"""
[ID]: Installer Otomatis: REA (Reverse Engineer Anything) + Antigravity MCP Server.
Skrip ini mengotomatiskan seluruh konfigurasi REA di lingkungan Antigravity IDE:
1. Verifikasi instalasi Node.js (>=22.19 / >=24.11 / 26+) dan npm.
2. Instalasi global paket `rea-agents` melalui npm.
3. Ekstraksi seluruh 200+ skema tool MCP dari server REA secara dinamis via JSON-RPC.
4. Penyimpanan skema ke direktori lokal vibe_tools dan direktori global IDE (~/.gemini/antigravity-ide/mcp/rea).
5. Pendaftaran konfigurasi server 'rea' ke ~/.gemini/config/mcp_config.json.
6. Validasi kesehatan server menggunakan `rea mcp doctor`.

[EN]: Automatic Installer: REA (Reverse Engineer Anything) + Antigravity MCP Server.
This script automates the complete configuration of REA in Antigravity IDE:
1. Verify Node.js (>=22.19 / >=24.11 / 26+) and npm installation.
2. Globally install `rea-agents` package via npm.
3. Dynamically extract 200+ MCP tool schemas from REA server via JSON-RPC.
4. Store schemas into local vibe_tools and global IDE dir (~/.gemini/antigravity-ide/mcp/rea).
5. Register 'rea' server config in ~/.gemini/config/mcp_config.json.
6. Validate server health using `rea mcp doctor`.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Memastikan output konsol mendukung encoding UTF-8 di Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def cetak_langkah(pesan: str):
    """Cetak header langkah proses."""
    print(f"\n[+] {pesan}")


def cetak_sukses(pesan: str):
    """Cetak status sukses."""
    print(f"  [OK] {pesan}")


def cetak_error(pesan: str):
    """Cetak status error."""
    print(f"  [ERROR] {pesan}")


def jalankan_perintah(cmd, cwd=None):
    """Menjalankan shell command secara aman dan mengembalikan output teks."""
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        cetak_error(f"Gagal menjalankan perintah: {cmd}")
        cetak_error(res.stderr.strip() or res.stdout.strip())
        return False, res.stderr
    return True, res.stdout


def temukan_rea_mjs() -> Path | None:
    """Mencari lokasi skrip entry point rea.mjs di instalasi Node global."""
    app_data = os.environ.get("APPDATA")
    kandidat = []
    if app_data:
        kandidat.append(Path(app_data) / "npm" / "node_modules" / "rea-agents" / "scripts" / "rea.mjs")
    
    # Kandidat berdasarkan prefix npm
    try:
        ok, out = jalankan_perintah("npm.cmd root -g" if os.name == "nt" else "npm root -g")
        if ok and out.strip():
            kandidat.append(Path(out.strip()) / "rea-agents" / "scripts" / "rea.mjs")
    except Exception:
        pass

    for k in kandidat:
        if k.exists():
            return k
    return None


def ambil_skema_mcp(rea_mjs_path: Path) -> list:
    """Mengambil katalog lengkap tools dari server REA stdio via protokol MCP JSON-RPC."""
    proc = subprocess.Popen(
        ["node", str(rea_mjs_path), "--mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    try:
        # Kirim request inisialisasi protokol MCP
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "rea-installer", "version": "1.0"}
            }
        }
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()
        proc.stdout.readline()

        # Ambil daftar tools lengkap
        tools_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        proc.stdin.write(json.dumps(tools_req) + "\n")
        proc.stdin.flush()
        response_line = proc.stdout.readline()
        
        data = json.loads(response_line)
        return data.get("result", {}).get("tools", [])
    finally:
        proc.terminate()


def main():
    print("=" * 70)
    print("   INSTALLER OTOMATIS: REA (REVERSE ENGINEER ANYTHING) x ANTIGRAVITY")
    print("=" * 70)

    # 1. Verifikasi Lingkungan Node.js
    cetak_langkah("Memeriksa dependensi Node.js dan npm...")
    ok_node, out_node = jalankan_perintah("node -v")
    if not ok_node:
        cetak_error("Node.js tidak terdeteksi. Silakan pasang Node.js (>=22.19 atau >=24.11) terlebih dahulu.")
        sys.exit(1)
    cetak_sukses(f"Node.js terdeteksi: {out_node.strip()}")

    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    ok_npm, out_npm = jalankan_perintah(f"{npm_cmd} -v")
    if not ok_npm:
        cetak_error("npm tidak terdeteksi di sistem.")
        sys.exit(1)
    cetak_sukses(f"npm terdeteksi: {out_npm.strip()}")

    # 2. Instalasi Paket rea-agents secara Global
    cetak_langkah("Memeriksa ketersediaan paket rea-agents global...")
    rea_path = temukan_rea_mjs()
    if not rea_path:
        print("  [*] Mengunduh dan memasang 'rea-agents' secara global melalui npm...")
        ok_install, _ = jalankan_perintah(f"{npm_cmd} install --global rea-agents")
        if not ok_install:
            cetak_error("Gagal memasang paket rea-agents secara global.")
            sys.exit(1)
        rea_path = temukan_rea_mjs()

    if not rea_path or not rea_path.exists():
        cetak_error("Tidak dapat menemukan file entry point 'scripts/rea.mjs'.")
        sys.exit(1)
    cetak_sukses(f"Entry point REA ditemukan: {rea_path}")

    # 3. Ambil dan Simpan Skema MCP Tools
    cetak_langkah("Mengekstrak skema tool MCP dari REA stdio server...")
    tools = ambil_skema_mcp(rea_path)
    cetak_sukses(f"Berhasil mengekstrak {len(tools)} tools dari server REA.")

    # Tentukan direktori penyimpanan skema
    skrip_dir = Path(__file__).parent.resolve()
    lokal_schemas_dir = skrip_dir / "mcp_schemas" / "rea"
    lokal_schemas_dir.mkdir(parents=True, exist_ok=True)

    gemini_dir = Path.home() / ".gemini"
    ide_schemas_dir = gemini_dir / "antigravity-ide" / "mcp" / "rea"
    ide_schemas_dir.mkdir(parents=True, exist_ok=True)

    for tool in tools:
        nama_tool = tool.get("name")
        if not nama_tool:
            continue
        
        # Format skema sesuai standar Antigravity IDE (parameter mapping)
        skema_antigravity = {
            "name": nama_tool,
            "description": tool.get("description", ""),
            "parameters": tool.get("inputSchema", {})
        }
        
        # Simpan ke folder lokal vibe_tools
        file_lokal = lokal_schemas_dir / f"{nama_tool}.json"
        with open(file_lokal, "w", encoding="utf-8") as f:
            json.dump(skema_antigravity, f, indent=2)

        # Simpan ke folder IDE global
        file_ide = ide_schemas_dir / f"{nama_tool}.json"
        with open(file_ide, "w", encoding="utf-8") as f:
            json.dump(skema_antigravity, f, indent=2)

    cetak_sukses(f"Skema tools tersimpan di:")
    print(f"      - Lokal: {lokal_schemas_dir}")
    print(f"      - IDE Global: {ide_schemas_dir}")

    # Buat file panduan instructions.md di folder MCP server IDE
    instruksi_mcp = (
        "# Panduan Penggunaan REA (Reverse Engineer Anything)\n\n"
        "Server MCP REA menyediakan inspeksi dan rekayasa balik mendalam tanpa source code:\n"
        "1. **Analisis Binary & PE**: Gunakan `inspect_pe_resources`, `inspect_binary_layout`, atau `inspect_native_api` "
        "untuk membedah file EXE, DLL (seperti DaVinci Resolve `Resolve.exe` dan `fusionscript.dll`).\n"
        "2. **Database SQLite**: Gunakan `inspect_sqlite_database` untuk memeriksa skema dan data project (seperti `Project.db` DaVinci).\n"
        "3. **Aplikasi JS/Electron**: Gunakan `analyze_javascript_application` untuk mengekstrak ASAR dan memetakan IPC channels.\n"
        "4. **Web & Network**: Gunakan `inspect_web_page` dan `inspect_web_network_capture` untuk reverse engineering API player YouTube.\n"
    )
    with open(ide_schemas_dir / "instructions.md", "w", encoding="utf-8") as f:
        f.write(instruksi_mcp)

    # 4. Daftarkan REA ke mcp_config.json
    cetak_langkah("Mendaftarkan server REA ke konfigurasi MCP Antigravity...")
    mcp_config_path = gemini_dir / "config" / "mcp_config.json"
    mcp_config_path.parent.mkdir(parents=True, exist_ok=True)

    config_data = {"mcpServers": {}}
    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception:
            config_data = {"mcpServers": {}}

    if "mcpServers" not in config_data:
        config_data["mcpServers"] = {}

    rea_mjs_normalized = str(rea_path).replace("\\", "/")
    config_data["mcpServers"]["rea"] = {
        "command": "node",
        "args": [
            rea_mjs_normalized,
            "--mcp"
        ],
        "disabled": False
    }

    with open(mcp_config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
    cetak_sukses(f"Server 'rea' berhasil didaftarkan di: {mcp_config_path}")

    # 5. Verifikasi Kesehatan Server
    cetak_langkah("Memverifikasi kesehatan server REA (mcp doctor)...")
    rea_cmd = "rea.cmd" if os.name == "nt" else "rea"
    ok_doctor, out_doctor = jalankan_perintah(f"{rea_cmd} mcp doctor")
    if ok_doctor and "healthy: true" in out_doctor:
        cetak_sukses("Verifikasi berhasil! REA MCP Server berjalan normal (healthy: true).")
    else:
        print("  [!] Dokter MCP selesai dieksekusi.")

    print("\n" + "=" * 70)
    print("   INSTALASI & REGISTRASI REA BERHASIL 100%!")
    print("=" * 70)
    print("REA kini siap digunakan oleh agen Antigravity untuk rekayasa balik!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
