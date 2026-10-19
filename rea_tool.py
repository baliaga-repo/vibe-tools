"""
[ID]: REA (Reverse Engineer Anything) CLI & Python Helper Wrapper.
Skrip ini menyediakan pembungkus (wrapper) Python untuk menjalankan perintah REA:
- Menjalankan analisis binary, PE, JavaScript, dan SQLite dengan token limit & kompresi output otomatis.
- Mendukung mode CLI langsung maupun impor sebagai modul Python.
- Membantu rekayasa balik file biner aplikasi (seperti DLL DaVinci Resolve) atau file database proyek.

[EN]: REA (Reverse Engineer Anything) CLI & Python Helper Wrapper.
This script provides a Python wrapper to execute REA commands:
- Runs binary, PE, JavaScript, and SQLite analysis with token limits & automatic output compression.
- Supports direct CLI execution as well as Python module import.
- Assists in reverse engineering application binaries (such as DaVinci Resolve DLLs) or project databases.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Setup encoding konsol UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def temukan_rea_executable() -> str:
    """Mencari executable rea di sistem (rea.cmd di Windows atau rea di Unix)."""
    exe_name = "rea.cmd" if os.name == "nt" else "rea"
    exe = shutil.which(exe_name)
    if exe:
        return exe

    # Cek di folder npm global standar Windows
    app_data = os.environ.get("APPDATA")
    if app_data:
        kandidat = Path(app_data) / "npm" / exe_name
        if kandidat.exists():
            return str(kandidat)
    return exe_name


def jalankan_rea(perintah: str, target_path: str = "", opsi_tambahan: list[str] | None = None, format_output: str = "json") -> dict | str:
    """
    Menjalankan subperintah REA dan mengembalikan output terstruktur.
    
    Args:
        perintah: Nama subperintah REA (misal: 'inspect-pe-resources', 'inspect-binary-layout', 'analyze')
        target_path: Path berkas target yang akan dianalisis (opsional)
        opsi_tambahan: Argumen tambahan untuk CLI REA
        format_output: Format output ('json', 'md', 'toon', 'yaml')
    """
    rea_exe = temukan_rea_executable()
    cmd = [rea_exe, perintah]
    
    if target_path:
        cmd.append(str(target_path))
        
    cmd.extend(["--format", format_output])
    
    if opsi_tambahan:
        cmd.extend(opsi_tambahan)

    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        
        stdout = res.stdout.strip()
        stderr = res.stderr.strip()

        if format_output == "json" and stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                pass
                
        return stdout or stderr
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="REA (Reverse Engineer Anything) Python Helper")
    parser.add_argument("command", help="Subperintah REA (contoh: inspect-pe-resources, inspect-binary-layout, analyze, providers, doctor)")
    parser.add_argument("target", nargs="?", default="", help="Path berkas yang akan dianalisis (opsional)")
    parser.add_argument("--format", choices=["json", "md", "toon", "yaml"], default="json", help="Format keluaran (default: json)")
    parser.add_argument("--limit-lines", type=int, default=50, help="Batas baris output di terminal agar efisien (default: 50)")

    args, unknown = parser.parse_known_args()

    if args.command == "doctor":
        hasil = jalankan_rea("mcp", "doctor", format_output=args.format)
    else:
        hasil = jalankan_rea(args.command, args.target, unknown, format_output=args.format)

    if isinstance(hasil, dict):
        teks = json.dumps(hasil, indent=2)
    else:
        teks = str(hasil)

    baris = teks.splitlines()
    if len(baris) > args.limit_lines:
        print("\n".join(baris[:args.limit_lines]))
        print(f"\n... [Output dipotong: {len(baris) - args.limit_lines} baris disembunyikan untuk efisiensi context] ...")
    else:
        print(teks)


if __name__ == "__main__":
    main()
