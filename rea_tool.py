"""
[ID]: REA (Reverse Engineer Anything) CLI, Helper Wrapper & Dual-IDE Toggle.
Skrip ini menyediakan utilitas terpadu untuk ekosistem REA:
- Mengendalikan saklar aktif/nonaktif REA MCP (--enable/--disable/--status) serentak di Antigravity dan Roo Code.
- Menghemat ~25.000 token per pesan saat REA tidak digunakan.
- Menjalankan analisis binary, PE, JavaScript, dan SQLite dengan token limit & kompresi output otomatis.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# Setup encoding konsol UTF-8
if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def temukan_rea_executable() -> str:
    """[ID]: Mencari executable rea di sistem (rea.cmd di Windows atau rea di Unix)."""
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


def _update_mcp_config_file(config_path: Path, disabled_val: Optional[bool]) -> Optional[bool]:
    """
    [ID]: Membaca atau memperbarui kunci mcpServers.rea.disabled pada berkas JSON.
    Jika disabled_val bernilai None, fungsi hanya membaca status saat ini.
    """
    if not config_path.exists():
        if disabled_val is None:
            return None
        config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"mcpServers": {}}
    else:
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            data = {"mcpServers": {}}

    servers = data.setdefault("mcpServers", {})
    rea_config = servers.setdefault("rea", {})

    current_status = rea_config.get("disabled", False)

    if disabled_val is not None:
        rea_config["disabled"] = disabled_val
        try:
            config_path.write_text(json.dumps(data, indent=2), encoding="utf-8", newline="\n")
            return disabled_val
        except (PermissionError, OSError) as e:
            print(f"  [PERINGATAN] Gagal menulis ke {config_path} ({e}). Periksa hak akses file.")
            return current_status
    return current_status


def kelola_status_rea_mcp(aksi: str, target_workspace: Optional[Path] = None) -> Dict[str, Any]:
    """
    [ID]: Mengendalikan saklar toggle REA MCP serentak pada dua kokpit IDE:
    1. Antigravity Global: ~/.gemini/config/mcp_config.json
    2. Roo Code Workspace: <target_workspace>/.roo/mcp.json
    """
    ws_root = (target_workspace or Path.cwd()).resolve()
    antigravity_cfg = Path.home() / ".gemini" / "config" / "mcp_config.json"
    roo_cfg = ws_root / ".roo" / "mcp.json"

    val_to_set: Optional[bool] = None
    if aksi == "enable":
        val_to_set = False  # disabled = False -> AKTIF
    elif aksi == "disable":
        val_to_set = True   # disabled = True -> NONAKTIF

    ag_disabled = _update_mcp_config_file(antigravity_cfg, val_to_set)
    roo_disabled = _update_mcp_config_file(roo_cfg, val_to_set)

    return {
        "antigravity": {
            "path": antigravity_cfg,
            "is_active": (ag_disabled is False) if ag_disabled is not None else None,
            "disabled": ag_disabled
        },
        "roo_code": {
            "path": roo_cfg,
            "is_active": (roo_disabled is False) if roo_disabled is not None else None,
            "disabled": roo_disabled
        }
    }


def cetak_status_dual_cockpit(hasil: Dict[str, Any]) -> None:
    """[ID]: Mencetak tabel status ringkas kondisi REA MCP di kedua IDE."""
    print("================================================================")
    print("  🔧 SAKLAR DUAL-COCKPIT REA MCP (Reverse Engineer Anything)   ")
    print("================================================================")
    for ide, info in (("Antigravity Global", hasil["antigravity"]), ("Roo Code Workspace", hasil["roo_code"])):
        st = info["is_active"]
        if st is True:
            label = "[AKTIF] (Penuh ~25K Token Tools)"
        elif st is False:
            label = "[NONAKTIF] (HEMAT ~25K TOKEN / PESAN)"
        else:
            label = "[TIDAK TERPASANG]"
        print(f"  • {ide:<22} : {label}")
        print(f"    Berkas: {info['path']}")
    print("================================================================")


def jalankan_rea(perintah: str, target_path: str = "", opsi_tambahan: list[str] | None = None, format_output: str = "json") -> dict | str:
    """[ID]: Menjalankan subperintah CLI REA dan mengembalikan output terstruktur."""
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
    """[ID]: Titik masuk utama CLI REA Helper & Dual-Cockpit Toggle."""
    parser = argparse.ArgumentParser(description="REA Helper & Dual-Cockpit MCP Switcher")
    parser.add_argument("command", nargs="?", default="", help="Subperintah REA (inspect, analyze, doctor, dll.)")
    parser.add_argument("target", nargs="?", default="", help="Path berkas yang akan dianalisis (opsional)")
    parser.add_argument("--status", action="store_true", help="Cek status aktif/nonaktif REA di Antigravity & Roo Code")
    parser.add_argument("--enable", action="store_true", help="Aktifkan REA MCP di Antigravity dan Roo Code serentak")
    parser.add_argument("--disable", action="store_true", help="Nonaktifkan REA MCP (DEFAULT hemat 25K token)")
    parser.add_argument("--target-workspace", dest="ws_target", default="", help="Target folder workspace Roo Code")
    parser.add_argument("--format", choices=["json", "md", "toon", "yaml"], default="json", help="Format keluaran")
    parser.add_argument("--limit-lines", type=int, default=50, help="Batas baris output di terminal (default: 50)")

    args, unknown = parser.parse_known_args()
    ws_path = Path(args.ws_target) if args.ws_target else None

    # Tangani saklar toggle MCP
    if args.status:
        hasil = kelola_status_rea_mcp("status", ws_path)
        cetak_status_dual_cockpit(hasil)
        return
    if args.enable:
        hasil = kelola_status_rea_mcp("enable", ws_path)
        print(">> REA MCP BERHASIL DIAKTIFKAN di kedua IDE.")
        cetak_status_dual_cockpit(hasil)
        return
    if args.disable:
        hasil = kelola_status_rea_mcp("disable", ws_path)
        print(">> REA MCP BERHASIL DINONAKTIFKAN (Kuota 25K token terlindungi).")
        cetak_status_dual_cockpit(hasil)
        return

    if not args.command:
        parser.print_help()
        return

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
