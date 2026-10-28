"""
[ID]: Server MCP OpenRouter untuk Antigravity IDE.
Menyediakan integrasi langsung ke berbagai model AI unggulan melalui OpenRouter API
dengan sistem alias cerdas (r1, claude, sonnet, deepseek, v3, gpt4o, qwen, free, dll).

[EN]: MCP OpenRouter server for Antigravity IDE.
Provides direct integration with leading AI models through OpenRouter API
using a smart alias system (r1, claude, sonnet, deepseek, v3, gpt4o, qwen, free, etc.).
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
    "r1": "deepseek/deepseek-r1-0528",
    "deepseek-r1": "deepseek/deepseek-r1-0528",
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
    """
[ID]: Mengambil OpenRouter API Key dari variabel lingkungan atau berkas openrouter_key.txt.
    Mendukung fallback otomatis jika salah satu belum terisi.

[EN]: Retrieves the OpenRouter API key from the environment variable or the openrouter_key.txt file.
Supports automatic fallback if either is not set.
"""
    # 1. Cek dari Environment Variable
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_key and env_key != "TEMPEL_API_KEY_DISINI":
        return env_key

    # 2. Cek dari berkas ~/.gemini/openrouter_key.txt
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
    """
[ID]: Menerjemahkan alias pendek ke model ID lengkap OpenRouter.
    Jika bukan alias terdaftar, gunakan string model asli apa adanya.

[EN]: Translates short aliases to full OpenRouter model IDs.
If not a registered alias, uses the original model string as-is.
"""
    if not alias_or_id:
        return "deepseek/deepseek-chat"
    alias_clean = alias_or_id.strip().lower()
    return MODEL_ALIASES.get(alias_clean, alias_or_id.strip())


# Batas limit harian dalam USD (default: $1.00)
DAILY_LIMIT_USD = float(os.environ.get("OPENROUTER_DAILY_LIMIT", "1.00"))


def check_daily_limit_exceeded(api_key: str) -> tuple[bool, float]:
    """
[ID]: Mengecek apakah penggunaan hari ini (usage_daily) telah melebihi batas limit harian.
    Mengembalikan (is_exceeded, current_daily_usage).

[EN]: Checks if today's usage (usage_daily) has exceeded the daily limit.
Returns (is_exceeded, current_daily_usage).
"""
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
[ID]: Mengirim pertanyaan atau tugas ke berbagai model AI melalui OpenRouter API.
    Mendukung alias cerdas seperti 'r1', 'claude', 'sonnet', 'deepseek', 'v3', 'gpt4o', 'qwen', 'free', dsb.
    Dilengkapi pengaman batas pengeluaran harian $1/hari.

[EN]: Sends queries or tasks to various AI models via the OpenRouter API.
Supports smart aliases such as 'r1', 'claude', 'sonnet', 'deepseek', 'v3', 'gpt4o', 'qwen', 'free', etc.
Includes a daily spending limit safeguard of $1/day.
"""
    api_key = get_api_key()
    if not api_key:
        return (
            "❌ Error: API Key OpenRouter belum dikonfigurasi.\n"
            "Silakan tempelkan API Key Anda ke berkas:\n"
            f"   {Path.home() / '.gemini' / 'openrouter_key.txt'}\n"
            "Atau tentukan variabel lingkungan OPENROUTER_API_KEY di mcp_config.json."
        )

    # Validasi pengaman batas limit harian ($1.00)
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
    """
[ID]: Menampilkan katalog model AI unggulan, alias pendek yang didukung, serta perkiraan biaya per 1 juta token.
[EN]: Displays a catalog of top AI models, supported shorthand aliases, and estimated costs per 1 million tokens.
"""
    katalog = """### 🏆 Katalog Model AI Pilihan OpenRouter

Anda dapat menggunakan Nama Panggilan (Alias) langsung pada parameter `model` di tool `tanya_openrouter`:

| Kategori & Kegunaan | Alias Cerdas | Model ID Resmi | Biaya (Input / Output per 1M Token) | Rekomendasi Kasus |
| :--- | :---: | :--- | :---: | :--- |
| 🧠 **Penalaran Super (Reasoning)** | `r1` | `deepseek/deepseek-r1` | $0.55 / $2.19 | Logika rumit, algoritma matematika, pelacakan bug misterius |
| 🧠 **Penalaran Cepat** | `o3-mini` | `openai/o3-mini` | $1.10 / $4.40 | Penalaran logis ala OpenAI |
| 💻 **Standar Emas Coding** | `claude` / `sonnet` | `anthropic/claude-3.5-sonnet` | $3.00 / $15.00 | Refactoring arsitektur besar, kode modular, zero halusinasi sintaks |
| 💻 **Spesialis Kode Ringan** | `qwen` | `qwen/qwen-2.5-coder-32b-instruct` | $0.08 / $0.16 | Sangat hemat dan cerdas untuk Python, JS, HTML |
| ⚡ **Harian Gesit & Super Hemat** | `deepseek` / `v3` | `deepseek/deepseek-chat` | $0.14 / $0.28 | Rekomendasi utama harian: cepat, murah, sangat pintar |
| ⚡ **Multifungsi Cepat** | `gpt4o` / `4o` | `openai/gpt-4o` | $2.50 / $10.00 | Ringkasan dokumen, analisis multi-bahasa, instruksi umum |
| 🎁 **100% GRATIS** | `free` | `meta-llama/llama-3.3-70b-instruct:free` | $0.00 (Gratis) | Eksperimen bebas biaya saat saldo kosong |
| 🎁 **100% GRATIS (R1)** | `deepseek-free` | `deepseek/deepseek-r1:free` | $0.00 (Gratis) | DeepSeek R1 versi antrean publik gratis |

💡 **Tips:** Jika ingin menggunakan model lain yang ada di openrouter.ai/models, Anda cukup memasukkan Model ID lengkapnya langsung ke parameter `model`.
"""
    return katalog


