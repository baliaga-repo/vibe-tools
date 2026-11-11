"""Server MCP OpenRouter Antigravity IDE: integrasi model AI, daily limit, dan Otak-Tangan debug loop."""
import os, sys, json, urllib.request, urllib.error
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    from mcp.server.mcpserver import MCPServer
    mcp = MCPServer("openrouter")
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("openrouter")
    except Exception as err:
        raise RuntimeError(f"Gagal memuat modul MCP: {err}")

MAX_SESSION_TURNS = 4
SESSION_CACHE_FILE = Path.home() / ".gemini" / "cache" / "openrouter_sessions.json"
DAILY_LIMIT_USD = float(os.environ.get("OPENROUTER_DAILY_LIMIT", "1.00"))

MODEL_ALIASES = {
    "r1": "deepseek/deepseek-r1-0528", "deepseek-r1": "deepseek/deepseek-r1-0528", "o3-mini": "openai/o3-mini",
    "claude": "anthropic/claude-sonnet-4.6", "sonnet": "anthropic/claude-sonnet-4.6", "claude-4.6": "anthropic/claude-sonnet-4.6",
    "opus": "anthropic/claude-opus-4.6", "claude-opus": "anthropic/claude-opus-4.6",
    "claude-4.5": "anthropic/claude-sonnet-4.5", "claude-thinking": "anthropic/claude-sonnet-4.6",
    "haiku": "anthropic/claude-haiku-4.5", "claude-haiku": "anthropic/claude-haiku-4.5",
    "codex": "openai/gpt-5-codex", "gpt5-codex": "openai/gpt-5-codex", "gpt5": "openai/gpt-5", "gpt4o": "openai/gpt-4o",
    "deepseek": "deepseek/deepseek-v3.2", "v3": "deepseek/deepseek-v3.2", "v3.2": "deepseek/deepseek-v3.2",
    "qwen": "qwen/qwen3-coder", "qwen-coder": "qwen/qwen3-coder", "qwen3": "qwen/qwen3-coder",
    "gemini": "google/gemini-2.5-flash", "gemini-flash": "google/gemini-2.5-flash", "gemini-pro": "google/gemini-2.5-pro",
    "free": "qwen/qwen3-coder:free", "gemma-free": "google/gemma-4-31b-it:free", "deepseek-free": "deepseek/deepseek-chat",
}

DEBUG_SYSTEM_PROMPT = (
    "[PERAN]: Lead Debugging Architect pola Otak-Tangan (Brain & Hands) bersama Gemini di Antigravity IDE.\n"
    "Tugas: Memimpin investigasi bug ilmiah melalui eksperimen minimal bertahap.\n"
    "ATURAN FORMAT WAJIB (Sertakan tag ini di setiap respons):\n"
    "[HIPOTESIS]: Dugaan teknis spesifik penyebab bug yang diuji.\n"
    "[PERINTAH_TES]: Perintah CLI/pytest/python minimal untuk dieksekusi Gemini di terminal IDE (atau '-' jika selesai).\n"
    "[STATUS]: 'LANJUT_TES' (jika masih butuh hasil pengetesan) atau 'SELESAI' (jika akar masalah sudah pasti).\n"
    "[SOLUSI_KODE]: (Hanya jika SELESAI) Rangkuman perbaikan kode presisi untuk diterapkan Gemini.\n"
    "[PELAJARAN_KUNCI]: (Hanya jika SELESAI) 1-2 kalimat intisari akar masalah & pencegahannya untuk self-learning.\n"
    "Gunakan bahasa teknis ringkas dan padat."
)

def _http_json(url: str, headers: dict = None, payload: dict = None, timeout: int = 90) -> tuple[int, dict, str]:
    """Helper HTTP mandiri menggunakan standard library urllib."""
    headers, data = headers or {}, (json.dumps(payload).encode("utf-8") if payload is not None else None)
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return resp.status, json.loads(raw), raw
            except Exception:
                return resp.status, {}, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw), raw
        except Exception:
            return e.code, {}, raw
    except urllib.error.URLError as e:
        raise RuntimeError(f"Kesalahan koneksi jaringan: {e.reason}")
    except Exception as e:
        raise RuntimeError(str(e))

def get_api_key() -> str:
    """Mengambil OpenRouter API Key dari environment variable atau ~/.gemini/openrouter_key.txt."""
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
    """Menerjemahkan alias pendek ke model ID resmi OpenRouter."""
    return MODEL_ALIASES.get(alias_or_id.strip().lower(), alias_or_id.strip()) if alias_or_id else "deepseek/deepseek-chat"


