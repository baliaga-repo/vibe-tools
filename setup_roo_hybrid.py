# -*- coding: utf-8 -*-
"""
[ID]: Installer & Updater Portabel Ekosistem Roo Code Hybrid Dual-Cockpit (setup_roo_hybrid.py).
Memasang atau memperbarui konfigurasi .roomodes, .roo/rules/*, .roo/commands/*, dan .roo/mcp.json
ke workspace saat ini maupun ke project lain (--target) secara non-destruktif (Smart Managed Copy).

Penggunaan:
    python vibe_tools/setup_roo_hybrid.py
    python vibe_tools/setup_roo_hybrid.py --target "D:/ProjectLain"
    python vibe_tools/setup_roo_hybrid.py --setup-ollama
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Tuple

if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VIBE_TOOLS_DIR: Path = Path(__file__).resolve().parent
TEMPLATE_ROOT: Path = VIBE_TOOLS_DIR / "roo_hybrid" / "templates"

TEMPLATE_ATURAN_SPESIFIK_PROYEK: str = """# Project-Specific Custom Rules (Protected File)

- File ini (`99-project-custom.md`) **100% dilindungi** dan TIDAK AKAN PERNAH ditimpa saat Anda menjalankan update `setup_roo_hybrid.py`.
- Tambahkan aturan unik khusus proyek ini di bawah baris ini (misal: konvensi domain, path aset lokal, atau pengecualian folder).
- Aturan utama tetap mengacu pada `.agents/AGENTS.md` dan `.agents/MAP.md`.
"""

MODEL_OLLAMA_TARGET: Tuple[str, ...] = (
    "nomic-embed-text",
    "qwen2.5-coder:3b-instruct",
    "qwen2.5-coder:7b-instruct-q4_K_M",
)


def tentukan_target_proyek(arg_target: str = "") -> Path:
    """[ID]: Menentukan direktori root proyek target pemasangan."""
    if arg_target:
        target = Path(arg_target).expanduser().resolve()
        target.mkdir(parents=True, exist_ok=True)
        return target
    if VIBE_TOOLS_DIR.name == "vibe_tools":
        return VIBE_TOOLS_DIR.parent
    return Path.cwd()


def sinkronkan_template_universal(target_dir: Path) -> Tuple[int, int]:
    """
    [ID]: Menyalin dan memperbarui seluruh berkas template universal dari vibe_tools/roo_hybrid/templates
    ke direktori proyek target tanpa menyentuh berkas kustom spesifik proyek.
    """
    if not TEMPLATE_ROOT.exists():
        raise FileNotFoundError(f"Folder template tidak ditemukan: {TEMPLATE_ROOT}")

    jumlah_baru = 0
    jumlah_update = 0

    for sumber in sorted(TEMPLATE_ROOT.rglob("*")):
        if sumber.is_dir():
            continue
        rel_path = sumber.relative_to(TEMPLATE_ROOT)
        tujuan = target_dir / rel_path
        tujuan.parent.mkdir(parents=True, exist_ok=True)

        isi_sumber = sumber.read_text(encoding="utf-8")
        if not tujuan.exists():
            tujuan.write_text(isi_sumber, encoding="utf-8", newline="\n")
            print(f"  [BARU]   {rel_path.as_posix()}")
            jumlah_baru += 1
        else:
            isi_lama = tujuan.read_text(encoding="utf-8")
            if isi_lama.strip() != isi_sumber.strip():
                tujuan.write_text(isi_sumber, encoding="utf-8", newline="\n")
                print(f"  [UPDATE] {rel_path.as_posix()}")
                jumlah_update += 1
            else:
                print(f"  [TETAP]  {rel_path.as_posix()} (sudah versi terbaru)")

    # Pastikan file aturan spesifik proyek tersedia dan tidak pernah ditimpa
    file_kustom = target_dir / ".roo" / "rules" / "99-project-custom.md"
    file_kustom.parent.mkdir(parents=True, exist_ok=True)
    if not file_kustom.exists():
        file_kustom.write_text(TEMPLATE_ATURAN_SPESIFIK_PROYEK, encoding="utf-8", newline="\n")
        print("  [BARU]   .roo/rules/99-project-custom.md (dilindungi dari overwrite)")
    else:
        print("  [AMAN]   .roo/rules/99-project-custom.md (aturan spesifik proyek dipertahankan)")

    return jumlah_baru, jumlah_update


def bangun_mcp_json_bebas_rahasia(target_dir: Path) -> None:
    """
    [ID]: Membangun berkas .roo/mcp.json secara dinamis tanpa menyimpan API Key mentah di dalamnya.
    Server openrouter & hermes_agent aktif, sedangkan rea dinonaktifkan (disabled: true) secara default.
    """
    gemini_dir = Path.home() / ".gemini"
    py_exe = Path(sys.executable).as_posix()

    # Gunakan skrip di ~/.gemini jika sudah terpasang, fallback ke vibe_tools proyek
    or_script = gemini_dir / "openrouter_mcp.py"
    if not or_script.exists():
        or_script = VIBE_TOOLS_DIR / "openrouter_mcp.py"

    hermes_script = gemini_dir / "hermes_mcp.py"
    if not hermes_script.exists():
        hermes_script = VIBE_TOOLS_DIR / "hermes_mcp.py"

    rea_script = gemini_dir / "rea-mcp" / "rea_tool.py"
    if not rea_script.exists():
        rea_script = VIBE_TOOLS_DIR / "rea_tool.py"

    konfigurasi_mcp: Dict[str, Any] = {
        "mcpServers": {
            "openrouter": {
                "command": py_exe,
                "args": [or_script.as_posix()],
                "disabled": False,
                "alwaysAllow": [
                    "tanya_openrouter",
                    "daftar_model_rekomendasi",
                    "cek_koneksi_openrouter"
                ]
            },
            "hermes_agent": {
                "command": py_exe,
                "args": [hermes_script.as_posix()],
                "disabled": False,
                "alwaysAllow": [
                    "delegasikan_ke_hermes"
                ]
            },
            "rea": {
                "command": py_exe,
                "args": [rea_script.as_posix()],
                "disabled": True,
                "alwaysAllow": []
            }
        }
    }

    mcp_path = target_dir / ".roo" / "mcp.json"
    mcp_path.parent.mkdir(parents=True, exist_ok=True)
    mcp_path.write_text(json.dumps(konfigurasi_mcp, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("  [MCP]    .roo/mcp.json (openrouter: ON, hermes: ON, rea: OFF/hemat 25K token, bebas API key)")


def cek_atau_pasang_ollama(jalankan_pull: bool = False) -> None:
    """[ID]: Memeriksa ketersediaan Ollama dan mengatur optimasi VRAM 6 GB jika diminta."""
    ollama_bin = shutil.which("ollama")
    if not ollama_bin:
        print("\n[INFO] Ollama belum terdeteksi di PATH. Mode Cloud + MCP tetap siap 100%.")
        print("       (Unduh Ollama di https://ollama.com jika ingin memakai Local Scout 3B/7B $0)")
        return

    if not jalankan_pull:
        print(f"\n[OK] Ollama terdeteksi ({ollama_bin}).")
        print("     Tip: Jalankan dengan flag '--setup-ollama' untuk auto-set VRAM 6GB & unduh model 3B/7B/Embed.")
        return

    print("\n[OLLAMA] Mengatur variabel environment optimasi RTX 3060 (6 GB VRAM)...")
    env_vars = {
        "OLLAMA_FLASH_ATTENTION": "1",
        "OLLAMA_KV_CACHE_TYPE": "q8_0",
        "OLLAMA_KEEP_ALIVE": "5m",
        "OLLAMA_MAX_LOADED_MODELS": "2",
    }
    for k, v in env_vars.items():
        os.environ[k] = v
        if sys.platform.startswith("win"):
            subprocess.run(["setx", k, v], capture_output=True, text=True)
        print(f"  • {k} = {v}")

    for model in MODEL_OLLAMA_TARGET:
        print(f"[OLLAMA] Menarik model {model}...")
        subprocess.run([ollama_bin, "pull", model], check=False)


def pasang_roo_hybrid(target_path: str = "", setup_ollama: bool = False) -> Path:
    """[ID]: Titik masuk publik untuk memasang/meng-update Roo Code Hybrid di direktori target."""
    target_dir = tentukan_target_proyek(target_path)
    print("=" * 70)
    print("🪃 SETUP & UPDATE ROO CODE HYBRID DUAL-COCKPIT (VIBE TOOLS PORTABLE)")
    print(f"Sumber Template : {TEMPLATE_ROOT}")
    print(f"Proyek Target   : {target_dir}")
    print("=" * 70)

    baru, update = sinkronkan_template_universal(target_dir)
    bangun_mcp_json_bebas_rahasia(target_dir)
    cek_atau_pasang_ollama(jalankan_pull=setup_ollama)

    print("-" * 70)
    print(f"✅ Selesai! ({baru} berkas baru, {update} berkas diperbarui di '{target_dir.name}')")
    print("   Shortcut siap pakai: /pakai-rag | /pakai-3b | /pakai-7b | /adu-metode | /grill-me")
    print("=" * 70)
    return target_dir


def main() -> None:
    """[ID]: Antarmuka baris perintah (CLI) untuk setup_roo_hybrid.py."""
    parser = argparse.ArgumentParser(
        description="Installer & Updater Portabel Roo Code Hybrid Dual-Cockpit"
    )
    parser.add_argument(
        "--target",
        type=str,
        default="",
        help="Path folder proyek lain yang ingin dipasang/di-update (opsional)"
    )
    parser.add_argument(
        "--setup-ollama",
        action="store_true",
        help="Atur variabel environment VRAM RTX 3060 dan tarik ke-3 model Ollama otomatis"
    )
    args = parser.parse_args()
    pasang_roo_hybrid(target_path=args.target, setup_ollama=args.setup_ollama)


if __name__ == "__main__":
    main()