@mcp.tool()
def cek_koneksi_openrouter() -> str:
    """
[ID]: Mengecek validitas API Key OpenRouter serta status saldo, limit pemakaian, dan kuota rate limit akun.
[EN]: Validates the OpenRouter API Key and checks account balance, usage limit, and rate limit quota.
"""
    api_key = get_api_key()
    if not api_key:
        return (
            "⚠️ API Key OpenRouter belum ditemukan.\n\n"
            "Langkah aktivasi:\n"
            f"1. Buka berkas: {Path.home() / '.gemini' / 'openrouter_key.txt'}\n"
            "2. Tempelkan API Key Anda (misal `sk-or-v1-xxxxxxxx...`).\n"
            "3. Simpan berkas, lalu panggil kembali tool ini."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        # Cek informasi API Key
        auth_res = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=15)
        if auth_res.status_code != 200:
            return f"❌ Validasi API Key Gagal (Status {auth_res.status_code}): {auth_res.text}"

        auth_data = auth_res.json().get("data", {})
        label = auth_data.get("label", "Tanpa Label")
        usage_total = auth_data.get("usage", 0.0)
        usage_daily = auth_data.get("usage_daily", 0.0) or 0.0
        usage_weekly = auth_data.get("usage_weekly", 0.0) or 0.0
        usage_monthly = auth_data.get("usage_monthly", 0.0) or 0.0
        
        server_limit = auth_data.get("limit", None)
        server_limit_reset = auth_data.get("limit_reset", None)
        server_limit_remaining = auth_data.get("limit_remaining", None)
        is_free_tier = auth_data.get("is_free_tier", False)

        # Cek informasi Saldo / Kredit
        credit_info = ""
        try:
            credits_res = requests.get("https://openrouter.ai/api/v1/credits", headers=headers, timeout=15)
            if credits_res.status_code == 200:
                credit_data = credits_res.json().get("data", {})
                total_credits = credit_data.get("total_credits", 0.0)
                total_usage = credit_data.get("total_usage", 0.0)
                remaining = max(0.0, total_credits - total_usage)
                credit_info = (
                    f"- Total Kredit: ${total_credits:.4f}\n"
                    f"- Total Penggunaan Akun: ${total_usage:.4f}\n"
                    f"- Sisa Saldo Tersedia: ${remaining:.4f}\n"
                )
        except Exception:
            pass

        if server_limit is not None:
            limit_str = f"${server_limit:.2f} ({server_limit_reset or 'Tetap'}) | Sisa Limit: ${server_limit_remaining:.4f}"
        else:
            limit_str = "Unlimited di Cloud OpenRouter"

        hasil = (
            "✅ **Koneksi OpenRouter Berhasil!**\n\n"
            f"- **Label Kunci:** {label}\n"
            f"- **Total Pemakaian Kunci Ini:** ${usage_total:.4f}\n"
            f"- **Pemakaian Hari Ini:** ${usage_daily:.4f} / Limit ${DAILY_LIMIT_USD:.2f}\n"
            f"- **Pemakaian Minggu Ini:** ${usage_weekly:.4f}\n"
            f"- **Pemakaian Bulan Ini:** ${usage_monthly:.4f}\n"
            f"- **Batas Limit Server:** {limit_str}\n"
            f"- **Pengaman Limit Harian MCP:** Aktif (Maks ${DAILY_LIMIT_USD:.2f}/hari)\n"
            f"- **Tier Akun:** {'Gratis' if is_free_tier else 'Berbayar (Prioritas Tinggi)'}\n"
        )
        if credit_info:
            hasil += f"\n📊 **Informasi Saldo:**\n{credit_info}"

        hasil += "\n🎉 Server MCP OpenRouter siap digunakan dengan perlindungan batas limit harian!"
        return hasil

    except requests.exceptions.RequestException as e:
        return f"❌ Gagal terhubung ke OpenRouter API: {str(e)}"


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Server MCP OpenRouter untuk Antigravity IDE")
        print("\nTool yang tersedia:")
        print("  - tanya_openrouter(prompt, model='deepseek', system_prompt='')")
        print("  - daftar_model_rekomendasi()")
        print("  - cek_koneksi_openrouter()")
        print("\nJalankan tanpa argumen untuk mode MCP stdio transport.")
        sys.exit(0)

    # Menjalankan server MCP menggunakan transportasi standar stdio
    mcp.run()