def check_daily_limit_exceeded(api_key: str) -> tuple[bool, float]:
    """
[ID]: Mengecek apakah penggunaan hari ini (usage_daily) melebihi batas pengeluaran harian.
[EN]: Check if today's usage (usage_daily) exceeds the daily spending limit.
"""
    try:
        status, data_json, _ = _http_json("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {api_key}"}, timeout=5)
        if status == 200:
            daily_usage = float(data_json.get("data", {}).get("usage_daily", 0.0) or 0.0)
            return (daily_usage >= DAILY_LIMIT_USD), daily_usage
    except Exception:
        pass
    return False, 0.0


def _kelola_sesi(session_id: str, user_prompt: str = None, assistant_reply: str = None) -> list[dict]:
    """
[ID]: Mengelola riwayat percakapan sesi (Sliding Window max 4 putaran / 8 pesan terakhir).
[EN]: Manage session conversation history (Sliding Window max 4 turns / last 8 messages).
"""
    if not session_id:
        return []
    clean_id, is_reset = session_id.strip(), False
    if clean_id.lower().startswith("new:") or clean_id.lower().startswith("reset:"):
        is_reset, clean_id = True, clean_id.split(":", 1)[1].strip()
    elif clean_id.lower() == "reset":
        return []

    sessions = {}
    try:
        if SESSION_CACHE_FILE.exists():
            sessions = json.loads(SESSION_CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        sessions = {}

    if is_reset and clean_id in sessions:
        sessions.pop(clean_id, None)
        try:
            SESSION_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            SESSION_CACHE_FILE.write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    history = sessions.get(clean_id, [])
    if user_prompt and assistant_reply:
        history.extend([{"role": "user", "content": user_prompt}, {"role": "assistant", "content": assistant_reply}])
        if len(history) > MAX_SESSION_TURNS * 2:
            history = history[-(MAX_SESSION_TURNS * 2):]
        sessions[clean_id] = history
        try:
            SESSION_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            SESSION_CACHE_FILE.write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    return list(history)


@mcp.tool()
def tanya_openrouter(
    prompt: str,
    model: str = "deepseek",
    system_prompt: str = "",
    session_id: str = "",
    mode_debug: bool = False,
) -> str:
    """
[ID]: Mengirim pertanyaan atau menjalankan siklus debugging bertahap ke AI via OpenRouter API.
[EN]: Send a query or run a step-by-step debugging cycle with the AI via the OpenRouter API.
"""
    api_key = get_api_key()
    if not api_key:
        return f"❌ Error: API Key belum dikonfigurasi di {Path.home() / '.gemini' / 'openrouter_key.txt'}"

    is_exceeded, daily_spend = check_daily_limit_exceeded(api_key)
    if is_exceeded:
        return f"🛑 Batas Pengeluaran Harian Tercapai! (${daily_spend:.4f} / Maks ${DAILY_LIMIT_USD:.2f}/hari)."

    model_id = resolve_model_id(model)
    full_system = f"{DEBUG_SYSTEM_PROMPT}\n\n{system_prompt}".strip() if mode_debug else system_prompt.strip()
    messages = [{"role": "system", "content": full_system}] if full_system else []

    clean_sid = session_id.strip()
    if clean_sid.lower().startswith(("new:", "reset:")):
        _kelola_sesi(clean_sid)
        clean_sid = clean_sid.split(":", 1)[1].strip()

    if clean_sid and clean_sid.lower() != "reset":
        messages.extend(_kelola_sesi(clean_sid))

    messages.append({"role": "user", "content": prompt})
    payload = {"model": model_id, "messages": messages}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/google/antigravity",
        "X-Title": "Antigravity OpenRouter MCP",
    }

    try:
        status, res_json, raw_text = _http_json("https://openrouter.ai/api/v1/chat/completions", headers, payload, 90)
        if status == 200:
            choices = res_json.get("choices", [])
            if choices and "message" in choices[0]:
                content = choices[0]["message"].get("content", "")
                if clean_sid and clean_sid.lower() != "reset":
                    _kelola_sesi(clean_sid, user_prompt=prompt, assistant_reply=content)
                usage = res_json.get("usage", {})
                tokens_info = ""
                if usage:
                    p_tok, c_tok, t_tok = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), usage.get("total_tokens", 0)
                    tag_sess = f" | Sesi: {clean_sid}" if clean_sid else ""
                    tag_dbg = " [DEBUG]" if mode_debug else ""
                    tokens_info = f"\n\n*(Model: {model_id}{tag_dbg}{tag_sess} | Token: {p_tok} in / {c_tok} out / {t_tok} total)*"
                return content + tokens_info
            return "⚠️ Respons dari OpenRouter tidak memiliki pesan teks yang valid."
        err_msg = res_json.get("error", {}).get("message", raw_text) if isinstance(res_json, dict) else raw_text
        return f"❌ Error OpenRouter API (Status {status}): {err_msg}"
    except TimeoutError:
        return "❌ Request timeout: Model membutuhkan waktu lebih dari 90 detik."
    except Exception as e:
        return f"❌ Kesalahan jaringan saat menghubungi OpenRouter: {str(e)}"


