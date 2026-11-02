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
from typing import Any, List, Optional, Tuple, Union

# Konfigurasi encoding UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Tambahkan path ke cache_chat/davinci_core untuk resolve_bridge
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "cache_chat" / "davinci_core"))

try:
    # pyrefly: ignore[missing-import]
    from resolve_bridge import (
        ensure_snap_captions_bin,
        ensure_subfolder,
        get_current_timeline_context,
        get_next_timeline_name,
        get_resolve,
    )
except ImportError:
    get_current_timeline_context = None
    get_resolve = None
    ensure_subfolder = None
    ensure_snap_captions_bin = None
    get_next_timeline_name = None


def natural_sort_key(s: str) -> List[Union[int, str]]:
    """Kunci pengurutan natural angka agar 1, 2, ..., 10 terurut benar."""
    name = os.path.basename(s)
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", name)]


def get_clip_channel_label(file_path: Union[str, Path], base_folder: Union[str, Path, None] = None) -> str:
    """
    Mengembalikan label nama channel/subfolder asal berkas klip (misal '@KoboKanaeru').
    Jika berkas berada langsung di folder non-'@', mengembalikan nama folder induknya.
    """
    p = Path(file_path)
    parent_name = p.parent.name
    if parent_name.startswith("@"):
        return parent_name
    if base_folder:
        base_name = Path(base_folder).name
        if base_name.startswith("@"):
            return base_name
    return parent_name


def scan_clip_files(folder_path: Union[str, Path]) -> List[Path]:
    """
    Memindai berkas video (.mp4 dan .mov) di permukaan folder_path serta
    di dalam subfolder langsung (1-level) yang namanya diawali '@'.
    Hasil diurutkan berdasarkan Nomor Klip Global (natural_sort_key(f.name)),
    dengan tie-breaker nama folder induk (natural_sort_key(f.parent.name)).
    """
    p = Path(folder_path)
    if not p.exists() or not p.is_dir():
        return []

    collected_files: List[Path] = []
    seen_paths = set()

    # 1. Berkas langsung di permukaan folder
    for f in list(p.glob("*.mp4")) + list(p.glob("*.mov")):
        res = f.resolve()
        if res not in seen_paths:
            seen_paths.add(res)
            collected_files.append(f)

    # 2. Subfolder 1-level yang diawali '@'
    for sub in p.iterdir():
        if sub.is_dir() and sub.name.startswith("@"):
            for f in list(sub.glob("*.mp4")) + list(sub.glob("*.mov")):
                res = f.resolve()
                if res not in seen_paths:
                    seen_paths.add(res)
                    collected_files.append(f)

    # Urutkan secara natural ascending (Nomor klip global, lalu nama channel)
    return sorted(
        collected_files,
        key=lambda f: (natural_sort_key(f.name), natural_sort_key(f.parent.name))
    )


def cari_folder_klip_default() -> str:
    """Mencari folder channel atau root yang memuat klip video terunduh."""
    # Prioritaskan ROOT_DIR jika memuat klip (langsung atau via subfolder @)
    if scan_clip_files(ROOT_DIR):
        return str(ROOT_DIR)

    renders = ROOT_DIR / "renders"
    if renders.exists() and scan_clip_files(renders):
        return str(renders)

    for d in ROOT_DIR.iterdir():
        if d.is_dir() and d.name.startswith("@"):
            if scan_clip_files(d):
                return str(d)

    return str(ROOT_DIR)


