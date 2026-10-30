"""
[ID]: Modul Penerjemah Docstring Otomatis (Bilingual Docstring Synchronizer).
[EN]: Automatic Docstring Translator Module (Bilingual Docstring Synchronizer).

Membaca berkas Python (.py), mendeteksi docstring Bahasa Indonesia menggunakan AST (Abstract Syntax Tree),
dan menyisipkan padanan Bahasa Inggris ([EN]) secara presisi tanpa merusak logika atau indentasi kode.
"""
import ast
import os
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, Union

# Konfigurasi encoding UTF-8 untuk terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json
import urllib.request
import urllib.error


def _http_post_json(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 20) -> Tuple[int, Dict[str, Any], str]:
    """Helper HTTP POST mandiri menggunakan urllib standard library (0 dependensi eksternal)."""
    data = json.dumps(payload).encode("utf-8")
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


def ambil_semua_api_keys() -> Dict[str, str]:
    """
    [ID]: Mendeteksi dan mengumpulkan semua API key yang tersedia (Gemini dan OpenRouter).
    [EN]: Detects and collects all available API keys (Gemini and OpenRouter).
    
    Returns:
        Dict[str, str]: Dictionary berisi key yang tersedia {'gemini': '...', 'openrouter': '...'}
    """
    keys = {}

    # 1. Cek Gemini API Key (Environment atau ~/.gemini/gemini_key.txt)
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("GOOGLE_API_KEY", "").strip()
    if not gemini_key:
        gemini_file = Path.home() / ".gemini" / "gemini_key.txt"
        if gemini_file.exists():
            try:
                for line in gemini_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and line != "TEMPEL_API_KEY_DISINI":
                        gemini_key = line
                        break
            except Exception:
                pass
    if gemini_key:
        keys["gemini"] = gemini_key

    # 2. Cek OpenRouter API Key (Environment atau ~/.gemini/openrouter_key.txt)
    or_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not or_key or or_key == "TEMPEL_API_KEY_DISINI":
        or_file = Path.home() / ".gemini" / "openrouter_key.txt"
        if or_file.exists():
            try:
                for line in or_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and line != "TEMPEL_API_KEY_DISINI":
                        or_key = line
                        break
            except Exception:
                pass
    if or_key and or_key != "TEMPEL_API_KEY_DISINI":
        keys["openrouter"] = or_key

    return keys


def terjemahkan_ke_inggris(teks_id: str, engine_or_state: Union[str, Dict[str, Any]], api_key: Optional[str] = None) -> Optional[str]:
    """
    [ID]: Menerjemahkan docstring Bahasa Indonesia ke Bahasa Inggris teknis ringkas, mendukung auto-fallback.
    [EN]: Translates Indonesian docstring into concise technical English, supporting auto-fallback.
    """


    # Normalisasi argumen untuk mendukung format lama (engine: str, api_key: str) dan format baru (engine_state: dict)
    if isinstance(engine_or_state, dict):
        engine_state = engine_or_state
    else:
        engine_state = {
            "current": engine_or_state,
            "keys": {engine_or_state: api_key} if api_key else {},
            "allow_fallback": False,
            "delay": 2.0
        }

    current_engine = engine_state.get("current", "gemini")
    keys = engine_state.get("keys", {})
    key = keys.get(current_engine, "")

    if not key:
        print(f"[ERROR] API Key untuk engine '{current_engine}' tidak ditemukan.")
        return None

    prompt_sistem = (
        "You are an expert technical translator for open-source Python codebases.\n"
        "Translate the provided Indonesian docstring into concise, professional, idiomatic English.\n"
        "Strict rules:\n"
        "- Preserve all code identifiers, parameters, types, syntax, and formatting.\n"
        "- Output ONLY the translated English text without quotes, conversational prefixes, or explanations."
    )

    try:
        if current_engine == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": prompt_sistem},
                    {"role": "user", "content": teks_id}
                ],
                "temperature": 0.2
            }
            status_code, data, raw_text = _http_post_json(url, headers=headers, payload=payload, timeout=20)
            if status_code == 200:
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"[ERROR OpenRouter] Status {status_code}: {raw_text[:100]}")
                if engine_state.get("allow_fallback") and "gemini" in keys and status_code in (429, 503):
                    print("      ⚠️ OpenRouter limit/overload. Beralih otomatis (fallback) ke GEMINI...")
                    engine_state["current"] = "gemini"
                    return terjemahkan_ke_inggris(teks_id, engine_state)

        elif current_engine == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {"parts": [{"text": f"{prompt_sistem}\n\nIndonesian text:\n{teks_id}"}]}
                ]
            }
            status_code, data, raw_text = _http_post_json(url, headers=headers, payload=payload, timeout=20)
            if status_code == 200:
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                print(f"[ERROR Gemini] Status {status_code}: {raw_text[:100]}")
                if engine_state.get("allow_fallback") and "openrouter" in keys and status_code in (429, 503):
                    print(f"      ⚠️ Gemini kuota penuh/overload (HTTP {status_code}). Beralih otomatis ke OPENROUTER (DeepSeek)...")
                    engine_state["current"] = "openrouter"
                    return terjemahkan_ke_inggris(teks_id, engine_state)

    except Exception as e:
        print(f"[ERROR Translate] Gagal terhubung ke engine {current_engine}: {e}")
        if engine_state.get("allow_fallback"):
            other_engine = "openrouter" if current_engine == "gemini" else "gemini"
            if other_engine in keys:
                print(f"      ⚠️ Mencoba alihkan ke {other_engine.upper()}...")
                engine_state["current"] = other_engine
                return terjemahkan_ke_inggris(teks_id, engine_state)

    return None


