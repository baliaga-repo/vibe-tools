"""
[ID]: Installer Otomatis: OpenRouter MCP Server untuk Antigravity IDE.
Skrip ini mengotomatiskan seluruh proses instalasi di PC/laptop baru:
1. Membuat folder ~/.gemini dan ~/.gemini/config/.
2. Menginstal pustaka python yang dibutuhkan (mcp, requests).
3. Memasang berkas server openrouter_mcp.py ke ~/.gemini/.
4. Mengonfigurasi openrouter_key.txt untuk menyimpan API Key.
5. Menambahkan konfigurasi server 'openrouter' ke ~/.gemini/config/mcp_config.json.
6. Memverifikasi kelayakan sintaks server MCP.

[EN]: Automatic Installer: OpenRouter MCP Server for Antigravity IDE.
This script automates the entire installation process on a new PC/laptop:
1. Creates the ~/.gemini and ~/.gemini/config/ directories.
2. Installs required Python libraries (mcp, requests).
3. Places the openrouter_mcp.py server file into ~/.gemini/.
4. Configures openrouter_key.txt to store the API Key.
5. Adds the 'openrouter' server configuration to ~/.gemini/config/mcp_config.json.
6. Verifies the MCP server syntax validity.
"""

import json
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


KONTEN_OPENROUTER_MCP = r'''"""
Server MCP OpenRouter untuk Antigravity IDE.
Menyediakan integrasi langsung ke berbagai model AI unggulan melalui OpenRouter API
dengan sistem alias cerdas (r1, claude, sonnet, deepseek, v3, gpt4o, qwen, free, dll).
"""

import os
import sys
from pathlib import Path
import requests

# Konfigurasi encoding UTF-8 agar kompatibel dengan terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Inisialisasi server FastMCP / MCPServer (kompatibel mcp 1.x dan 2.x)
try:
    from mcp.server.mcpserver import MCPServer
    mcp = MCPServer("openrouter")
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("openrouter")
    except Exception as err:
        raise RuntimeError(f"Gagal memuat modul MCP: {err}")

# Pemetaan alias cerdas ke model ID resmi OpenRouter
MODEL_ALIASES = {
    # Penalaran Mendalam & Khusus (Reasoning)
    "r1": "deepseek/deepseek-r1",
    "deepseek-r1": "deepseek/deepseek-r1",
    "o3-mini": "openai/o3-mini",
    
    # Standar Emas Coding & Refactoring
    "claude": "anthropic/claude-3.7-sonnet:thinking",
    "claude-thinking": "anthropic/claude-3.7-sonnet:thinking",
    "claude-3.7": "anthropic/claude-3.7-sonnet",
    "claude-3.7-thinking": "anthropic/claude-3.7-sonnet:thinking",
    "claude-4.5": "anthropic/claude-sonnet-4.5",
    "sonnet": "anthropic/claude-3.7-sonnet:thinking",
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "claude-haiku": "anthropic/claude-3.5-haiku",
    "haiku": "anthropic/claude-3.5-haiku",
    
    # Model Google Long-Context
    "gemini": "google/gemini-2.5-flash",
    "gemini-flash": "google/gemini-2.5-flash",
    "gemini-pro": "google/gemini-2.5-pro",
    
    # Spesialis Coding Cepat & Hemat
    "qwen": "qwen/qwen-2.5-coder-32b-instruct",
    "qwen-coder": "qwen/qwen-2.5-coder-32b-instruct",
    
    # Harian Gesit & Super Hemat
    "deepseek": "deepseek/deepseek-chat",
    "v3": "deepseek/deepseek-chat",
    "deepseek-v3": "deepseek/deepseek-chat",
    
    # OpenAI Multifungsi
    "gpt4o": "openai/gpt-4o",
    "4o": "openai/gpt-4o",
    "gpt-4o": "openai/gpt-4o",
    "gpt4o-mini": "openai/gpt-4o-mini",
    "4o-mini": "openai/gpt-4o-mini",
    
    # Model 100% Gratis (Free Tier Aktif)
    "free": "google/gemma-4-31b-it:free",
    "gemma-free": "google/gemma-4-31b-it:free",
    "code-free": "cohere/north-mini-code:free",
    "deepseek-free": "deepseek/deepseek-chat",
}


def get_api_key() -> str:
    """Mengambil OpenRouter API Key dari env var atau ~/.gemini/openrouter_key.txt."""
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_key and env_key != "TEMPEL_API_KEY_DISINI":
        return env_key

    key_file = Path.home() / ".gemini" / "openrouter_key.txt"
    if key_file.exists():
        try:
            for line in key_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and line != "TEMPEL_API_KEY_DISINI":
                    return line
        except Exception:
            pass

    return ""


def resolve_model_id(alias_or_id: str) -> str:
    """Menerjemahkan alias pendek ke model ID lengkap OpenRouter."""
    if not alias_or_id:
        return "deepseek/deepseek-chat"
    alias_clean = alias_or_id.strip().lower()
    return MODEL_ALIASES.get(alias_clean, alias_or_id.strip())


DAILY_LIMIT_USD = float(os.environ.get("OPENROUTER_DAILY_LIMIT", "1.00"))


def check_daily_limit_exceeded(api_key: str) -> tuple[bool, float]:
    """Mengecek apakah penggunaan hari ini telah melebihi batas limit harian."""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        res = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=5)
        if res.status_code == 200:
            auth_data = res.json().get("data", {})
            daily_usage = float(auth_data.get("usage_daily", 0.0) or 0.0)
            if daily_usage >= DAILY_LIMIT_USD:
                return True, daily_usage
            return False, daily_usage
    except Exception:
        pass
    return False, 0.0


@mcp.tool()
def tanya_openrouter(prompt: str, model: str = "deepseek", system_prompt: str = "") -> str:
    """
    Mengirim pertanyaan atau tugas ke berbagai model AI melalui OpenRouter API.
    Mendukung alias cerdas seperti 'r1', 'claude', 'sonnet', 'deepseek', 'v3', 'gpt4o', 'qwen', 'free', dsb.
    Dilengkapi pengaman batas pengeluaran harian $1/hari.
    """
    api_key = get_api_key()
    if not api_key:
        return (
            "❌ Error: API Key OpenRouter belum dikonfigurasi.\n"
            "Silakan tempelkan API Key Anda ke berkas:\n"
            f"   {Path.home() / '.gemini' / 'openrouter_key.txt'}\n"
            "Atau tentukan variabel lingkungan OPENROUTER_API_KEY di mcp_config.json."
        )

    is_exceeded, daily_spend = check_daily_limit_exceeded(api_key)
    if is_exceeded:
        return (
            f"🛑 **Batas Pengeluaran Harian Tercapai!**\n\n"
            f"- Penggunaan Hari Ini: **${daily_spend:.4f}**\n"
            f"- Batas Limit Maksimal: **${DAILY_LIMIT_USD:.2f} per hari**\n\n"
            "Permintaan ditahan secara otomatis untuk mencegah pengeluaran melebihi limit harian.\n"
            "Batas akan direset kembali besok oleh OpenRouter, atau Anda dapat menyesuaikan OPENROUTER_DAILY_LIMIT."
        )

    model_id = resolve_model_id(model)
    endpoint = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/google/antigravity",
        "X-Title": "Antigravity OpenRouter MCP",
    }

    messages = []
    if system_prompt and system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_id,
        "messages": messages,
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=90)
        
        if response.status_code == 200:
            res_json = response.json()
            choices = res_json.get("choices", [])
            if choices and "message" in choices[0]:
                content = choices[0]["message"].get("content", "")
                usage = res_json.get("usage", {})
                tokens_info = ""
                if usage:
                    prompt_tokens = usage.get("prompt_tokens", 0)
                    completion_tokens = usage.get("completion_tokens", 0)
                    total_tokens = usage.get("total_tokens", 0)
                    tokens_info = f"\n\n*(Model: {model_id} | Token: {prompt_tokens} in / {completion_tokens} out / {total_tokens} total)*"
                return content + tokens_info
            return "⚠️ Respons dari OpenRouter tidak memiliki pesan teks yang valid."
        else:
            try:
                err_detail = response.json().get("error", {}).get("message", response.text)
            except Exception:
                err_detail = response.text
            return f"❌ Error OpenRouter API (Status {response.status_code}): {err_detail}"

    except requests.exceptions.Timeout:
        return "❌ Request timeout: Model membutuhkan waktu terlalu lama untuk merespons (lebih dari 90 detik)."
    except requests.exceptions.RequestException as e:
        return f"❌ Terjadi kesalahan jaringan saat menghubungi OpenRouter: {str(e)}"


@mcp.tool()
def daftar_model_rekomendasi() -> str:
    """Menampilkan katalog model AI unggulan dan alias pendek yang didukung."""
    return """### 🏆 Katalog Model AI Pilihan OpenRouter

| Kategori | Alias Cerdas | Model ID Resmi | Rekomendasi Kasus |
| :--- | :---: | :--- | :--- |
| 🧠 **Penalaran Super** | `r1` | `deepseek/deepseek-r1` | Logika rumit, matematika, debugging |
| 🧠 **Penalaran Cepat** | `o3-mini` | `openai/o3-mini` | Penalaran logis ala OpenAI |
| 💻 **Standar Coding** | `claude` / `sonnet` | `anthropic/claude-3.5-sonnet` | Refactoring arsitektur, modularitas |
| 💻 **Kode Ringan & Hemat** | `qwen` | `qwen/qwen-2.5-coder-32b-instruct` | Python, JS, HTML super hemat |
| ⚡ **Harian Gesit** | `deepseek` / `v3` | `deepseek/deepseek-chat` | Rekomendasi harian: cepat & cerdas |
| ⚡ **Multifungsi Cepat** | `gpt4o` / `4o` | `openai/gpt-4o` | Ringkasan, instruksi umum |
| 🎁 **100% GRATIS** | `free` | `meta-llama/llama-3.3-70b-instruct:free` | Eksperimen bebas biaya |
| 🎁 **100% GRATIS (R1)** | `deepseek-free` | `deepseek/deepseek-r1:free` | DeepSeek R1 antrean publik gratis |
"""


@mcp.tool()
def cek_koneksi_openrouter() -> str:
    """Mengecek validitas API Key OpenRouter serta status saldo dan kuota akun."""
    api_key = get_api_key()
    if not api_key:
        return f"⚠️ API Key OpenRouter belum ditemukan di {Path.home() / '.gemini' / 'openrouter_key.txt'}."

    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        auth_res = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=15)
        if auth_res.status_code != 200:
            return f"❌ Validasi API Key Gagal: {auth_res.text}"

        auth_data = auth_res.json().get("data", {})
        label = auth_data.get("label", "Tanpa Label")
        usage_total = auth_data.get("usage", 0.0)
        usage_daily = auth_data.get("usage_daily", 0.0) or 0.0
        
        credit_info = ""
        try:
            credits_res = requests.get("https://openrouter.ai/api/v1/credits", headers=headers, timeout=15)
            if credits_res.status_code == 200:
                credit_data = credits_res.json().get("data", {})
                rem = max(0.0, credit_data.get("total_credits", 0.0) - credit_data.get("total_usage", 0.0))
                credit_info = f"- Sisa Saldo Tersedia: ${rem:.4f}\n"
        except Exception:
            pass

        return (
            "✅ **Koneksi OpenRouter Berhasil!**\n\n"
            f"- **Label Kunci:** {label}\n"
            f"- **Total Pemakaian Kunci:** ${usage_total:.4f}\n"
            f"- **Pemakaian Hari Ini:** ${usage_daily:.4f} / Limit ${DAILY_LIMIT_USD:.2f}\n"
            f"{credit_info}"
            "- Server MCP OpenRouter siap digunakan!"
        )
    except requests.exceptions.RequestException as e:
        return f"❌ Gagal terhubung ke OpenRouter API: {str(e)}"


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Server MCP OpenRouter untuk Antigravity IDE")
        sys.exit(0)
    mcp.run()
'''


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

    # 2. Instal pustaka pendukung
    cetak_langkah("2. Menginstal pustaka Python yang dibutuhkan (mcp, requests)...")
    ok, _ = jalankan(f'"{sys.executable}" -m pip install -q mcp requests')
    if ok:
        cetak_sukses("Pustaka mcp & requests berhasil terpasang.")
    else:
        cetak_error("Gagal menginstal dependensi. Cek koneksi internet Anda.")

    # 3. Tulis skrip openrouter_mcp.py ke ~/.gemini
    cetak_langkah("3. Memasang server bridge openrouter_mcp.py...")
    server_script.write_text(KONTEN_OPENROUTER_MCP.strip() + "\n", encoding="utf-8")
    cetak_sukses(f"Skrip server terpasang: {server_script}")

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
