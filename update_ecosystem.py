# -*- coding: utf-8 -*-
"""
[ID]: Universal Ecosystem Updater & Standarisasi Dual-Cockpit (Antigravity + Roo Code).
Memperbarui konfigurasi ekosistem AI (.agents, .roomodes, .roo) secara non-destruktif
lintas proyek melalui Remote GitHub maupun dorongan Master Lokal (--target).
"""

import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys
import urllib.request
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class UpdateStatus(Enum):
    """[ID]: Status perbandingan berkas antara sumber dan target."""
    UP_TO_DATE = "UP_TO_DATE"
    OUTDATED = "OUTDATED"
    LOCAL_MODIFIED = "LOCAL_MODIFIED"
    NEW_FILE = "NEW_FILE"
    PROTECTED_PROJECT_FILE = "PROTECTED_PROJECT_FILE"


@dataclass
class FileDiffManifest:
    """[ID]: Manifest status berkas ekosistem."""
    relative_path: Path
    status: UpdateStatus
    source_hash: str
    local_hash: Optional[str]
    is_protected: bool


class VibeEcosystemUpdater:
    """[ID]: Orkestrator pembaruan Dual-Cockpit (Antigravity .agents + Roo Code .roo)."""

    GITHUB_TREE_API: str = "https://api.github.com/repos/baliaga-repo/vibe-tools/git/trees/main?recursive=1"
    STRICT_BLACKLIST: Tuple[str, ...] = (
        ".env", "cookies", "openrouter_key.txt", ".git", "__pycache__",
        ".pytest_cache", "graphify-out", "node_modules", "build", "dist"
    )
    MANAGED_DIRS: Tuple[str, ...] = ("vibe_tools", ".agents", ".roomodes", ".roo", ".zoomodes", ".zoo")

    def __init__(self, target_root: Optional[Path] = None, source_dir: Optional[Path] = None):
        self.target_root: Path = (target_root or Path.cwd()).resolve()
        vibe_dir = Path(__file__).resolve().parent
        self.source_vibe_dir: Path = (source_dir or vibe_dir).resolve()
        self.backup_dir: Path = self.target_root / ".agents" / "backups"

    @staticmethod
    def hitung_sha256(file_path: Path) -> str:
        """[ID]: Menghitung SHA256 berkas dengan normalisasi LF."""
        try:
            konten = file_path.read_bytes().replace(b"\r\n", b"\n")
            return hashlib.sha256(konten).hexdigest()
        except Exception:
            return ""

    def is_blacklisted(self, rel_path: Path) -> bool:
        """[ID]: Memeriksa blacklist (kode produksi, rahasia, cache)."""
        rel_posix = rel_path.as_posix()
        if any(pat in rel_posix for pat in self.STRICT_BLACKLIST):
            return True
        if rel_path.suffix == ".py" and not rel_posix.startswith("vibe_tools/"):
            return True
        if rel_path.parts and rel_path.parts[0] in ("core", "gui", "tests", "docs", "locales"):
            return True
        return False

    def is_strictly_protected(self, rel_path: Path) -> bool:
        """[ID]: Memeriksa proteksi berkas kustom pengguna."""
        return "99-project-custom.md" in rel_path.as_posix()

    def build_local_manifest(self) -> Dict[str, str]:
        """[ID]: Membangun manifest dari folder master lokal."""
        manifest: Dict[str, str] = {}
        s_root = self.source_vibe_dir.parent if self.source_vibe_dir.name == "vibe_tools" else self.source_vibe_dir
        for d in self.MANAGED_DIRS:
            target = s_root / d
            if not target.exists():
                continue
            if target.is_file():
                manifest[d] = self.hitung_sha256(target)
            else:
                for f in target.rglob("*"):
                    if f.is_file():
                        rel = f.relative_to(s_root)
                        if not self.is_blacklisted(rel):
                            manifest[rel.as_posix()] = self.hitung_sha256(f)
        return manifest

    def fetch_remote_manifest(self) -> Dict[str, str]:
        """[ID]: Mengambil manifest dari branch main GitHub."""
        manifest: Dict[str, str] = {}
        try:
            req = urllib.request.Request(self.GITHUB_TREE_API, headers={"User-Agent": "Vibe-Tools/2.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("tree", []):
                    if item.get("type") == "blob":
                        p = item.get("path", "")
                        if any(p.startswith(d) for d in self.MANAGED_DIRS) and not self.is_blacklisted(Path(p)):
                            manifest[p] = item.get("sha", "")
        except Exception as e:
            print(f"[PERINGATAN] Gagal ke GitHub API ({e}), beralih ke manifest lokal.")
            return self.build_local_manifest()
        return manifest

    def analyze_workspace(self, source_manifest: Dict[str, str]) -> List[FileDiffManifest]:
        """[ID]: Membandingkan berkas target terhadap manifest sumber."""
        diffs: List[FileDiffManifest] = []
        for rel_posix, src_hash in source_manifest.items():
            rel_path = Path(rel_posix)
            if self.is_blacklisted(rel_path):
                continue
            loc_file = self.target_root / rel_path
            is_prot = self.is_strictly_protected(rel_path)
            if not loc_file.exists():
                diffs.append(FileDiffManifest(rel_path, UpdateStatus.NEW_FILE, src_hash, None, is_prot))
            else:
                loc_hash = self.hitung_sha256(loc_file)
                st = UpdateStatus.PROTECTED_PROJECT_FILE if is_prot else (
                    UpdateStatus.UP_TO_DATE if loc_hash == src_hash else UpdateStatus.OUTDATED
                )
                diffs.append(FileDiffManifest(rel_path, st, src_hash, loc_hash, is_prot))
        return diffs

    def smart_merge_agents_md(self, local_content: str, new_content: str) -> str:
        """[ID]: Menggabungkan guardrails universal ke .agents/AGENTS.md tanpa menghapus aturan proyek."""
        if not local_content.strip():
            return new_content
        marker = "## Project Specific Rules"
        if marker in local_content:
            return f"{new_content.strip()}\n\n{marker}{local_content.split(marker, 1)[1]}"
        if local_content.strip() != new_content.strip() and "# Custom Agent Rules" in local_content:
            return f"{new_content.strip()}\n\n{marker} (Dipertahankan Otomatis):\n{local_content.strip()}"
        return new_content

    def create_pre_update_backup(self, files_to_update: List[Path]) -> Optional[Path]:
        """[ID]: Mencadangkan berkas ke .agents/backups/backup_YYYYMMDD_HHMMSS/."""
        if not files_to_update:
            return None
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target_backup = self.backup_dir / f"backup_{ts}"
        target_backup.mkdir(parents=True, exist_ok=True)
        for rel in files_to_update:
            src = self.target_root / rel
            if src.is_file():
                dest = target_backup / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
        return target_backup

    def rollback_backup(self, backup_name: Optional[str] = None) -> bool:
        """[ID]: Memulihkan snapshot berkas dari folder backup."""
        if not self.backup_dir.exists():
            print("[INFO] Folder backup tidak ditemukan.")
            return False
        backups = sorted([d for d in self.backup_dir.iterdir() if d.is_dir()], reverse=True)
        if not backups:
            print("[INFO] Tidak ada snapshot backup tersedia.")
            return False
        selected = (self.backup_dir / backup_name) if backup_name and (self.backup_dir / backup_name).exists() else backups[0]
        print(f">> Melakukan Rollback dari snapshot: {selected.name}")
        for f in selected.rglob("*"):
            if f.is_file():
                dest = self.target_root / f.relative_to(selected)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                print(f"  [RESTORE] {f.relative_to(selected).as_posix()}")
        print(">> Rollback selesai dengan sukses.")
        return True

    def sync_roo_hybrid_cockpit(self, setup_ollama: bool = False) -> None:
        """[ID]: Memperbarui konfigurasi Zoo Code / Roo Code via setup_zoo_hybrid.py."""
        try:
            from vibe_tools.setup_zoo_hybrid import pasang_zoo_hybrid
            pasang_zoo_hybrid(target_path=str(self.target_root), setup_ollama=setup_ollama)
        except Exception as e:
            print(f"[PERINGATAN] Gagal sinkronisasi Zoo Code / Roo Code Hybrid: {e}")

    def apply_updates(self, diffs: List[FileDiffManifest], dry_run: bool = False, setup_ollama: bool = False) -> bool:
        """[ID]: Menerapkan pembaruan berkas, backup otomatis, dan sinkronisasi kokpit."""
        to_up = [d.relative_path for d in diffs if d.status in (UpdateStatus.OUTDATED, UpdateStatus.NEW_FILE) and not d.is_protected]
        if not to_up and not any(d.is_protected for d in diffs):
            print(">> Seluruh komponen ekosistem sudah versi terbaru (UP TO DATE).")
            return True

        print(f">> Analisis: {len(to_up)} berkas perlu diperbarui:")
        for d in diffs:
            if d.is_protected:
                print(f"  [DILINDUNGI] {d.relative_path.as_posix()} (aturan kustom aman)")
            elif d.status in (UpdateStatus.OUTDATED, UpdateStatus.NEW_FILE):
                tag = "[BARU]" if d.status == UpdateStatus.NEW_FILE else "[UPDATE]"
                print(f"  {tag:<10} {d.relative_path.as_posix()}")

        if dry_run:
            print("[DRY RUN] Mode simulasi selesai. Tidak ada berkas yang diubah.")
            return True

        b_path = self.create_pre_update_backup(to_up)
        if b_path:
            print(f">> Backup pra-update disimpan di: {b_path.name}")

        s_root = self.source_vibe_dir.parent if self.source_vibe_dir.name == "vibe_tools" else self.source_vibe_dir
        for rel in to_up:
            src = s_root / rel
            dest = self.target_root / rel
            if not src.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            if rel.as_posix() == ".agents/AGENTS.md" and dest.exists():
                dest.write_text(self.smart_merge_agents_md(dest.read_text(encoding="utf-8"), src.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
            else:
                shutil.copy2(src, dest)

        self.sync_roo_hybrid_cockpit(setup_ollama=setup_ollama)
        return True


def main():
    """[ID]: Titik masuk CLI Universal Updater Dual-Cockpit."""
    parser = argparse.ArgumentParser(description="Vibe Tools Universal Updater (Dual-Cockpit)")
    parser.add_argument("--check", action="store_true", help="Pengecekan versi tanpa modifikasi")
    parser.add_argument("--dry-run", action="store_true", help="Simulasi pembaruan tanpa menyentuh disk")
    parser.add_argument("--target", default="", help="Path direktori proyek tujuan (Offline Push)")
    parser.add_argument("--setup-ollama", action="store_true", help="Setup model lokal Ollama RTX 3060")
    parser.add_argument("--rollback", nargs="?", const="", help="Pulihkan konfigurasi dari backup")

    args = parser.parse_args()
    target = Path(args.target).resolve() if args.target else Path.cwd().resolve()
    updater = VibeEcosystemUpdater(target_root=target)

    if args.rollback is not None:
        updater.rollback_backup(args.rollback or None)
        return

    diffs = updater.analyze_workspace(updater.build_local_manifest())
    updater.apply_updates(diffs, dry_run=(args.check or args.dry_run), setup_ollama=args.setup_ollama)


if __name__ == "__main__":
    main()

