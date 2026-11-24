# -*- coding: utf-8 -*-
"""[ID]: Benchmark live model ':free' OpenRouter untuk format SEARCH/REPLACE, latensi, dan reasoning bloat."""

import argparse, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path

if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROMPT_UJI: str = (
    "Change return 1 to return 2. Reply ONLY with one diff block:\n"
    "<<<<<<< SEARCH\n    return 1\n=======\n    return 2\n>>>>>>> REPLACE\nCode:\ndef f():\n    return 1"
)


def resolve_openrouter_key() -> str:
    """[ID]: Mengambil kunci OpenRouter dari env OPENROUTER_API_KEY atau ~/.gemini/openrouter_key.txt."""
    k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if k and k != "TEMPEL_API_KEY_DISINI":
        return k
    kf = Path.home() / ".gemini" / "openrouter_key.txt"
    if kf.is_file():
        for baris in kf.read_text(encoding="utf-8", errors="replace").splitlines():
            b = baris.strip()
            if b and not b.startswith("#") and b != "TEMPEL_API_KEY_DISINI":
                return b
    return ""


def _req_json(url: str, key: str, payload: dict[str, object] | None = None, timeout: int = 45) -> tuple[int, dict[str, object], str]:
    """[ID]: Mengirim permintaan HTTP JSON via stdlib urllib tanpa membocorkan kunci API."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(raw), raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw), raw
        except Exception:
            return e.code, {}, raw
    except Exception as e:
        return 0, {}, str(e)


def ambil_model_free(api_key: str) -> list[dict[str, object]]:
    """[ID]: Mengambil daftar model aktif berakhiran ':free' dari OpenRouter."""
    status, data, raw = _req_json("https://openrouter.ai/api/v1/models", api_key, timeout=20)
    if status != 200:
        raise RuntimeError(f"Gagal mengambil katalog model (HTTP {status}): {raw[:160]}")
    models = [m for m in (data.get("data") or []) if isinstance(m, dict) and str(m.get("id", "")).endswith(":free")]
    return sorted(models, key=lambda m: (-(int(m.get("context_length") or 0)), str(m.get("id", ""))))


def uji_model(api_key: str, model_id: str, timeout: int = 45) -> dict[str, object]:
    """[ID]: Menguji latensi, status HTTP, reasoning_bloat, dan kepatuhan blok SEARCH/REPLACE."""
    payload: dict[str, object] = {"model": model_id, "messages": [{"role": "user", "content": PROMPT_UJI}], "max_tokens": 400}
    t0 = time.time()
    status, data, raw = _req_json("https://openrouter.ai/api/v1/chat/completions", api_key, payload, timeout=timeout)
    lat = round(time.time() - t0, 2)
    bloat, lolos, galat = False, False, ""
    if status == 200:
        msg = ((data.get("choices") or [{}])[0] or {}).get("message") or {}
        teks = str(msg.get("content") or "")
        bloat = (len(teks.strip()) == 0) and bool(msg.get("reasoning"))
        lolos = (not bloat) and all(t in teks for t in ("<<<<<<< SEARCH", "=======", ">>>>>>> REPLACE", "return 2"))
        if bloat:
            galat = "reasoning_bloat (content kosong)"
    else:
        err = data.get("error") if isinstance(data, dict) else None
        galat = str((err.get("message") if isinstance(err, dict) else raw) or f"HTTP {status}")[:90]
    return {"model": model_id, "latensi_dtk": lat, "status_http": status, "reasoning_bloat": bloat, "lolos_format": lolos, "galat": galat}


def jalankan_bench(maks_model: int = 14, jeda_dtk: float = 3.5) -> list[dict[str, object]]:
    """[ID]: Menjalankan benchmark seluruh model ':free' secara berurutan dengan jeda anti-429."""
    key = resolve_openrouter_key()
    if not key:
        raise RuntimeError("Kunci API OpenRouter tidak ditemukan di env maupun ~/.gemini/openrouter_key.txt")
    kandidat = ambil_model_free(key)[:maks_model]
    hasil: list[dict[str, object]] = []
    print(f"{'Model':<48} | {'HTTP':>4} | {'Dtk':>5} | {'Bloat':<5} | {'Diff':<5} | Catatan")
    print("-" * 105)
    for idx, item in enumerate(kandidat):
        r = uji_model(key, str(item["id"]))
        hasil.append(r)
        print(f"{r['model']:<48} | {r['status_http']:>4} | {r['latensi_dtk']:>5.2f} | {str(r['reasoning_bloat']):<5} | {str(r['lolos_format']):<5} | {r['galat']}")
        if idx + 1 < len(kandidat) and jeda_dtk > 0:
            time.sleep(jeda_dtk)
    return hasil


def main() -> None:
    """[ID]: Titik masuk CLI benchmark model ':free' OpenRouter."""
    p = argparse.ArgumentParser(description="Benchmark live model :free OpenRouter")
    p.add_argument("--maks", type=int, default=14, help="Maksimum jumlah model :free yang diuji")
    p.add_argument("--jeda", type=float, default=3.5, help="Jeda detik antar-request (anti-429)")
    p.add_argument("--json", default="", help="Path opsional untuk menyimpan hasil JSON")
    args = p.parse_args()
    hasil = jalankan_bench(maks_model=args.maks, jeda_dtk=args.jeda)
    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(hasil, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[OK] Hasil benchmark disimpan ke: {out}")


if __name__ == "__main__":
    main()
