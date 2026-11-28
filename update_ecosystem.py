# -*- coding: utf-8 -*-
"""[ID]: Universal Ecosystem Updater Vibe Tools (Antigravity + Aider + MCP).
Memasang & memperbarui isi vibe_tools terbaru (skills, rules, references, templates,
workflows, mcp_schemas, skrip MCP/CLI) via Git Pull, GitHub API (--remote), atau --target."""

import argparse, datetime, hashlib, importlib.util, json, shutil, subprocess, sys, urllib.request
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
    UP_TO_DATE, OUTDATED, LOCAL_MODIFIED = "UP_TO_DATE", "OUTDATED", "LOCAL_MODIFIED"
    NEW_FILE, PROTECTED_PROJECT_FILE = "NEW_FILE", "PROTECTED_PROJECT_FILE"

@dataclass
class FileDiffManifest:
    """[ID]: Manifest status berkas ekosistem."""
    relative_path: Path
    status: UpdateStatus
    source_hash: str
    local_hash: Optional[str]
    is_protected: bool


class VibeEcosystemUpdater:
    """[ID]: Orkestrator pemasangan & pembaruan ekosistem (Antigravity + Aider + MCP)."""

    GITHUB_TREE_API: str = "https://api.github.com/repos/baliaga-repo/vibe-tools/git/trees/main?recursive=1"
    GITHUB_RAW_BASE: str = "https://raw.githubusercontent.com/baliaga-repo/vibe-tools/main/"
    STRICT_BLACKLIST: Tuple[str, ...] = (
        ".env", "cookies", "openrouter_key.txt", ".git", "__pycache__", ".pytest_cache",
        "graphify-out", "node_modules", "build", "dist", "desktop.ini", ".pyc",
        ".agents/backups", ".agents/MAP.md", ".agents/hooks", ".agents/skills", ".github/",
    )
    LEGACY_OBSOLETE_PATHS: Tuple[str, ...] = (
        "vibe_tools/setup_roo_hybrid.py", "vibe_tools/PANDUAN_ZOO_CODE_HYBRID.md", "vibe_tools/roo_hybrid",
    )
    MANAGED_DIRS: Tuple[str, ...] = ("vibe_tools", ".agents")

    def __init__(self, target_root: Optional[Path] = None, source_dir: Optional[Path] = None):
        self.target_root: Path = (target_root or Path.cwd()).resolve()
        self.source_vibe_dir: Path = (source_dir or Path(__file__).resolve().parent).resolve()
        self.backup_dir: Path = self.target_root / ".agents" / "backups"
        self._source_map: Dict[str, Path] = {}
        self._remote_urls: Dict[str, str] = {}

    @staticmethod
    def hitung_sha256(file_path: Path) -> str:
        """[ID]: Menghitung SHA256 berkas dengan normalisasi LF."""
        try: return hashlib.sha256(file_path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        except Exception: return ""

    @staticmethod
    def hitung_git_blob_sha1(file_path: Path, normalisasi_lf: bool = False) -> str:
        """[ID]: Menghitung Git Blob SHA-1 lokal untuk perbandingan manifest GitHub."""
        try:
            data = file_path.read_bytes().replace(b"\r\n", b"\n") if normalisasi_lf else file_path.read_bytes()
            return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()
        except Exception: return ""

    def is_blacklisted(self, rel_path: Path) -> bool:
        """[ID]: Memeriksa blacklist (kode produksi, rahasia, cache, aset spesifik proyek)."""
        rel_posix = rel_path.as_posix()
        if any(pat in rel_posix for pat in self.STRICT_BLACKLIST): return True
        if rel_path.suffix == ".py" and not rel_posix.startswith("vibe_tools/"): return True
        return bool(rel_path.parts and rel_path.parts[0] in ("core", "gui", "tests", "docs", "locales"))

    def is_strictly_protected(self, rel_path: Path) -> bool:
        """[ID]: Memeriksa proteksi berkas kustom pengguna."""
        return "99-project-custom.md" in rel_path.as_posix()

    def _catat_entri(self, manifest: Dict[str, str], rel_in_vibe: Path, digest: str, src_lokal: Optional[Path] = None, url: Optional[str] = None) -> None:
        """[ID]: Mendaftarkan berkas vibe_tools serta pemetaan workflow universal ke .agents/workflows/."""
        kandidat = [Path("vibe_tools") / rel_in_vibe]
        if len(rel_in_vibe.parts) >= 2 and rel_in_vibe.parts[0] == "workflows":
            kandidat.append(Path(".agents") / rel_in_vibe)
        for rel_t in kandidat:
            if not self.is_blacklisted(rel_t):
                key = rel_t.as_posix()
                manifest[key] = digest
                if src_lokal is not None:
                    self._source_map[key] = src_lokal
                if url is not None:
                    self._remote_urls[key] = url

    def build_local_manifest(self) -> Dict[str, str]:
        """[ID]: Membangun manifest lengkap isi vibe_tools terbaru & workflow universal lokal."""
        manifest: Dict[str, str] = {}
        self._source_map.clear(); self._remote_urls.clear()
        if self.source_vibe_dir.exists():
            for f in sorted(self.source_vibe_dir.rglob("*")):
                if f.is_file(): self._catat_entri(manifest, f.relative_to(self.source_vibe_dir), self.hitung_sha256(f), src_lokal=f)
        return manifest

    def build_remote_manifest(self) -> Dict[str, str]:
        """[ID]: Menarik manifest seluruh berkas vibe_tools terbaru langsung dari GitHub API."""
        manifest: Dict[str, str] = {}
        self._source_map.clear(); self._remote_urls.clear()
        with urllib.request.urlopen(urllib.request.Request(self.GITHUB_TREE_API, headers={"User-Agent": "vibe-tools-updater"}), timeout=20) as resp:
            tree = json.loads(resp.read().decode("utf-8")).get("tree", [])
        for item in tree:
            if item.get("type") == "blob":
                rp = item["path"].lstrip("/")
                self._catat_entri(manifest, Path(rp[11:] if rp.startswith("vibe_tools/") else rp), f"git:{item['sha']}", url=f"{self.GITHUB_RAW_BASE}{rp}")
        return manifest

    def analyze_workspace(self, source_manifest: Dict[str, str]) -> List[FileDiffManifest]:
        """[ID]: Membandingkan berkas target terhadap manifest sumber (lokal/remote)."""
        diffs: List[FileDiffManifest] = []
        for rel_posix, src_hash in source_manifest.items():
            rel_path = Path(rel_posix)
            if self.is_blacklisted(rel_path): continue
            loc_file, is_prot = self.target_root / rel_path, self.is_strictly_protected(rel_path)
            if not loc_file.exists():
                diffs.append(FileDiffManifest(rel_path, UpdateStatus.NEW_FILE, src_hash, None, is_prot)); continue
            if src_hash.startswith("git:"):
                loc_raw = self.hitung_git_blob_sha1(loc_file, False)
                sama, loc_hash = src_hash[4:] in (loc_raw, self.hitung_git_blob_sha1(loc_file, True)), f"git:{loc_raw}"
            else:
                loc_hash = self.hitung_sha256(loc_file); sama = (loc_hash == src_hash)
            st = UpdateStatus.PROTECTED_PROJECT_FILE if is_prot else (UpdateStatus.UP_TO_DATE if sama else UpdateStatus.OUTDATED)
            diffs.append(FileDiffManifest(rel_path, st, src_hash, loc_hash, is_prot))
        return diffs

    def smart_merge_agents_md(self, local_content: str, new_content: str) -> str:
        """[ID]: Menggabungkan guardrails universal ke .agents/AGENTS.md tanpa menghapus aturan proyek."""
        if not local_content.strip(): return new_content
        marker = "## Project Specific Rules"
        if marker in local_content: return f"{new_content.strip()}\n\n{marker}{local_content.split(marker, 1)[1]}"
        if local_content.strip() != new_content.strip() and "# Custom Agent Rules" in local_content:
            return f"{new_content.strip()}\n\n{marker} (Dipertahankan Otomatis):\n{local_content.strip()}"
        return new_content

    def create_pre_update_backup(self, files_to_update: List[Path]) -> Optional[Path]:
        """[ID]: Mencadangkan berkas/folder ke .agents/backups/backup_YYYYMMDD_HHMMSS/."""
        kandidat = [rel for rel in files_to_update if (self.target_root / rel).exists()]
        if not kandidat:
            return None
        target_backup = self.backup_dir / f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        target_backup.mkdir(parents=True, exist_ok=True)
        for rel in kandidat:
            src, dest = self.target_root / rel, target_backup / rel
            if src.is_file():
                dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dest)
            elif src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
        return target_backup

    def rollback_backup(self, backup_name: Optional[str] = None) -> bool:
        """[ID]: Memulihkan snapshot berkas dari folder backup."""
        backups = sorted([d for d in self.backup_dir.iterdir() if d.is_dir()], reverse=True) if self.backup_dir.exists() else []
        if not backups:
            print("[INFO] Tidak ada snapshot backup tersedia.")
            return False
        selected = (self.backup_dir / backup_name) if backup_name and (self.backup_dir / backup_name).exists() else backups[0]
        print(f">> Melakukan Rollback dari snapshot: {selected.name}")
        for f in selected.rglob("*"):
            if f.is_file():
                dest = self.target_root / f.relative_to(selected)
                dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, dest)
                print(f"  [RESTORE] {f.relative_to(selected).as_posix()}")
        print(">> Rollback selesai dengan sukses.")
        return True

    def _muat_modul_vibe(self, nama_modul: str):
        """[ID]: Mengimpor modul dari vibe_tools target atau sumber secara dinamis."""
        for root_vt in (self.target_root / "vibe_tools", self.source_vibe_dir):
            kandidat = root_vt / f"{nama_modul}.py"
            if kandidat.is_file():
                spec = importlib.util.spec_from_file_location(f"_vt_{nama_modul}", str(kandidat))
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
        return None

    def sync_aider_hybrid_cockpit(self, setup_ollama: bool = False) -> None:
        """[ID]: Memperbarui konfigurasi Aider Hybrid via setup_aider_hybrid.py."""
        try:
            mod = self._muat_modul_vibe("setup_aider_hybrid")
            if mod and hasattr(mod, "pasang_aider_hybrid"):
                mod.pasang_aider_hybrid(target_path=str(self.target_root), setup_ollama=setup_ollama)
        except Exception as e:
            print(f"[PERINGATAN] Gagal sinkronisasi Aider Hybrid: {e}")

    def sinkronkan_komponen_ekosistem(self, setup_ollama: bool = False, skip_global: bool = False) -> None:
        """[ID]: Menyelaraskan seluruh komponen ekosistem terbaru (AGENTS, Aider, Global Junction, MCP, MAP)."""
        print("\n>> Menyelaraskan komponen ekosistem terbaru...")
        mod_setup, mod_sync = self._muat_modul_vibe("setup_vibe_ecosystem"), self._muat_modul_vibe("sync_universal")
        if mod_setup:
            mod_setup.BASE_DIR, mod_setup.VT_DIR = self.target_root, self.target_root / "vibe_tools"
            try: mod_setup.pasang_agents_md()
            except Exception as e: print(f"[PERINGATAN] Sinkronisasi AGENTS.md dilewati: {e}")
        self.sync_aider_hybrid_cockpit(setup_ollama=setup_ollama)
        is_same_ws = (self.target_root == self.source_vibe_dir.parent)
        if not skip_global and (is_same_ws or not (Path.home() / ".gemini" / "config" / "rules").exists()):
            for fn, lbl in ((getattr(mod_sync, "sinkronisasi_universal", None), "global skills/rules"), (getattr(mod_setup, "sinkronkan_mcp_servers", None), "MCP global")):
                if fn:
                    try: fn()
                    except Exception as e: print(f"[PERINGATAN] Sinkronisasi {lbl} dilewati: {e}")
        elif mod_sync and hasattr(mod_sync, "sanitasi_frontmatter_rules"):
            try: mod_sync.sanitasi_frontmatter_rules([str(self.target_root / ".agents" / "rules")])
            except Exception: pass
        try:
            mod_map = self._muat_modul_vibe("graphify_sync")
            if mod_map and hasattr(mod_map, "perbarui_peta"):
                hasil = mod_map.perbarui_peta(str(self.target_root))
                print(f"[OK] Peta berkas (.agents/MAP.md) disinkronkan ({len(hasil.get('baru', []))} entri baru).")
        except Exception as e:
            print(f"[PERINGATAN] Pembaruan .agents/MAP.md dilewati: {e}")

    def _salin_atau_unduh(self, rel: Path) -> bool:
        """[ID]: Menyalin berkas dari sumber lokal atau mengunduh dari GitHub Raw."""
        rel_posix, dest = rel.as_posix(), self.target_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        src_lokal = self._source_map.get(rel_posix)
        if src_lokal and src_lokal.is_file():
            if rel_posix == ".agents/AGENTS.md" and dest.exists():
                dest.write_text(self.smart_merge_agents_md(dest.read_text(encoding="utf-8"), src_lokal.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
            elif src_lokal.resolve() != dest.resolve():
                shutil.copy2(src_lokal, dest)
            return True
        if rel_posix in self._remote_urls:
            req = urllib.request.Request(self._remote_urls[rel_posix], headers={"User-Agent": "vibe-tools-updater"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                dest.write_bytes(resp.read())
            return True
        return False

    def apply_updates(self, diffs: List[FileDiffManifest], dry_run: bool = False, setup_ollama: bool = False, skip_global: bool = False, prune_legacy: bool = True) -> bool:
        """[ID]: Menerapkan pembaruan berkas, backup otomatis, pembersihan aset usang, & sinkronisasi penuh."""
        to_up = [d.relative_path for d in diffs if d.status in (UpdateStatus.OUTDATED, UpdateStatus.NEW_FILE) and not d.is_protected]
        usang = [Path(p) for p in self.LEGACY_OBSOLETE_PATHS if prune_legacy and (self.target_root / p).exists()]
        if not to_up and not usang:
            print(">> Seluruh berkas vibe_tools sudah versi terbaru (UP TO DATE).")
            if not dry_run:
                self.sinkronkan_komponen_ekosistem(setup_ollama=setup_ollama, skip_global=skip_global)
            return True
        print(f">> Analisis: {len(to_up)} berkas diperbarui/ditambah, {len(usang)} aset usang dibersihkan:")
        rea_count = 0
        for d in diffs:
            p_str = d.relative_path.as_posix()
            if d.is_protected:
                print(f"  [DILINDUNGI] {p_str} (aturan kustom aman)")
            elif d.status in (UpdateStatus.OUTDATED, UpdateStatus.NEW_FILE):
                if p_str.startswith("vibe_tools/mcp_schemas/rea/"):
                    rea_count += 1; continue
                print(f"  {('[BARU]' if d.status == UpdateStatus.NEW_FILE else '[UPDATE]'):<10} {p_str}")
        if rea_count: print(f"  {'[BULK]':<10} vibe_tools/mcp_schemas/rea/* ({rea_count} skema MCP)")
        for u in usang: print(f"  {'[USANG]':<10} {u.as_posix()}")
        if dry_run:
            print("[DRY RUN] Mode simulasi selesai. Tidak ada berkas yang diubah.")
            return True
        if b_path := self.create_pre_update_backup(to_up + usang):
            print(f">> Backup pra-update disimpan di: {b_path.name}")
        for rel in to_up: self._salin_atau_unduh(rel)
        for u in usang:
            t_u = self.target_root / u
            shutil.rmtree(t_u, ignore_errors=True) if t_u.is_dir() else t_u.unlink(missing_ok=True)
        self.sinkronkan_komponen_ekosistem(setup_ollama=setup_ollama, skip_global=skip_global)
        return True


def main() -> None:
    """[ID]: Titik masuk CLI Universal Ecosystem Updater (Antigravity + Aider + MCP)."""
    parser = argparse.ArgumentParser(description="Vibe Tools Universal Updater (Antigravity + Aider + MCP)")
    for flag, hlp in (
        ("--pull", "Tarik pembaruan submodule dari GitHub sebelum update"),
        ("--remote", "Ambil manifest & pasang berkas terbaru langsung dari GitHub API"),
        ("--check", "Pengecekan versi tanpa modifikasi"),
        ("--dry-run", "Simulasi pembaruan tanpa menyentuh disk"),
        ("--setup-ollama", "Tampilkan cek & panduan opsi Ollama lokal"),
        ("--skip-global", "Lewati sinkronisasi junction & MCP global (~/.gemini)"),
        ("--no-prune", "Jangan hapus berkas legacy usang di vibe_tools/"),
    ):
        parser.add_argument(flag, action="store_true", help=hlp)
    parser.add_argument("--target", default="", help="Path direktori proyek tujuan (Offline/Remote Push)")
    parser.add_argument("--rollback", nargs="?", const="", help="Pulihkan konfigurasi dari backup")
    args = parser.parse_args()
    if args.pull and (skrip_pull := Path(__file__).resolve().parent / "pull_from_github.py").is_file():
        subprocess.run([sys.executable, str(skrip_pull), "--no-sync"])
    updater = VibeEcosystemUpdater(target_root=Path(args.target).resolve() if args.target else Path.cwd().resolve())
    if args.rollback is not None:
        updater.rollback_backup(args.rollback or None); return
    pakai_remote = args.remote or not (updater.source_vibe_dir / "rules").is_dir()
    manifest = updater.build_remote_manifest() if pakai_remote else updater.build_local_manifest()
    updater.apply_updates(updater.analyze_workspace(manifest), dry_run=(args.check or args.dry_run), setup_ollama=args.setup_ollama, skip_global=args.skip_global, prune_legacy=not args.no_prune)


if __name__ == "__main__":
    main()