def format_docstring_bilingual(teks_asli: str, teks_en: str) -> str:
    """
    [ID]: Menyusun format dwibahasa [ID] dan [EN].
    [EN]: Assembles bilingual docstring format [ID] and [EN].
    """
    teks_asli_clean = teks_asli.strip()
    teks_en_clean = teks_en.strip()

    # Bersihkan tag [ID] jika sebelumnya sudah ada
    if teks_asli_clean.startswith("[ID]:"):
        teks_asli_clean = teks_asli_clean[5:].strip()

    # Jika teks asli adalah satu baris sederhana
    if "\n" not in teks_asli_clean and "\n" not in teks_en_clean:
        return f"\n[ID]: {teks_asli_clean}\n[EN]: {teks_en_clean}\n"

    # Jika teks multi-baris
    return f"\n[ID]: {teks_asli_clean}\n\n[EN]: {teks_en_clean}\n"


def proses_file_python(
    filepath: Path,
    engine_or_state: Union[str, Dict[str, Any]],
    api_key: Optional[str] = None,
    dry_run: bool = False
) -> int:
    """
    [ID]: Membaca berkas Python, menemukan docstring non-bilingual, dan memperbaruinya.
    [EN]: Reads a Python file, detects non-bilingual docstrings, and updates them.
    
    Returns:
        int: Jumlah docstring yang berhasil diperbarui.
    """
    # Normalisasi engine_state
    if isinstance(engine_or_state, dict):
        engine_state = engine_or_state
    else:
        engine_state = {
            "current": engine_or_state,
            "keys": {engine_or_state: api_key} if api_key else {},
            "allow_fallback": False,
            "delay": 2.0
        }

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[LEWATI] Tidak dapat membaca {filepath}: {e}")
        return 0

    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"[LEWATI] Syntax error pada {filepath}")
        return 0

    target_nodes = []

    # 1. Cek Module Docstring
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        doc = tree.body[0].value.value
        if "[EN]:" not in doc and "[en]:" not in doc.lower():
            target_nodes.append((tree.body[0].value, doc))

    # 2. Cek Function, AsyncFunction, dan Class Docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                doc = node.body[0].value.value
                if "[EN]:" not in doc and "[en]:" not in doc.lower():
                    target_nodes.append((node.body[0].value, doc))

    if not target_nodes:
        return 0

    print(f"\n📄 Memproses: {filepath.name} ({len(target_nodes)} docstring terdeteksi)")
    count = 0

    # Lakukan penggantian teks dari urutan belakang ke depan agar index posisi tetap valid
    modified_content = content
    try:
        for node_const, old_doc in target_nodes:
            print(f"   🔄 Menerjemahkan: '{old_doc.strip()[:40]}...'")
            
            if dry_run:
                print(f"      [DRY-RUN] Melewati translasi aktual.")
                count += 1
                continue

            en_translation = terjemahkan_ke_inggris(old_doc, engine_state)
            if not en_translation:
                print("      ⚠️ Gagal mendapatkan terjemahan, melewati node ini.")
                continue

            new_bilingual_doc = format_docstring_bilingual(old_doc, en_translation)

            # Cari representasi docstring lama di dalam file (triple double quotes atau triple single quotes)
            pattern_d = f'"""{old_doc}"""'
            pattern_s = f"'''{old_doc}'''"

            if pattern_d in modified_content:
                modified_content = modified_content.replace(pattern_d, f'"""{new_bilingual_doc}"""', 1)
                count += 1
                print(f"      ✅ Berhasil disinkronkan ke bilingual!")
            elif pattern_s in modified_content:
                modified_content = modified_content.replace(pattern_s, f"'''{new_bilingual_doc}'''", 1)
                count += 1
                print(f"      ✅ Berhasil disinkronkan ke bilingual!")
            else:
                print("      ⚠️ Tidak dapat memetakan batas kutipan docstring secara presisi.")

            # Throttling jeda untuk menghormati kuota RPM API (terutama Gemini Free Tier 15 RPM)
            if not dry_run:
                if engine_state.get("current") == "gemini":
                    time.sleep(engine_state.get("delay", 2.0))
                else:
                    time.sleep(0.3)
    except KeyboardInterrupt:
        print(f"\n⚠️ Interupsi keyboard (Ctrl+C) terdeteksi saat memproses {filepath.name}.")
        if count > 0 and not dry_run:
            filepath.write_text(modified_content, encoding="utf-8")
            print(f"   💾 [AUTO-SAVE] {count} docstring yang sudah selesai berhasil diselamatkan ke {filepath.name}.")
        raise

    if count > 0 and not dry_run:
        filepath.write_text(modified_content, encoding="utf-8")
        print(f"   💾 {filepath.name} berhasil disimpan.")

    return count


