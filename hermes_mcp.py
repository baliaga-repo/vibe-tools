r"""
[ID]: Hermes Agent Worker MCP Server untuk Antigravity IDE.
Menghubungkan Antigravity dengan Hermes Agent lokal
sebagai worker mandiri untuk eksekusi perintah, riset file, web search, dan scripting
tanpa membebani token context model utama (Claude / GPT).

[EN]: Hermes Agent Worker MCP Server for Antigravity IDE.
Connects Antigravity with the local Hermes Agent
as an independent worker for command execution, file research, web search, and scripting
without burdening the main model context token (Claude / GPT).
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


DEFAULT_HERMES_MODEL = "deepseek/deepseek-r1"

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
[ID]: Kirim tugas ke Hermes Agent.
    
    Args:
        tugas: Deskripsi perintah atau tugas lengkap yang harus dilakukan Hermes.
        direktori_kerja: Folder tempat Hermes harus bekerja (opsional, otomatis menggunakan direktori kerja aktif saat ini).
        model: Model OpenRouter spesifik yang ingin dipakai (default: 'deepseek/deepseek-r1', atau alternatif: 'deepseek/deepseek-chat', 'meta-llama/llama-3.3-70b-instruct:free').

[EN]: Submit a task to the Hermes Agent.

    Args:
        tugas: Full description of the command or task for Hermes to execute.
        direktori_kerja: Folder where Hermes should operate (optional, defaults to the current working directory).
        model: Specific OpenRouter model to use (default: 'deepseek/deepseek-r1', or alternatives: 'deepseek/deepseek-chat', 'meta-llama/llama-3.3-70b-instruct:free').
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

    active_model = model.strip() if model and model.strip() else DEFAULT_HERMES_MODEL

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
    model_thinker: str = "anthropic/claude-3.5-haiku",
    model_worker: str = "deepseek/deepseek-chat"
) -> str:
    """
    Eksekusi pipeline Duo-Model di Hermes:
    Langkah 1: Claude Haiku merancang technical plan padat.
    Langkah 2: DeepSeek-Chat mengeksekusi penulisan kode dan command secara nyata.
    """
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
        "-m", model_thinker.strip()
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
            return f"Duo-Hermes Gagal di Tahap Thinking (Claude): {err or plan_output}"
    except Exception as e:
        return f"Error eksekusi Thinker (Claude): {str(e)}"

    # Fase 2: Eksekusi Nyata oleh DeepSeek-Chat (Worker)
    prompt_worker = (
        f"Anda adalah Agen Koding (Worker). Eksekusi rencana teknis berikut secara nyata ke dalam sistem file/terminal:\n\n"
        f"RENCANA TEKNIS DARI ARSITEK:\n{plan_output}\n\n"
        f"Lakukan pembuatan/pengeditan file yang dibutuhkan dan jalankan verifikasi. Laporkan ringkasan hasil eksekusi."
    )

    cmd_worker = [
        HERMES_EXE,
        "-z", prompt_worker,
        "--yolo",
        "-m", model_worker.strip()
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
            f"=== HASIL DUO-HERMES (CLAUDE HAIKU + DEEPSEEK CHAT) ===\n\n"
            f"[THINKER - Claude 3.5 Haiku Plan]:\n{plan_output}\n\n"
            f"[WORKER - DeepSeek-Chat Execution]:\n{worker_output or 'Eksekusi selesai tanpa output.'}"
        )
    except Exception as e:
        return f"Error eksekusi Worker (DeepSeek): {str(e)}"


if __name__ == "__main__":
    mcp.run()
