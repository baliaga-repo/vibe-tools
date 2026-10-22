"""
Modul: davinci_timeline_inserter.py
Deskripsi: Skrip CLI & Backend untuk memindai berkas klip video terunduh dan
           memasukkannya ke timeline DaVinci Resolve yang sedang aktif secara berurutan ascending.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Konfigurasi encoding UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Tambahkan path ke cache_chat/davinci_core untuk resolve_bridge
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "cache_chat" / "davinci_core"))

try:
    from resolve_bridge import get_current_timeline_context, get_resolve
except ImportError:
    get_current_timeline_context = None
    get_resolve = None


def natural_sort_key(s: str):
    """Kunci pengurutan natural angka agar 1, 2, ..., 10 terurut benar."""
    name = os.path.basename(s)
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", name)]


def cari_folder_klip_default() -> str:
    """Mencari folder channel yang memuat klip video terunduh."""
    # Cari di folder @Channel
    for d in ROOT_DIR.iterdir():
        if d.is_dir() and d.name.startswith("@"):
            if list(d.glob("*.mp4")) or list(d.glob("*.mov")):
                return str(d)

    renders = ROOT_DIR / "renders"
    if renders.exists() and (list(renders.glob("*.mp4")) or list(renders.glob("*.mov"))):
        return str(renders)

    return str(ROOT_DIR)


def main():
    parser = argparse.ArgumentParser(description="Impor klip video ke DaVinci Resolve berurutan ascending.")
    parser.add_argument("--folder", type=str, default="", help="Folder sumber klip video")
    parser.add_argument("--timeline", type=str, default="VTuber_Clips_Assembly", help="Nama timeline jika dibuat baru")
    args = parser.parse_args()

    folder_target = args.folder or cari_folder_klip_default()
    print("=" * 60)
    print("🎬 DAVINCI TIMELINE CLIP INSERTER")
    print(f"• Folder Sumber  : {folder_target}")
    print(f"• Target Timeline: {args.timeline}")
    print("=" * 60)

    p = Path(folder_target)
    if not p.exists():
        print(f"[ERROR] Folder tidak ditemukan: {folder_target}")
        sys.exit(1)

    video_files = list(p.glob("*.mp4")) + list(p.glob("*.mov"))
    if not video_files:
        print("[WARNING] Tidak ditemukan berkas video (.mp4/.mov) di folder tersebut.")
        sys.exit(0)

    # Urutkan secara natural ascending
    sorted_files = sorted(video_files, key=lambda f: natural_sort_key(f.name))
    print(f"\n[1/3] Ditemukan {len(sorted_files)} berkas klip video:")
    for idx, f in enumerate(sorted_files, start=1):
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"      {idx:02d}. {f.name} ({size_mb:.2f} MB)")

    # 2. Hubungkan ke DaVinci Resolve
    print("\n[2/3] Menghubungkan ke DaVinci Resolve Scripting API...")
    if get_resolve is None:
        print("[ERROR] Modul resolve_bridge tidak tersedia.")
        sys.exit(1)

    resolve = get_resolve()
    if not resolve:
        print("[ERROR] DaVinci Resolve tidak terdeteksi berjalan.")
        print("Pastikan DaVinci Resolve Studio aktif dan External scripting diatur ke 'Local' atau 'Network'.")
        sys.exit(1)

    project_manager, project, current_timeline = get_current_timeline_context(resolve)
    if not project:
        print("[ERROR] Tidak ada project aktif yang sedang terbuka di DaVinci Resolve.")
        sys.exit(1)

    media_pool = project.GetMediaPool()
    if not media_pool:
        print("[ERROR] Gagal mengakses Media Pool DaVinci Resolve.")
        sys.exit(1)

    # 3. Impor & Masukkan ke Timeline
    print("\n[3/3] Mengimpor berkas ke Media Pool dan Timeline...")
    file_paths = [str(f.resolve()) for f in sorted_files]
    imported_items = media_pool.ImportMedia(file_paths)
    if not imported_items:
        print("[ERROR] DaVinci Resolve gagal mengimpor berkas klip video ke Media Pool.")
        sys.exit(1)

    # Petakan kembali agar urutan tetap natural ascending
    item_map = {}
    for it in imported_items:
        try:
            prop_path = it.GetClipProperty("File Path") or ""
            if prop_path:
                item_map[str(Path(prop_path).resolve())] = it
        except Exception:
            pass

    ordered_items = []
    for fp in file_paths:
        resolved_fp = str(Path(fp).resolve())
        if resolved_fp in item_map:
            ordered_items.append(item_map[resolved_fp])

    final_items = ordered_items if len(ordered_items) == len(imported_items) else imported_items

    if not current_timeline:
        print(f"      Membuat timeline baru: '{args.timeline}'...")
        current_timeline = media_pool.CreateEmptyTimeline(args.timeline)

    success = media_pool.AppendToTimeline(final_items)
    try:
        resolve.OpenPage("edit")
    except Exception:
        pass

    if success:
        print(f"✨ SUKSES! Sebanyak {len(final_items)} klip berhasil disusun ke timeline DaVinci Resolve secara ascending.")
    else:
        print(f"[WARNING] MediaPool.AppendToTimeline selesai (status return: {success}). Periksa timeline DaVinci Resolve.")

    print("=" * 60)


if __name__ == "__main__":
    main()