def main():
    parser = argparse.ArgumentParser(
        description="[ID]: Penerjemah Docstring Otomatis (Bilingual Docstring Synchronizer)\n"
                    "[EN]: Automatic Docstring Translator (Bilingual Docstring Synchronizer)"
    )
    parser.add_argument("target", nargs="?", default=".", help="Path berkas .py atau folder target (default: direktori saat ini)")
    parser.add_argument("--dry-run", action="store_true", help="Hanya mengecek docstring tanpa mengubah file fisik")
    parser.add_argument(
        "--engine",
        choices=["auto", "gemini", "openrouter"],
        default="auto",
        help="Pilihan engine translasi: 'auto' (Gemini gratis dengan auto-fallback ke OpenRouter), 'gemini', atau 'openrouter'"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Jeda detik antar panggilan Gemini untuk menghindari kuota 15 RPM (default: 2.0)"
    )
    args = parser.parse_args()

    keys = ambil_semua_api_keys()
    if not keys:
        print("❌ Error: Tidak ditemukan API Key yang valid.")
        print("   Silakan atur salah satu atau kedua API Key berikut:")
        print("   - GEMINI    : ~/.gemini/gemini_key.txt atau GEMINI_API_KEY")
        print("   - OPENROUTER: ~/.gemini/openrouter_key.txt atau OPENROUTER_API_KEY")
        sys.exit(1)

    # Validasi jika pengguna memilih engine tertentu secara manual
    if args.engine == "gemini" and "gemini" not in keys:
        print("❌ Error: Engine 'gemini' dipilih tetapi GEMINI_API_KEY tidak ditemukan!")
        sys.exit(1)
    if args.engine == "openrouter" and "openrouter" not in keys:
        print("❌ Error: Engine 'openrouter' dipilih tetapi OPENROUTER_API_KEY tidak ditemukan!")
        sys.exit(1)

    # Tentukan engine aktif awal dan izin auto-fallback
    if args.engine == "auto":
        current_engine = "gemini" if "gemini" in keys else "openrouter"
        allow_fallback = True
    else:
        current_engine = args.engine
        allow_fallback = False

    engine_state = {
        "current": current_engine,
        "keys": keys,
        "allow_fallback": allow_fallback,
        "delay": args.delay
    }

    fallback_info = " (Auto-fallback ke OpenRouter aktif)" if (allow_fallback and "openrouter" in keys) else ""
    print(f"🚀 Memulai sinkronisasi docstring bilingual...")
    print(f"   - Engine Aktif : {current_engine.upper()}{fallback_info}")
    print(f"   - Kunci Siap   : {', '.join([k.upper() for k in keys.keys()])}")
    print(f"   - Mode         : {'DRY RUN (Pengecekan)' if args.dry_run else 'EKSEKUSI PENUH'}")
    print(f"   - Tips         : Gunakan '--engine openrouter' atau '--engine gemini' untuk gonta-ganti engine secara manual.\n")

    target_path = Path(args.target).resolve()
    py_files = []

    if target_path.is_file() and target_path.suffix == ".py":
        py_files.append(target_path)
    elif target_path.is_dir():
        for p in target_path.rglob("*.py"):
            parts = p.parts
            if any(ign in parts for ign in [".git", "__pycache__", "venv", ".venv", "build", "dist"]):
                continue
            py_files.append(p)

    total_updated = 0
    try:
        for f in py_files:
            total_updated += proses_file_python(f, engine_state, dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print(f"🛑 Dihentikan oleh pengguna (Ctrl+C). Total {total_updated} docstring tersimpan aman.")
        print("=" * 60)
        sys.exit(0)

    print("\n" + "=" * 60)
    print(f"🎉 Selesai! Total {total_updated} docstring berhasil disinkronkan ke bilingual.")
    print("=" * 60)


if __name__ == "__main__":
    main()
