r"""
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

import shutil

def temukan_hermes_exe() -> str:
    exe = shutil.which("hermes") or shutil.which("hermes.exe")
    if exe:
        return exe
    script_candidate = Path(sys.executable).parent / "Scripts" / "hermes.exe"
    if script_candidate.exists():
        return str(script_candidate)
    local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    for candidate in local_app_data.glob("Programs/Python/*/Scripts/hermes.exe"):
        return str(candidate)
    return "hermes"

def temukan_hermes_repo() -> str:
    candidates = [
        Path("C:/hermes_env/hermes-agent"),
        Path.home() / "hermes_env" / "hermes-agent",
        Path.home() / ".hermes" / "hermes-agent",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return str(Path.home())

HERMES_EXE = temukan_hermes_exe()
HERMES_REPO = temukan_hermes_repo()


# Konfigurasi Persistent Model Duo-Hermes
SETTINGS_FILE = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "hermes" / "duo_settings.json"

def muat_duo_settings() -> dict:
    default_settings = {
        "thinker": "anthropic/claude-3.5-haiku",
        "worker": "deepseek/deepseek-chat",
        "solo": "deepseek/deepseek-chat"
    }
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                default_settings.update(data)
        except Exception:
            pass
    return default_settings

def simpan_duo_settings(settings: dict) -> bool:
    try:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

DEFAULT_HERMES_MODEL = muat_duo_settings().get("solo", "deepseek/deepseek-chat")


@mcp.tool(
    name="atur_model_hermes",
    description=(
        "Ubah konfigurasi model Hermes secara langsung dari chat percakapan. "
        "Dapat mengatur model Thinker (arsitek/penalaran), model Worker (eksekusi koding), "
        "atau model Solo (worker tunggal). Perubahan tersimpan permanen."
    )
)
def atur_model_hermes(
    model_thinker: str = "",
    model_worker: str = "",
    model_solo: str = ""
) -> str:
    """
    Atur model default untuk Hermes Agent.
    
    Args:
        model_thinker: Model OpenRouter untuk fase perancangan/thinking (misal: 'anthropic/claude-3.5-haiku', 'anthropic/claude-3.5-sonnet', 'deepseek/deepseek-r1').
        model_worker: Model OpenRouter untuk eksekusi kode/terminal (misal: 'deepseek/deepseek-chat', 'meta-llama/llama-3.3-70b-instruct:free').
        model_solo: Model OpenRouter untuk tugas tunggal delegasikan_ke_hermes (misal: 'deepseek/deepseek-chat').
    """
    settings = muat_duo_settings()
    diubah = []

    if model_thinker and model_thinker.strip():
        settings["thinker"] = model_thinker.strip()
        diubah.append(f"Thinker -> `{settings['thinker']}`")
    if model_worker and model_worker.strip():
        settings["worker"] = model_worker.strip()
        diubah.append(f"Worker  -> `{settings['worker']}`")
    if model_solo and model_solo.strip():
        settings["solo"] = model_solo.strip()
        diubah.append(f"Solo    -> `{settings['solo']}`")

    if not diubah:
        return (
            f"Tidak ada model yang diubah.\nKonfigurasi aktif saat ini:\n"
            f"- Thinker : `{settings['thinker']}`\n"
            f"- Worker  : `{settings['worker']}`\n"
            f"- Solo    : `{settings['solo']}`"
        )

    simpan_duo_settings(settings)
    return (
        f"✅ Konfigurasi model Hermes berhasil diperbarui dan disimpan:\n" +
        "\n".join([f"- {d}" for d in diubah]) +
        f"\n\nStatus lengkap saat ini:\n"
        f"- Thinker (Arsitek) : `{settings['thinker']}`\n"
        f"- Worker (Koding)   : `{settings['worker']}`\n"
        f"- Solo (Tunggal)    : `{settings['solo']}`"
    )


@mcp.tool(
    name="lihat_model_hermes",
    description="Lihat konfigurasi model aktif yang saat ini digunakan oleh Hermes Agent (Thinker, Worker, Solo)."
)
def lihat_model_hermes() -> str:
    """
