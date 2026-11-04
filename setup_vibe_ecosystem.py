"""[ID]: Skrip Otomasi Pemasangan Ekosistem Vibe Coding Universal & Lean (<250 baris).
Memasang aturan .agents, sinkronisasi junction universal skills/rules,
mcp bridge (openrouter & hermes), zoo hybrid dual-cockpit, dan peta AST awal.

[EN]: Universal & Lean Vibe Coding Ecosystem Auto-Setup Script (<250 lines).
Installs .agents rules, universal skills/rules junction sync,
mcp bridges (openrouter & hermes), zoo hybrid dual-cockpit, and initial AST map.
"""

import json
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if BASE_DIR.name == "vibe_tools":
    BASE_DIR = BASE_DIR.parent

VT_DIR = BASE_DIR / "vibe_tools"


def pasang_agents_md() -> None:
    """Memasang atau menggabungkan aturan .agents/AGENTS.md secara non-destruktif."""
    target = BASE_DIR / ".agents" / "AGENTS.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    guardrails = (
        "\n\n---\n\n## Vibe Coding, Token Efficiency & Ponytail Guardrails (Universal)\n"
        "- **Ponytail Threshold (< 250 Lines)**: Never prematurely split files or create single-use classes while target file is < 250 lines. Prefer Python stdlib.\n"
        "- **Clean Architecture Seam (250-300 Lines)**: Split growing logic into dedicated sub-packages using the Facade Pattern.\n"
        "- **Token Efficiency**: Sliced reading (StartLine/EndLine max 100 lines). Prioritize .agents/MAP.md -> grep_search.\n"
        "- **RTK Emulation & CLI Guardrails**: Quiet flags (pip -q, git status -s, pytest -q). Redirect heavy logs to temp logs.\n"
        "- **Direct Unicode Symbols**: Avoid LaTeX math ($...). Use plain text or Unicode (->, *, •).\n"
    )

    if not target.exists():
        target.write_text("# Custom Agent Rules for Workspace\n" + guardrails, encoding="utf-8")
        print("[BUAT] .agents/AGENTS.md")
    else:
        txt = target.read_text(encoding="utf-8")
        if "Ponytail Threshold" not in txt and "Token Efficiency" not in txt:
            target.write_text(txt + guardrails, encoding="utf-8")
            print("[GABUNG] .agents/AGENTS.md (aturan lama dipertahankan, guardrails universal ditambahkan)")
        else:
            print("[LEWATI] .agents/AGENTS.md (aturan guardrails sudah lengkap)")


def sinkronkan_mcp_servers() -> None:
    """Menyalin skrip server MCP dan mengonfigurasi mcp_config.json global."""
    user_home = Path.home()
    gemini_dir = user_home / ".gemini"
    gemini_config_dir = gemini_dir / "config"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    gemini_config_dir.mkdir(parents=True, exist_ok=True)

    # 1. Salin skrip MCP jika ada di vibe_tools
    for s_name in ["openrouter_mcp.py", "hermes_mcp.py", "rea_tool.py"]:
        src = VT_DIR / s_name
        dst = gemini_dir / s_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"[SYNC MCP] {s_name} -> ~/.gemini/")

    # 2. Siapkan openrouter_key.txt jika belum ada
    key_file = gemini_dir / "openrouter_key.txt"
    if not key_file.exists():
        key_file.write_text("TEMPEL_API_KEY_DISINI\n", encoding="utf-8")

    # 3. Konfigurasi mcp_config.json
    mcp_cfg = gemini_config_dir / "mcp_config.json"
    cfg = {"mcpServers": {}}
    if mcp_cfg.exists():
        try:
            cfg = json.loads(mcp_cfg.read_text(encoding="utf-8"))
        except Exception:
            cfg = {"mcpServers": {}}

    py_exe = sys.executable.replace("\\", "/")
    or_script = str(gemini_dir / "openrouter_mcp.py").replace("\\", "/")
    hermes_script = str(gemini_dir / "hermes_mcp.py").replace("\\", "/")

    if "openrouter" not in cfg["mcpServers"]:
        cfg["mcpServers"]["openrouter"] = {"command": py_exe, "args": [or_script]}
    if "hermes_agent" not in cfg["mcpServers"]:
        cfg["mcpServers"]["hermes_agent"] = {"command": py_exe, "args": [hermes_script], "disabled": False}

    mcp_cfg.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    print("[OK] mcp_config.json tersinkronisasi.")


def main() -> None:
    """Menjalankan seluruh pipeline instalasi ekosistem Vibe Coding."""
    print("=" * 65)
    print("  MEMASANG EKOSISTEM VIBE CODING & AGENT CUSTOMIZATION (LEAN)")
    print("=" * 65)
    print(f"Target Direktori: {BASE_DIR}")
    print(f"Python Runtime   : {sys.executable}\n")

    # 1. Konfigurasi Workspace .agents
    pasang_agents_md()

    # 2. Sinkronkan MCP Global
    sinkronkan_mcp_servers()

    # 3. Sinkronisasi Universal Skills & Rules via NTFS Junction ke ~/.gemini/config
    try:
        sys.path.insert(0, str(VT_DIR))
        import sync_universal
        sync_universal.sinkronisasi_universal()
    except Exception as e:
        print(f"[WARNING] sync_universal dilewati: {e}")

    # 4. Sinkronisasi Zoo Code Hybrid Dual-Cockpit
    try:
        import setup_zoo_hybrid
        setup_zoo_hybrid.pasang_zoo_hybrid(target_path=BASE_DIR, setup_ollama=False)
    except Exception:
        try:
            import setup_roo_hybrid
            setup_roo_hybrid.pasang_roo_hybrid(target_path=BASE_DIR, setup_ollama=False)
        except Exception as err:
            print(f"[WARNING] setup_zoo_hybrid dilewati: {err}")

    # 5. Jalankan pemetaan awal .agents/MAP.md
    print("\n[INFO] Membangun/memperbarui peta berkas (.agents/MAP.md)...")
    try:
        import graphify_sync
        r = graphify_sync.perbarui_peta(str(BASE_DIR))
        print(f"[OK] Peta berkas siap ({len(r.get('baru', []))} entri diperbarui).")
    except Exception as e:
        print(f"[WARNING] Peta berkas dilewati: {e}")

    print("\n" + "=" * 65)
    print("  [SELESAI] SELURUH EKOSISTEM VIBE CODING SIAP DIGUNAKAN 100%!")
    print("  (Restart Antigravity IDE atau Zoo Code sekali untuk memuat MCP)")
    print("=" * 65)


if __name__ == "__main__":
    main()
