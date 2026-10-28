"""
[ID]: Modul Ekstraktor Pengetahuan & Pembaruan Panduan Berbasis Database Antigravity IDE (doc_db_extractor.py).
Mengekstrak intisari sesi percakapan kemarin dan hari ini dari tabel SQLite turn_cache_v2 (monitor_cache.db),
menyaring topik yang relevan dengan ekosistem vibe_tools, .agents, skills, rules, dan MCP,
serta memetakannya secara deterministik ke bab-bab target di PANDUAN_LENGKAP_EKOSISTEM.md.

[EN]: Knowledge Extractor & Ecosystem Guide Updater from Antigravity IDE Database (doc_db_extractor.py).
Extracts session insights from yesterday and today from SQLite table turn_cache_v2 (monitor_cache.db),
filters topics relevant to vibe_tools, .agents, skills, rules, and MCP,
and maps them deterministically to target chapters in PANDUAN_LENGKAP_EKOSISTEM.md.
"""

import os
import sys
import json
import sqlite3
import datetime
from typing import List, Dict, Any, Optional

DEFAULT_DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "monitor", "monitor_cache.db")
)

RELEVANT_KEYWORDS = [
    "vibe_tools", ".agents", "skill", "rule", "mcp", "grill-me", "ask-matt",
    "gemini", "openrouter", "hermes", "rea", "docstring", "panduan",
    "argon", "flash", "sonnet", "deepseek", "r1", "pipeline", "syntax gate",
    "agent-security", "cookie", "to-tickets", "to-spec", "diagnosing-bugs"
]

def format_wita_time(utc_str: str) -> str:
    """
    [ID]: Konversi string timestamp ISO UTC menjadi string waktu lokal (WITA UTC+8).
    [EN]: Convert ISO UTC timestamp string to local time string (WITA UTC+8).
    """
    if not utc_str:
        return ""
    try:
        clean = utc_str.replace("Z", "+00:00")
        dt_utc = datetime.datetime.fromisoformat(clean)
        dt_wita = dt_utc + datetime.timedelta(hours=8)
        return dt_wita.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return utc_str

def extract_recent_knowledge(
    db_path: str = DEFAULT_DB_PATH,
    days: int = 2,
    custom_keywords: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    [ID]: Mengambil dan menyaring percakapan dari SQLite turn_cache_v2 dalam N hari terakhir.
    [EN]: Retrieve and filter conversations from SQLite turn_cache_v2 within the last N days.
    """
    if not os.path.exists(db_path):
        return {"error": f"Database tidak ditemukan di {db_path}", "sessions": []}

    keywords = [k.lower() for k in (custom_keywords or RELEVANT_KEYWORDS)]
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    cutoff_dt = now_utc - datetime.timedelta(days=days)
    cutoff_str = cutoff_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cursor = conn.cursor()

    query = """
        SELECT conversation_id, step_index, timestamp, model_name,
               prompt_text, response_text, worked_summary_json
        FROM turn_cache_v2
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """
    cursor.execute(query, (cutoff_str,))
    rows = cursor.fetchall()
    conn.close()

    sessions: Dict[str, List[Dict[str, Any]]] = {}
    matched_count = 0

    for cid, step, ts, model, prompt, response, worked_json in rows:
        p_text = (prompt or "").strip()
        r_text = (response or "").strip()
        combined_text = f"{p_text}\n{r_text}".lower()

        # Filter relevansi: harus mengandung minimal satu kata kunci ekosistem
        is_relevant = any(kw in combined_text for kw in keywords)
        if not is_relevant:
            continue

        matched_count += 1
        worked_dict = {}
        if worked_json:
            try:
                worked_dict = json.loads(worked_json)
            except Exception:
                pass

        if cid not in sessions:
            sessions[cid] = []

        sessions[cid].append({
            "step_index": step,
            "timestamp_wita": format_wita_time(ts),
            "model": model or "Unknown",
            "prompt_snippet": p_text[:250].replace("\r", " ").replace("\n", " "),
            "response_snippet": r_text[:300].replace("\r", " ").replace("\n", " "),
            "commands": worked_dict.get("commands", []),
            "edited_files": worked_dict.get("edited", []),
            "explored_files": worked_dict.get("explored", []),
        })

    return {
        "cutoff_utc": cutoff_str,
        "total_matched_turns": matched_count,
        "total_sessions": len(sessions),
        "sessions": sessions
    }

def generate_markdown_digest(data: Dict[str, Any]) -> str:
    """
    [ID]: Menghasilkan draf ringkasan Markdown padat untuk panduan pembaruan dokumen.
    [EN]: Generate a dense Markdown digest draft for document update guidance.
    """
    lines = [
        "# 📑 Ringkasan Pembaruan Pengetahuan dari Database Antigravity IDE",
        f"**Waktu Potong Data:** >= `{data.get('cutoff_utc', '')}` | **Total Turn Relevan:** `{data.get('total_matched_turns', 0)}`",
        "---",
        ""
    ]

    sessions = data.get("sessions", {})
    if not sessions:
        lines.append("*Tidak ditemukan percakapan relevan yang cocok dengan kriteria filter.*")
        return "\n".join(lines)

    for cid, turns in sessions.items():
        first_t = turns[0]
        last_t = turns[-1]
        lines.append(f"### 💬 Sesi `{cid[:8]}...` ({first_t['timestamp_wita']} s/d {last_t['timestamp_wita']})")
        lines.append(f"- **Model Aktif:** {last_t['model']}")
        
        all_edited = set()
        for t in turns:
            all_edited.update(t.get("edited_files", []))
        if all_edited:
            lines.append(f"- **Berkas Diubah:** {', '.join([f'`{os.path.basename(f)}`' for f in sorted(list(all_edited))])}")

        lines.append("- **Sorotan Percakapan Penting:**")
        for t in turns:
            # Ambil prompt yang memiliki instruksi substantif
            p = t["prompt_snippet"]
            if any(k in p.lower() for k in ["/grill", "/implement", "spec", "cookie", "gemini", "db", "argon"]):
                lines.append(f"  * [#{t['step_index']}] `{p[:130]}...`")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    days_arg = 2
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        days_arg = int(sys.argv[1])
    
    extracted = extract_recent_knowledge(days=days_arg)
    print(f"[Extractor] Selesai: {extracted.get('total_matched_turns', 0)} turn dari {extracted.get('total_sessions', 0)} sesi.")
    md_output = generate_markdown_digest(extracted)
    
    out_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scratch"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "recent_db_knowledge.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md_output)
    print(f"[Extractor] Hasil tersimpan di: {out_file}")