[ID]: Melihat model yang sedang aktif digunakan oleh Hermes.
[EN]: View the model currently in use by Hermes.
"""
    settings = muat_duo_settings()
    return (
        f"📋 Konfigurasi Model Hermes Aktif:\n"
        f"- Thinker (Perancang/Arsitek) : `{settings['thinker']}`\n"
        f"- Worker (Eksekutor Kode)     : `{settings['worker']}`\n"
        f"- Solo (Worker Tunggal)       : `{settings['solo']}`\n"
        f"File pengaturan: `{SETTINGS_FILE}`"
    )

@mcp.tool(
    name="delegasikan_ke_hermes",
    description=(
        "Kirim tugas ke Hermes Agent lokal (background worker mandiri). "
        "Hermes dapat mengeksekusi terminal command/test, membaca & menyisir file luas, "
        "mencari regex di direktori kerja, scraping web, atau eksplorasi kode "
        "secara otonom dengan model reasoning DeepSeek R1 tanpa membuang token Claude/GPT. "
        "Hasil akan otomatis diringkas padat agar efisien di context window."
    )
)
def delegasikan_ke_hermes(tugas: str, direktori_kerja: str = "", model: str = DEFAULT_HERMES_MODEL) -> str:
    """
    Kirim tugas ke Hermes Agent.
    
    Args:
        tugas: Deskripsi perintah atau tugas lengkap yang harus dilakukan Hermes.
        direktori_kerja: Folder tempat Hermes harus bekerja (opsional, otomatis menggunakan direktori kerja aktif saat ini).
        model: Model OpenRouter spesifik yang ingin dipakai (default: 'deepseek/deepseek-r1', atau alternatif: 'deepseek/deepseek-chat', 'meta-llama/llama-3.3-70b-instruct:free').
    """
    # Tentukan direktori kerja aktif secara cerdas
    target_cwd = ""
    if direktori_kerja and Path(direktori_kerja).exists():
        target_cwd = direktori_kerja
    else:
        current_dir = os.getcwd()
        # Hindari fallback ke direktori sistem Windows yang tidak relevan
        if current_dir and not current_dir.lower().endswith("system32") and Path(current_dir).exists():
            target_cwd = current_dir
        elif Path(HERMES_REPO).exists():
            target_cwd = HERMES_REPO
        else:
            target_cwd = str(Path.home())

    # Tambahkan arahan kompresi token agar Hermes tidak membuang teks berlebihan ke context
    instruksi_tugas = (
        f"{tugas}\n\n"
        "(Catatan: Berikan ringkasan padat, langsung ke temuan/akar masalah/nomor baris atau poin hasil eksekusi. "
        "Jangan dump output log mentah yang terlalu panjang agar menghemat token context.)"
    )

    settings = muat_duo_settings()
    active_model = model.strip() if model and model.strip() else settings.get("solo", "deepseek/deepseek-chat")

    cmd = [
        HERMES_EXE,
        "-z", instruksi_tugas,  # oneshot mode dengan task spesifik
        "--yolo",               # eksekusi otonom tanpa prompt interaktif
        "-m", active_model
    ]

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
            return f"Hermes Error (code {result.returncode}):\n{errors or output}"

        if not output and errors:
            return f"Hermes Output (stderr):\n{errors}"

        return output or "Tugas selesai dijalankan oleh Hermes Agent (tanpa output teks)."

    except subprocess.TimeoutExpired:
        return "Hermes Timeout: Tugas membutuhkan waktu lebih dari 5 menit."
    except Exception as e:
        return f"Gagal menjalankan Hermes Agent: {str(e)}"


@mcp.tool(
    name="delegasikan_duo_hermes",
    description=(
        "Pipeline Duo-Model di dalam Hermes: Mengombinasikan Claude 3.5 Haiku sebagai THINKER "
        "(merancang arsitektur & langkah teknis) dan DeepSeek-Chat sebagai WORKER "
        "(mengekskusi penulisan kode, file, dan terminal otonom). "
        "Gemini/Antigravity hanya memicu tugas di awal, seluruh proses berpikir dan eksekusi berjalan di OpenRouter."
    )
)
def delegasikan_duo_hermes(
    tugas: str,
    direktori_kerja: str = "",
    model_thinker: str = "",
    model_worker: str = ""
) -> str:
    """