def import_and_assemble_clips(
    resolve: Any,
    file_paths: List[str],
    timeline_prefix: str = "Timeline"
) -> Tuple[bool, str]:
    """
    Orkestrator terpusat untuk mengorganisasikan Bin dan menyusun klip ke Timeline:
    1. Memastikan bin 'Snap Captions' ada di Master Bin via ensure_snap_captions_bin().
    2. Memastikan bin 'Video' ada di Master Bin, mengaktifkannya, dan mengimpor klip baru
       tanpa menduplikasi klip yang sudah ada di dalam bin 'Video'.
    3. Memastikan bin 'Timeline' ada di Master Bin, mengaktifkannya, dan membuat timeline baru
       bernama 'Timeline N' (get_next_timeline_name).
    4. Memasukkan klip secara berurutan (AppendToTimeline) ke timeline baru tersebut.
    5. Mengembalikan folder aktif Media Pool ke Master Bin (root_folder) dan membuka halaman 'edit'.
    """
    if not resolve:
        return False, "DaVinci Resolve tidak aktif."

    if not file_paths:
        return False, "Tidak ada berkas klip video untuk diimpor."

    project_manager, project, _ = (
        get_current_timeline_context(resolve)
        if get_current_timeline_context
        else (None, None, None)
    )
    if not project:
        return False, "Tidak ada project aktif yang sedang terbuka di DaVinci Resolve."

    media_pool = project.GetMediaPool()
    if not media_pool:
        return False, "Gagal mengakses Media Pool DaVinci Resolve."

    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        return False, "Gagal mengakses Master Bin DaVinci Resolve."

    # 1. Pastikan bin 'Snap Captions' tersedia di Master Bin
    if ensure_snap_captions_bin:
        ensure_snap_captions_bin(media_pool, str(ROOT_DIR))

    # 2. Pastikan bin 'Video' tersedia di Master Bin & aktifkan
    video_bin = (
        ensure_subfolder(media_pool, root_folder, "Video")
        if ensure_subfolder
        else root_folder
    )
    target_video_folder = video_bin or root_folder
    if hasattr(media_pool, "SetCurrentFolder"):
        media_pool.SetCurrentFolder(target_video_folder)

    # 3. Cek item klip yang sudah ada di dalam bin 'Video' (anti-duplikasi)
    existing_paths = set()
    clip_map = {}
    for clip in (target_video_folder.GetClipList() or []):
        try:
            p_str = clip.GetClipProperty("File Path") or ""
            if p_str:
                norm_p = str(Path(p_str).resolve())
                existing_paths.add(norm_p)
                clip_map[norm_p] = clip
        except Exception:
            pass

    # Impor hanya file yang belum ada di bin 'Video'
    missing_paths = [p for p in file_paths if str(Path(p).resolve()) not in existing_paths]
    if missing_paths and hasattr(media_pool, "ImportMedia"):
        imported = media_pool.ImportMedia(missing_paths) or []
        for it in imported:
            try:
                p_str = it.GetClipProperty("File Path") or ""
                if p_str:
                    clip_map[str(Path(p_str).resolve())] = it
            except Exception:
                pass

    # Susun ordered_items persis sesuai urutan file_paths
    ordered_items = []
    for fp in file_paths:
        norm_fp = str(Path(fp).resolve())
        if norm_fp in clip_map:
            ordered_items.append(clip_map[norm_fp])

    if not ordered_items:
        return False, "Gagal menyiapkan klip video di Media Pool."

    # 4. Pastikan bin 'Timeline' tersedia di Master Bin & aktifkan
    timeline_bin = (
        ensure_subfolder(media_pool, root_folder, "Timeline")
        if ensure_subfolder
        else root_folder
    )
    target_timeline_folder = timeline_bin or root_folder
    if hasattr(media_pool, "SetCurrentFolder"):
        media_pool.SetCurrentFolder(target_timeline_folder)

    # Buat timeline baru sekuensial ('Timeline 1', 'Timeline 2', dst.)
    new_timeline_name = (
        get_next_timeline_name(project, timeline_prefix)
        if get_next_timeline_name
        else f"{timeline_prefix} 1"
    )
    new_timeline = media_pool.CreateEmptyTimeline(new_timeline_name)
    if not new_timeline:
        return False, f"Gagal membuat timeline baru '{new_timeline_name}'."

    # 5. Susun klip ke timeline baru
    success = media_pool.AppendToTimeline(ordered_items)

    # 6. Kembalikan folder aktif ke Master Bin dan buka halaman Edit
    try:
        if hasattr(media_pool, "SetCurrentFolder"):
            media_pool.SetCurrentFolder(root_folder)
        if hasattr(resolve, "OpenPage"):
            resolve.OpenPage("edit")
    except Exception:
        pass

    msg = f"Berhasil memasukkan {len(ordered_items)} klip ke '{new_timeline_name}' di dalam bin 'Timeline'!"
    return bool(success), msg


def main():
    parser = argparse.ArgumentParser(description="Impor klip video ke DaVinci Resolve berurutan ascending.")
    parser.add_argument("--folder", type=str, default="", help="Folder sumber klip video")
    parser.add_argument("--timeline", type=str, default="Timeline", help="Prefix nama timeline jika dibuat baru (misal: Timeline)")
    args = parser.parse_args()

    folder_target = args.folder or cari_folder_klip_default()
    print("=" * 60)
    print("🎬 DAVINCI TIMELINE CLIP INSERTER")
    print(f"• Folder Sumber  : {folder_target}")
    print(f"• Target Timeline: {args.timeline} 1..N")
    print("=" * 60)

    p = Path(folder_target)
    if not p.exists():
        print(f"[ERROR] Folder tidak ditemukan: {folder_target}")
        sys.exit(1)

    sorted_files = scan_clip_files(p)
    if not sorted_files:
        print("[WARNING] Tidak ditemukan berkas video (.mp4/.mov) di folder tersebut.")
        sys.exit(0)

    print(f"\n[1/3] Ditemukan {len(sorted_files)} berkas klip video:")
    for idx, f in enumerate(sorted_files, start=1):
        channel_label = get_clip_channel_label(f, p)
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"      {idx:02d}. [{channel_label}] {f.name} ({size_mb:.2f} MB)")

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

    # 3. Impor & Masukkan ke Timeline
    print("\n[3/3] Mengorganisasi Bin ('Video', 'Timeline', 'Snap Captions') dan menyusun klip...")
    file_paths = [str(f.resolve()) for f in sorted_files]
    success, msg = import_and_assemble_clips(resolve, file_paths, timeline_prefix=args.timeline)

    if success:
        print(f"✨ SUKSES! {msg}")
    else:
        print(f"[WARNING] {msg}")

    print("=" * 60)


if __name__ == "__main__":
    main()