@mcp.tool()
def daftar_model_rekomendasi() -> str:
    """
[ID]: Menampilkan katalog model AI unggulan dan alias pendek yang didukung.
[EN]: Display the catalog of featured AI models and supported short aliases.
"""
    return """### 🏆 Katalog Model AI Unggulan OpenRouter
| Kategori | Alias | Model ID Resmi | Kasus Rekomendasi |
| :--- | :---: | :--- | :--- |
| 👑 **Standar Emas Coding** | `claude` / `sonnet` | `anthropic/claude-sonnet-4.6` | Debugging terarah, refactoring arsitektur |
| 🏛️ **Flagship Kompleks** | `opus` | `anthropic/claude-opus-4.6` | Investigasi bug sistemik multi-file rumit |
| 🛠️ **Spesialis Engineering** | `codex` / `gpt5` | `openai/gpt-5-codex` | Rekayasa perangkat lunak presisi & clean code |
| 🧠 **Penalaran (Reasoning)** | `r1` | `deepseek/deepseek-r1-0528` | Logika rumit, algoritma matematika |
| ⚡ **Harian Gesit & Super Hemat** | `deepseek` / `v3` | `deepseek/deepseek-v3.2` | Rekomendasi harian utama (DSA), super hemat |
| 💻 **Spesialis Kode Open-Weight** | `qwen` / `qwen3` | `qwen/qwen3-coder` | Cepat & efisien untuk Python/JS (MoE) |
| 🚀 **Thinker Ringan** | `haiku` | `anthropic/claude-haiku-4.5` | Cepat & cerdas untuk tugas pembantu |
| 🎁 **100% Gratis** | `free` | `qwen/qwen3-coder:free` | Eksperimen koding bebas biaya |"""


@mcp.tool()
def cek_koneksi_openrouter() -> str:
    """
[ID]: Mengecek validitas API Key, saldo, dan limit pemakaian OpenRouter.
[EN]: Check OpenRouter API key validity, balance, and usage limit.
"""
    api_key = get_api_key()
    if not api_key:
        return f"⚠️ API Key belum ditemukan di {Path.home() / '.gemini' / 'openrouter_key.txt'}"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        s_auth, j_auth, r_auth = _http_json("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=15)
        if s_auth != 200:
            return f"❌ Validasi Gagal (Status {s_auth}): {r_auth}"
        data = j_auth.get("data", {})
        label, u_total, u_daily = data.get("label", "Tanpa Label"), data.get("usage", 0.0), data.get("usage_daily", 0.0) or 0.0
        rem_cred = ""
        s_cr, j_cr, _ = _http_json("https://openrouter.ai/api/v1/credits", headers=headers, timeout=15)
        if s_cr == 200:
            c_data = j_cr.get("data", {})
            rem_cred = f"- Sisa Saldo: ${max(0.0, c_data.get('total_credits', 0.0) - c_data.get('total_usage', 0.0)):.4f}\n"
        return (
            f"✅ **Koneksi OpenRouter Berhasil!**\n- Label: {label}\n- Total Pakai: ${u_total:.4f}\n"
            f"- Hari Ini: ${u_daily:.4f} / Limit ${DAILY_LIMIT_USD:.2f}\n{rem_cred}🎉 Server MCP siap digunakan!"
        )
    except Exception as e:
        return f"❌ Gagal terhubung ke OpenRouter API: {str(e)}"


if __name__ == "__main__":
    mcp.run()