[ID]: Eksekusi pipeline Duo-Model di Hermes:
    Langkah 1: Claude Haiku merancang technical plan padat.
    Langkah 2: DeepSeek-Chat mengeksekusi penulisan kode dan command secara nyata.

[EN]: Execute the Duo-Model pipeline in Hermes:
    Step 1: Claude Haiku designs a concise technical plan.
    Step 2: DeepSeek-Chat executes the actual code writing and commands.
"""
    settings = muat_duo_settings()
    active_thinker = model_thinker.strip() if model_thinker and model_thinker.strip() else settings.get("thinker", "anthropic/claude-3.5-haiku")
    active_worker = model_worker.strip() if model_worker and model_worker.strip() else settings.get("worker", "deepseek/deepseek-chat")

    target_cwd = direktori_kerja if direktori_kerja and Path(direktori_kerja).exists() else os.getcwd()
    if not target_cwd or target_cwd.lower().endswith("system32"):
        target_cwd = HERMES_REPO if Path(HERMES_REPO).exists() else str(Path.home())

    # Fase 1: Thinking oleh Claude Haiku
    prompt_thinker = (
        f"Anda adalah Arsitek Perangkat Lunak senior (Thinker). Analisis tugas berikut dan buatkan rencana aksi "
        f"teknis yang sangat spesifik, terstruktur, dan siap dieksekusi tanpa basa-basi untuk agen koding (Worker):\n\n"
        f"TUGAS: {tugas}\n\n"
        f"Format output: Ringkas, cantumkan file target, algoritma/logika yang harus ditulis, dan perintah terminal yang diperlukan."
    )

    cmd_thinker = [
        HERMES_EXE,
        "-z", prompt_thinker,
        "--yolo",
        "-m", active_thinker
    ]

    try:
        res_thinker = subprocess.run(
            cmd_thinker,
            cwd=target_cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=240
        )
        plan_output = res_thinker.stdout.strip()
        if res_thinker.returncode != 0 or not plan_output:
            err = res_thinker.stderr.strip()
            return f"Duo-Hermes Gagal di Tahap Thinking ({active_thinker}): {err or plan_output}"
    except Exception as e:
        return f"Error eksekusi Thinker ({active_thinker}): {str(e)}"

    # Fase 2: Eksekusi Nyata oleh Worker
    prompt_worker = (
        f"Anda adalah Agen Koding (Worker). Eksekusi rencana teknis berikut secara nyata ke dalam sistem file/terminal:\n\n"
        f"RENCANA TEKNIS DARI ARSITEK:\n{plan_output}\n\n"
        f"Lakukan pembuatan/pengeditan file yang dibutuhkan dan jalankan verifikasi. Laporkan ringkasan hasil eksekusi."
    )

    cmd_worker = [
        HERMES_EXE,
        "-z", prompt_worker,
        "--yolo",
        "-m", active_worker
    ]

    try:
        res_worker = subprocess.run(
            cmd_worker,
            cwd=target_cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=360
        )
        worker_output = res_worker.stdout.strip()
        if res_worker.returncode != 0:
            err = res_worker.stderr.strip()
            return f"Duo-Hermes Berhasil Berpikir, tapi Gagal Eksekusi Worker: {err or worker_output}"

        return (
            f"=== HASIL DUO-HERMES ({active_thinker} + {active_worker}) ===\n\n"
            f"[THINKER - {active_thinker} Plan]:\n{plan_output}\n\n"
            f"[WORKER - {active_worker} Execution]:\n{worker_output or 'Eksekusi selesai tanpa output.'}"
        )
    except Exception as e:
        return f"Error eksekusi Worker ({active_worker}): {str(e)}"


if __name__ == "__main__":
    mcp.run()
