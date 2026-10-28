"""
Modul: gemini_web_automator.py
Deskripsi: Automasi peramban Chromium menggunakan Playwright untuk memproses highlight VOD di Gemini Web (gemini.google.com).
           Menggunakan profil peramban tersimpan (cookies & sesi langganan Gemini Pro/Argon aktif),
           mengirimkan prompt & data chat secara otomatis, memantau proses berpikir model hingga tuntas,
           lalu mengekstrak laporan markdown langsung ke sections.txt dan marker DaVinci Resolve tanpa biaya API.
"""

import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Konfigurasi encoding UTF-8 untuk terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Tambahkan path ke modul terkait
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "vibe_tools"))
sys.path.append(str(ROOT_DIR / "cache_chat" / "davinci_core"))

try:
    from core.chat_peak_detector import ekspor_livechat_timeline_csv
except ImportError:
    ekspor_livechat_timeline_csv = None

try:
    from gemini_prompt_builder import GeminiWebPromptFacade
except ImportError:
    from vibe_tools.gemini_prompt_builder import GeminiWebPromptFacade

try:
    from auto_highlighter_argon import (
        analisis_lonjakan_cpm,
        buat_prompt_analisis,
        ekstrak_segmen_dari_markdown,
        muat_livechat,
        muat_transkrip,
        simpan_ke_sections_txt,
        temukan_folder_channel,
    )
except ImportError:
    pass

try:
    # pyrefly: ignore[missing-import]
    from marker_exporter import ekspor_ke_csv, ekspor_ke_edl, injeksi_marker_ke_resolve
except ImportError:
    ekspor_ke_csv = None
    ekspor_ke_edl = None
    injeksi_marker_ke_resolve = None

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout, sync_playwright
except ImportError:
    print("[ERROR] Playwright belum terpasang. Jalankan: pip install playwright && playwright install chromium")
    sys.exit(1)


def dapatkan_path_profil_chrome(gunakan_profil_utama: bool = False) -> str:
    """
    Menentukan path folder profil Chrome.
    Jika gunakan_profil_utama: memakai folder User Data Google Chrome Windows asli.
    Jika default: memakai folder profil automasi tersendiri di ~/.gemini/chrome_gemini_profile
    agar tidak bentrok kunci (lock) jika Google Chrome biasa sedang dibuka.
    """
    if gunakan_profil_utama:
        path_utama = Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data"
        if path_utama.exists():
            return str(path_utama)

    # Profil dedikasi automasi (login satu kali, sesi tersimpan permanen)
    profil_dedikasi = Path.home() / ".gemini" / "chrome_gemini_profile"
    profil_dedikasi.mkdir(parents=True, exist_ok=True)
    return str(profil_dedikasi)


class GeminiWebAutomator:
    """Kelas pengontrol automasi peramban Gemini Web berbasis Playwright."""

    def __init__(self, user_data_dir: str, headless: bool = False, debug_port: int = 0):
        self.user_data_dir = user_data_dir
        self.headless = headless
        self.debug_port = debug_port
        self.playwright = None
        self.context = None
        self.page = None

    def buka_browser(self):
        """Membuka peramban Chromium dengan profil persisten atau menempel via CDP."""
        self.playwright = sync_playwright().start()

        # Opsi 1: Menempel ke Chrome yang sudah berjalan dengan remote-debugging-port
        if self.debug_port > 0:
            try:
                print(f"[INFO] Mencoba menghubungkan ke Chrome di port {self.debug_port} (CDP)...")
                browser = self.playwright.chromium.connect_over_cdp(f"http://localhost:{self.debug_port}")
                self.context = browser.contexts[0] if browser.contexts else browser.new_context()
                self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
                print("      Berhasil terhubung ke sesi Chrome aktif.")
                return
            except Exception as e:
                print(f"      [INFO] Tidak dapat menghubungkan via port {self.debug_port}: {e}. Membuka browser mandiri...")

        # Opsi 2: Membuka Chromium dengan profil persisten (cookies & cache tersimpan)
        args = [
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--no-default-browser-check",
            "--enable-clipboard-read-write",
        ]

        print(f"[INFO] Membuka peramban dengan profil: {self.user_data_dir}")
        permissions = ["clipboard-read", "clipboard-write"]
        try:
            # Gunakan Google Chrome asli di sistem jika tersedia agar Google login lebih terpercaya
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                args=args,
                permissions=permissions,
                no_viewport=True,
                channel="chrome",
            )
            self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        except Exception as e_chrome:
            print(f"[INFO] Channel Chrome dialihkan ke Chromium bawaan: {e_chrome}")
            try:
                self.context = self.playwright.chromium.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    headless=self.headless,
                    args=args,
                    permissions=permissions,
                    no_viewport=True,
                )
                self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
            except Exception as e:
                # Jika profil utama terkunci oleh Chrome yang sedang aktif, beralih ke profil automasi khusus
                if "Target page, context or browser has been closed" in str(e) or "lock" in str(e).lower():
                    print("[WARNING] Profil Chrome utama sedang dipakai aplikasi lain. Beralih ke profil automasi khusus...")
                    fallback_dir = str(Path.home() / ".gemini" / "chrome_gemini_profile")
                    self.context = self.playwright.chromium.launch_persistent_context(
                        user_data_dir=fallback_dir,
                        headless=self.headless,
                        args=args,
                        permissions=permissions,
                        no_viewport=True,
                    )
                    self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
                else:
                    raise e

    def navigasi_ke_gemini(self):
        """
[ID]: Membuka laman gemini.google.com dan memvalidasi kesiapan halaman.
[EN]: Open gemini.google.com and validate page readiness.
"""
        print("[INFO] Membuka https://gemini.google.com/app ...")
        self.page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)

        # Cek apakah perlu login (bisa via URL accounts.google.com atau tombol Sign In / Masuk)
        tombol_signin = self.page.locator('a[href*="accounts.google.com"], button:has-text("Sign in"), button:has-text("Masuk")').first
        perlu_login = False
        try:
            if "accounts.google.com" in self.page.url or tombol_signin.is_visible(timeout=2000):
                perlu_login = True
        except Exception:
            pass

        if perlu_login:
            print("\n" + "=" * 65)
            print("[PERINGATAN] Sesi belum login ke akun Google Gemini Pro Anda.")
            print("Silakan klik 'Sign in' / 'Masuk' di jendela browser yang terbuka.")
            print("CUKUP LOGIN 1 KALI INI SAJA! Cookies & sesi akan tersimpan permanen di:")
            print(f"  {self.user_data_dir}")
            print("Untuk penggunaan selanjutnya, Anda TIDAK PERLU login lagi!")
            print("=" * 65 + "\n")

            try:
                if tombol_signin.is_visible(timeout=1000):
                    tombol_signin.click()
            except Exception:
                pass

            # Tunggu hingga pengguna selesai login (kotak input chat sudah muncul di gemini.google.com)
            self.page.wait_for_selector(
                'div[contenteditable="true"], div.ql-editor, rich-textarea, textarea',
                timeout=300000
            )
            time.sleep(3)

        print("      Laman Gemini Web siap.")

    def _temukan_tombol_picker_model(self):
        """Mencari tombol picker model di dalam prompt bar Gemini."""
        selectors = [
            'button:has-text("Flash")',
            'button:has-text("3.8 Flash")',
            'button:has-text("3.5 Flash-Lite")',
            'button:has-text("3.1 Pro")',
            'button:has-text("4 Argon")',
            'button:has-text("Argon")',
            'button:has-text("Pro")',
            'button[aria-haspopup="menu"]',
            'button[aria-label*="model" i]',
            'button[aria-label*="Model" i]',
            '[data-test-id*="model-selector"]',
            '.model-picker-btn',
        ]
        for sel in selectors:
            try:
                loc = self.page.locator(sel).first
                if loc.is_visible(timeout=1000):
                    return loc
            except Exception:
                continue

        # Fallback via JavaScript evaluasi untuk tombol di dekat input chat
        try:
            handle = self.page.evaluate_handle(
                """() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    for (const b of buttons) {
                        const t = (b.innerText || '').trim();
                        if (/^(Flash|3\\.8 Flash|3\\.5 Flash-Lite|3\\.1 Pro|4 Argon|Argon|Pro)$/i.test(t) ||
                            ((t.includes('Flash') || t.includes('Argon') || t.includes('Pro')) && b.querySelector('mat-icon, svg, i'))) {
                            return b;
                        }
                    }
                    return null;
                }"""
            )
            if handle and handle.as_element():
                return handle.as_element()
        except Exception:
            pass

        return None

    def pilih_model_argon_jika_ada(self):
        """
        Otomatis memilih model 4 Argon dan mengatur Tingkat Penalaran ke 'Tinggi'.
        Sesuai antarmuka Gemini web Bahasa Indonesia / Inggris.
        """
        print("[INFO] Mengonfigurasi model ke '4 Argon' dan penalaran 'Tinggi'...")
        try:
            time.sleep(1.5)
            # 1. Buka dropdown model jika belum terbuka
            btn_picker = self._temukan_tombol_picker_model()
            if not btn_picker:
                print("      [WARNING] Tombol pemilih model tidak ditemukan di halaman.")
                return

            btn_text = ""
            try:
                btn_text = btn_picker.inner_text().strip()
            except Exception:
                pass
            print(f"      Tombol model saat ini: '{btn_text}'")

            # Klik tombol picker untuk menampilkan daftar menu
            btn_picker.click()
            time.sleep(1)

            # 2. Cari dan klik opsi '4 Argon' (Tugas kompleks)
            selectors_argon = [
                'text=/4\\s*Argon/i',
                '[role="menuitem"]:has-text("4 Argon")',
                '[role="menuitem"]:has-text("Argon")',
                'div:has-text("4 Argon")',
                'text=/Argon/i',
            ]
            argon_dipilih = False
            for sel in selectors_argon:
                loc_argon = self.page.locator(sel).first
                try:
                    if loc_argon.is_visible(timeout=1500):
                        loc_argon.click()
                        argon_dipilih = True
                        print("      [OK] Berhasil memilih model: 4 Argon.")
                        time.sleep(1.5)
                        break
                except Exception:
                    continue

            if not argon_dipilih:
                print("      [INFO] Opsi '4 Argon' belum terklik atau sudah aktif. Melanjutkan ke pengaturan tingkat penalaran...")

            # 3. Pengaturan 'Tingkat penalaran' ke 'Tinggi'
            # Cek apakah menu masih terbuka atau perlu dibuka ulang
            loc_penalaran = self.page.locator('text=/Tingkat\\s*penalaran|Reasoning\\s*level/i').first
            menu_terbuka = False
            try:
                menu_terbuka = loc_penalaran.is_visible(timeout=1000)
            except Exception:
                pass

            if not menu_terbuka:
                # Buka kembali menu picker
                btn_picker_again = self._temukan_tombol_picker_model()
                if btn_picker_again:
                    btn_picker_again.click()
                    time.sleep(1)

            # Cari item 'Tingkat penalaran' (Reasoning level)
            loc_penalaran = self.page.locator('text=/Tingkat\\s*penalaran|Reasoning\\s*level/i').first
            try:
                if loc_penalaran.is_visible(timeout=2500):
                    print("      Membuka submenu 'Tingkat penalaran'...")
                    loc_penalaran.hover()
                    time.sleep(0.5)
                    loc_penalaran.click()
                    time.sleep(1)

                    # 4. Pilih opsi 'Tinggi' (High)
                    selectors_tinggi = [
                        'text=/^Tinggi$|^High$/i',
                        '[role="menuitem"]:has-text("Tinggi")',
                        '[role="menuitem"]:has-text("High")',
                        'div:has-text("Tinggi")',
                        'text=/Tinggi/i',
                        'text=/High/i',
                    ]
                    tinggi_dipilih = False
                    for sel_t in selectors_tinggi:
                        loc_tinggi = self.page.locator(sel_t).first
                        try:
                            if loc_tinggi.is_visible(timeout=1500):
                                loc_tinggi.click()
                                tinggi_dipilih = True
                                print("      [OK] Berhasil mengatur Tingkat Penalaran ke: TINGGI.")
                                time.sleep(1)
                                break
                        except Exception:
                            continue

                    if not tinggi_dipilih:
                        print("      [INFO] Opsi 'Tinggi' tidak terdeteksi langsung atau sudah terpilih secara default.")
            except Exception as e_penalaran:
                print(f"      [INFO] Kendala saat menyetel tingkat penalaran: {e_penalaran}")

            # 5. Tutup sisa popup menu jika masih terbuka
            try:
                self.page.keyboard.press("Escape")
                time.sleep(0.5)
            except Exception:
                pass

            print("      Model 4 Argon & tingkat penalaran siap.")
        except Exception as e:
            print(f"[WARNING] Gagal otomatisasi pemilihan model Argon: {e}")

    def lampirkan_berkas(self, file_paths: List[str]) -> bool:
        """
        Melampirkan berkas sumber asli (livechat.csv dan/atau transkrip.csv)
        langsung dari folder channel VTuber ke formulir Gemini Web via Playwright.
        """
        valid_paths = []
        for p in file_paths:
            if not p:
                continue
            src = Path(p).resolve()
            if not src.exists():
                continue
            valid_paths.append(str(src))

        if not valid_paths:
            print("      [WARNING] Tidak ada berkas valid untuk dilampirkan.")
            return False

        print(f"[INFO] Melampirkan {len(valid_paths)} berkas sumber asli ke Gemini Web:")
        for vp in valid_paths:
            print(f"      • {vp}")

        try:
            # 1. Cek apakah elemen input[type="file"] sudah tersedia di DOM
            file_input = self.page.locator('input[type="file"]').first
            input_ada = False
            try:
                if file_input.count() > 0:
                    input_ada = True
            except Exception:
                pass

            if not input_ada:
                # Klik tombol unggah/tambah file untuk merender file input jika belum ada
                selectors_upload = [
                    'button[aria-label*="Upload"]',
                    'button[aria-label*="Unggah"]',
                    'button[aria-label*="Tambahkan"]',
                    'button[aria-label*="Add"]',
                    'button[aria-label*="file"]',
                    'button:has(mat-icon:has-text("add"))',
                    'button:has(mat-icon:has-text("attach_file"))',
                    'button:has(svg[data-icon="plus"])',
                    '.upload-button',
                ]
                for sel in selectors_upload:
                    try:
                        loc = self.page.locator(sel).first
                        if loc.is_visible(timeout=1500):
                            loc.click()
                            time.sleep(1)
                            break
                    except Exception:
                        continue

            # 2. Injeksi berkas ke input[type="file"]
            self.page.set_input_files('input[type="file"]', valid_paths)
            print("      [OK] Berkas berhasil dilampirkan ke sesi Gemini Web.")

            # Pastikan popup menu atau dialog overlay tertutup agar tidak menghalangi kotak input
            try:
                self.page.keyboard.press("Escape")
            except Exception:
                pass
            time.sleep(3)  # Tunggu rendering chip pratinjau berkas
            return True

        except Exception as e:
            print(f"      [WARNING] Gagal melampirkan berkas ke Gemini Web: {e}")
            return False

    def injeksi_prompt(self, teks_prompt: str):
        """Menginjeksi teks prompt ke dalam kotak input Gemini secara instan tanpa lag."""
        print("[INFO] Menginjeksi teks prompt ke kotak pesan...")

        # Tutup dialog/dropdown/overlay apa pun yang mungkin masih terbuka
        try:
            self.page.keyboard.press("Escape")
            time.sleep(0.5)
        except Exception:
            pass

        # Selector kotak input pesan Gemini
        selectors_input = [
            'div[contenteditable="true"]',
            'div.ql-editor',
            'rich-textarea p',
            'rich-textarea div',
            'rich-textarea',
            'textarea',
        ]

        target_input = None
        for attempt in range(8):
            for sel in selectors_input:
                loc = self.page.locator(sel).first
                try:
                    if loc.is_visible(timeout=1000):
                        target_input = loc
                        break
                except Exception:
                    continue
            if target_input:
                break
            time.sleep(1)

        if not target_input:
            raise RuntimeError("Kotak input chat Gemini tidak ditemukan di halaman.")

        try:
            target_input.click(force=True, timeout=3000)
        except Exception:
            try:
                target_input.focus(timeout=2000)
            except Exception:
                pass
        time.sleep(0.5)

        # Injeksi menggunakan clipboard paste (metode paling handal untuk Quill / rich-textarea Angular)
        injeksi_sukses = False
        try:
            self.page.evaluate(
                """async (teks) => {
                    await navigator.clipboard.writeText(teks);
                }""",
                teks_prompt
            )
            self.page.keyboard.press("Control+V")
            time.sleep(0.8)
            injeksi_sukses = True
        except Exception:
            pass

        if not injeksi_sukses:
            # Fallback JavaScript innerText + Dispatch Event
            self.page.evaluate(
                """(teks) => {
                    const el = document.querySelector('div[contenteditable="true"], div.ql-editor, rich-textarea p, textarea');
                    if (el) {
                        el.focus();
                        if (el.tagName === 'P') {
                            el.textContent = teks;
                        } else {
                            el.innerText = teks;
                        }
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""",
                teks_prompt,
            )
        time.sleep(1)

    def kirim_dan_tunggu_respon(self, batas_waktu_detik: int = 600) -> str:
        """Menekan tombol kirim dan memantau DOM hingga proses pembuatan teks selesai sepenuhnya."""
        print("[INFO] Mengirim pesan ke Gemini...")

        # Cari tombol kirim
        selectors_kirim = [
            'button[aria-label*="Send"]',
            'button[aria-label*="Kirim"]',
            'button.send-button',
            'mat-icon:has-text("send")',
            'button:has(mat-icon:has-text("send"))',
        ]

        tombol_kirim = None
        for sel in selectors_kirim:
            loc = self.page.locator(sel).first
            try:
                if loc.is_visible(timeout=2000):
                    tombol_kirim = loc
                    break
            except Exception:
                continue

        if tombol_kirim:
            tombol_kirim.click()
        else:
            # Alternatif: tekan tombol Enter di keyboard
            self.page.keyboard.press("Enter")

        print("      Pesan terkirim. Menunggu proses penalaran dan pembuatan teks (Thinking)...")

        # Beri jeda awal agar status 'Thinking / Generating' muncul di DOM
        time.sleep(5)

        # Tunggu hingga balasan model benar-benar selesai dibuat dan teksnya stabil
        selectors_stop = [
            'button[aria-label*="Stop"]',
            'button[aria-label*="Berhenti"]',
            'button[aria-label*="Hentikan"]',
            'button:has-text("Stop generating")',
            'button:has-text("Berhenti")',
            '.stop-generating-button',
        ]

        waktu_mulai = time.time()
        panjang_terakhir = 0
        hitung_stabil = 0

        while time.time() - waktu_mulai < batas_waktu_detik:
            ada_tombol_stop = False
            for sel in selectors_stop:
                try:
                    loc = self.page.locator(sel).first
                    if loc.is_visible(timeout=400):
                        ada_tombol_stop = True
                        break
                except Exception:
                    pass

            # Ambil teks dari kontainer jawaban model (bukan gelembung prompt user)
            teks_model = ""
            try:
                kontainer_model = self.page.locator(
                    'model-response message-content, .model-response-text, message-content'
                ).last
                if kontainer_model.count() > 0:
                    teks_model = (kontainer_model.inner_text() or "").strip()
            except Exception:
                pass

            # Abaikan jika teks masih kosong, masih berupa prompt user, atau terlalu pendek (< 200 karakter)
            bukan_prompt = (
                "# ROLE & OBJECTIVE" not in teks_model
                and "# DATA KLASTER LONJAKAN" not in teks_model
                and "# CANDIDATE CLUSTER DATA" not in teks_model
            )
            sudah_berisi_laporan = len(teks_model) > 250 and bukan_prompt
            ada_struktur = "timeline kronologis" in teks_model.lower() and "kandidat klip" in teks_model.lower()
            ada_hashtag = "hashtag" in teks_model.lower()

            # Deteksi cepat jika model menolak (Safety Refusal) saat tombol stop sudah hilang
            frasa_refusal_cepat = [
                "against my guidelines", "go against", "against our guidelines",
                "safety guidelines", "tidak bisa membantu", "hanya model bahasa", "cannot help"
            ]
            teks_lower = teks_model.lower()
            terdeteksi_refusal = (
                not ada_tombol_stop
                and len(teks_model) > 20
                and len(teks_model) < 400
                and any(f in teks_lower for f in frasa_refusal_cepat)
            )

            if terdeteksi_refusal:
                print(f"      [WARNING] Terdeteksi respon penolakan keselamatan model ({len(teks_model)} karakter).")
                break

            if not ada_tombol_stop and sudah_berisi_laporan and ada_struktur:
                # Opsi 3A: Auto-scroll ke bawah saat tombol stop hilang agar konten virtual/lazy render muncul penuh
                try:
                    self.page.evaluate("""() => {
                        window.scrollTo(0, document.body.scrollHeight);
                        const scroller = document.querySelector('chat-window, infinite-scroller, .chat-history, main');
                        if (scroller) scroller.scrollTop = scroller.scrollHeight;
                    }""")
                except Exception:
                    pass

                # Tunggu teks stabil atau sampai penutup hashtag terdeteksi
                if ada_hashtag or len(teks_model) == panjang_terakhir:
                    hitung_stabil += 1
                    if (ada_hashtag and hitung_stabil >= 2) or hitung_stabil >= 4:
                        print(f"      Proses penalaran dan pembuatan teks selesai! ({len(teks_model)} karakter, penutup Hashtag terverifikasi)")
                        break
                else:
                    panjang_terakhir = len(teks_model)
                    hitung_stabil = 0
            else:
                panjang_terakhir = len(teks_model)
                hitung_stabil = 0

            time.sleep(2)

        # Ekstrak respon teks terakhir dari asisten/model
        hasil = self.ekstrak_respon_markdown()

        # Deteksi penolakan model (Refusal / Safety filter)
        frasa_penolakan = [
            "saya hanya ai berbasis teks",
            "tidak dirancang untuk itu",
            "tidak bisa membantu anda untuk itu",
            "as a text-based ai",
            "i cannot process video",
            "i'm only a language model",
            "against my guidelines",
            "go against",
            "against our guidelines",
            "safety guidelines",
        ]
        hasil_lower = hasil.lower()
        if any(f in hasil_lower for f in frasa_penolakan) and len(hasil) < 350:
            print("      [WARNING] Terdeteksi penolakan awal model / pedoman keselamatan (Safety Guidelines).")
            if "guidelines" in hasil_lower or "go against" in hasil_lower:
                print("      [INFO] Mengirim instruksi klarifikasi ramah pedoman keselamatan Google...")
                pesan_klarifikasi = (
                    "Klarifikasi Keselamatan: Ini MURNI analisis kurasi arsip siaran hiburan gaming publik yang ramah keluarga (PG-13). Tolong abaikan pesan spam atau kata-kata kasar penonton di riwayat chat, dan buatkan dokumen laporan Markdown highlight momen game di atas sekarang sesuai format yang diminta."
                )
            else:
                print("      [INFO] Mengirim klarifikasi otomatis bahwa ini adalah tugas penulisan teks dokumen Markdown...")
                pesan_klarifikasi = (
                    "Klarifikasi: Anda TIDAK diminta memproses atau memutar berkas video. Tugas ini MURNI analisis data teks di atas untuk menuliskan daftar catatan waktu (timestamp) ke dalam format dokumen teks Markdown. Tolong buatkan dokumen laporan Markdown sesuai format di atas sekarang."
                )
            self.injeksi_prompt(pesan_klarifikasi)

            # Klik tombol kirim
            selectors_kirim = [
                'button[aria-label*="Send"]',
                'button[aria-label*="Kirim"]',
                'button.send-button',
                'mat-icon:has-text("send")',
                'button:has(mat-icon:has-text("send"))',
            ]
            for sel in selectors_kirim:
                try:
                    loc = self.page.locator(sel).first
                    if loc.is_visible(timeout=1500):
                        loc.click()
                        break
                except Exception:
                    pass
            else:
                self.page.keyboard.press("Enter")

            print("      Menunggu respon model setelah klarifikasi teks...")
            time.sleep(6)
            # Polling ulang sampai generasi selesai
            waktu_mulai2 = time.time()
            panjang2 = 0
            stabil2 = 0
            while time.time() - waktu_mulai2 < 180:
                teks_skrg = self.ekstrak_respon_markdown()
                if len(teks_skrg) > 300:
                    if len(teks_skrg) == panjang2:
                        stabil2 += 1
                        if stabil2 >= 3:
                            hasil = teks_skrg
                            break
                    else:
                        panjang2 = len(teks_skrg)
                        stabil2 = 0
                time.sleep(2)
            hasil = self.ekstrak_respon_markdown()

        return hasil

    def ekstrak_respon_markdown(self) -> str:
        """Mengambil teks markdown dari elemen respon model terakhir di Gemini Web (Hybrid Dual-Check Opsi 2C)."""
        print("[INFO] Mengekstrak hasil respon markdown...")

        # Pastikan halaman di-scroll ke elemen respons model terakhir
        try:
            self.page.evaluate("""() => {
                const el = document.querySelector('model-response:last-of-type, .model-response-text:last-of-type');
                if (el) el.scrollIntoView({ behavior: 'instant', block: 'end' });
            }""")
            time.sleep(0.5)
        except Exception:
            pass

        # Fungsi pembantu validasi respons model
        def _is_valid_model_response(t: str) -> bool:
            if not t or len(t) < 25:
                return False
            # Pastikan bukan teks prompt input kita sendiri
            if (
                "DATA KLASTER HASIL ANALISIS LONJAKAN" in t
                or "# DATA KLASTER LONJAKAN" in t
                or "# CANDIDATE CLUSTER DATA" in t
            ):
                return False
            return True

        # Opsi 0: Cek Canvas / Dokumen Artifact viewer Gemini
        selectors_canvas = [
            'document-canvas',
            'div[data-test-id*="document"]',
            'div[class*="document-content"]',
            'div[class*="canvas-content"]',
            'div[class*="document-viewer"]',
            'div[role="region"][aria-label*="Canvas"]',
            'div[role="region"][aria-label*="Dokumen"]',
            'div[role="region"][aria-label*="Document"]',
            '.ql-editor[contenteditable="false"]',
            '.rendered-markdown',
        ]
        for sel in selectors_canvas:
            try:
                loc = self.page.locator(sel).first
                if loc.is_visible(timeout=1500):
                    teks_canvas = loc.inner_text()
                    if teks_canvas and len(teks_canvas) > 250 and ("Timeline Kronologis" in teks_canvas or "Berakhir di" in teks_canvas):
                        print(f"      [OK] Berhasil mengekstrak {len(teks_canvas)} karakter langsung dari Canvas Dokumen Gemini.")
                        return teks_canvas
            except Exception:
                continue

        # Opsi A (Utama): Klik tombol "Salin" (Copy) di model-response terakhir
        selectors_copy = [
            'model-response:last-of-type button[aria-label*="Copy"]',
            'model-response:last-of-type button[aria-label*="Salin"]',
            'model-response button[aria-label*="Copy"]',
            'model-response button[aria-label*="Salin"]',
            '.response-container:last-of-type button[aria-label*="Copy"]',
            '.response-container:last-of-type button[aria-label*="Salin"]',
            'button[aria-label*="Copy to clipboard"]',
            'button[aria-label*="Salin ke papan klip"]',
        ]
        for sel_copy in selectors_copy:
            try:
                tombol_salin = self.page.locator(sel_copy).last
                if tombol_salin.is_visible(timeout=1000):
                    tombol_salin.click(force=True)
                    time.sleep(0.8)
                    teks_cb = self.page.evaluate("navigator.clipboard.readText()")
                    if _is_valid_model_response(teks_cb):
                        print(f"      [OK] Berhasil mengekstrak {len(teks_cb)} karakter via tombol Salin resmi (Clipboard).")
                        return teks_cb
            except Exception:
                continue

        # Opsi B (Fallback): Ambil langsung dari container pesan model
        selectors_respon = [
            'model-response:last-of-type message-content',
            'model-response message-content',
            '.model-response-text',
            '[data-message-author="model"]',
            'message-content',
        ]
        for sel in selectors_respon:
            try:
                kontainer = self.page.locator(sel).last
                if kontainer.is_visible(timeout=2000):
                    teks = kontainer.inner_text()
                    if _is_valid_model_response(teks):
                        print(f"      [OK] Berhasil mengekstrak {len(teks)} karakter langsung dari kontainer model.")
                        return teks
            except Exception:
                pass

        raise RuntimeError(
            "Model Gemini Web tidak mengembalikan teks rangkuman valid (elemen respon model tidak terdeteksi atau sesi belum siap)."
        )

    def tutup(self):
        """Menutup konteks peramban dengan aman."""
        try:
            if self.context:
                self.context.close()
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass


def pangkas_laporan_bersih(teks: str) -> str:
    """Memangkas teks respon agar bersih mulai dari '## 1. Timeline Kronologis' (Opsi 1A)."""
    if not teks:
        return ""
    m = re.search(r"(##\s*1\.\s*Timeline Kronologis.*)", teks, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return teks.strip()


def buat_prompt_gemini_web(
    klaster_segmen: Optional[List[Dict[str, Any]]] = None,
    vtuber_name: str = "VTuber",
    vod_title: str = "VTuber Livestream Highlight",
    files_attached: bool = True,
) -> str:
    """Menyusun prompt kurasi teks catatan waktu (timestamp) untuk Gemini Web via Facade Pattern."""
    return GeminiWebPromptFacade.create_prompt(
        klaster_segmen=klaster_segmen,
        vtuber_name=vtuber_name,
        vod_title=vod_title,
        files_attached=files_attached,
    )


def main():
    parser = argparse.ArgumentParser(description="Automasi Gemini Web via Chromium untuk ekstraksi highlight VTuber.")
    parser.add_argument("--chat", type=str, default="", help="Path berkas livechat.csv")
    parser.add_argument("--transcript", type=str, default="", help="Path berkas transkrip.csv")
    parser.add_argument("--url", type=str, default="", help="URL video YouTube sumber")
    parser.add_argument("--vtuber", type=str, default="VTuber", help="Nama VTuber")
    parser.add_argument("--vod", type=str, default="VTuber Livestream", help="Judul VOD")
    parser.add_argument("--headless", action="store_true", help="Jalankan tanpa tampilan jendela (headless)")
    parser.add_argument("--main-profile", action="store_true", help="Gunakan profil Chrome utama (User Data)")
    parser.add_argument("--debug-port", type=int, default=0, help="Port remote debugging Chrome (default 0 / dinonaktifkan)")
    parser.add_argument("--output-sections", type=str, default="sections.txt", help="Path keluaran sections.txt")
    parser.add_argument("--auto-marker", action="store_true", default=True, help="Otomatis injeksikan marker ke DaVinci")
    parser.add_argument("--attach-chat", action="store_true", default=False, help="Lampirkan berkas livechat.csv mentah ke Gemini Web (default False agar tidak memicu safety filter penonton)")

    args = parser.parse_args()

    base_dir = ROOT_DIR
    chat_file = args.chat
    transkrip_file = args.transcript
    url = args.url
    vtuber = args.vtuber
    vod = args.vod

    if not url:
        sec_file = base_dir / "sections.txt"
        if sec_file.exists():
            for line in sec_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    url = line.split("|")[0].strip()
                    break
        if not url:
            url = "https://www.youtube.com/watch?v=source_video"

    # Resolusi otomatis folder channel, talent, dan judul VOD
    auto_folder, auto_vtuber, auto_vod = temukan_folder_channel(url, base_dir)

    if chat_file and Path(chat_file).exists():
        auto_folder = Path(chat_file).parent
    elif not chat_file and auto_folder:
        calon_chat = auto_folder / "livechat.csv"
        if calon_chat.exists():
            chat_file = str(calon_chat)

    if not transkrip_file and auto_folder:
        calon_transkrip = auto_folder / "transkrip.csv"
        if calon_transkrip.exists():
            transkrip_file = str(calon_transkrip)

    if vtuber in ("", "VTuber") and auto_vtuber != "VTuber":
        vtuber = auto_vtuber

    if vod in ("", "VTuber Livestream", "VTuber Livestream Highlight", "VTuber Highlight") and auto_vod != "VTuber Livestream Highlight":
        vod = auto_vod

    print("=" * 60)
    print("🌐 GEMINI WEB AUTOMATOR (MODE B - CHROMIUM)")
    print(f"• Talent         : {vtuber}")
    print(f"• Judul VOD      : {vod}")
    print(f"• Berkas Chat    : {chat_file}")
    print(f"• Transkrip      : {transkrip_file}")
    print(f"• URL Sumber     : {url}")
    print(f"• Headless Mode  : {args.headless}")
    print("=" * 60)

    # 1. Pra-agregasi data lokal
    print("\n[1/6] Membaca data chat & transkrip lokal...")
    chats = muat_livechat(chat_file)
    transkrips = muat_transkrip(transkrip_file)
    print(f"      Ditemukan {len(chats)} pesan chat dan {len(transkrips)} baris transkrip.")

    print("\n[2/6] Menghitung lonjakan reaksi CPM...")
    klaster = analisis_lonjakan_cpm(chats, transkrips, jendela_detik=20, pengali_cpm=2.0)
    print(f"      Teridentifikasi {len(klaster)} klaster momen potensial.")

    if not klaster:
        print("[ERROR] Tidak ada klaster chat yang terdeteksi.")
        sys.exit(1)

    # 2. Buka automasi peramban
    print("\n[3/6] Membuka Chromium & memverifikasi sesi login Gemini Pro...")
    profil_dir = dapatkan_path_profil_chrome(gunakan_profil_utama=args.main_profile)
    bot = GeminiWebAutomator(profil_dir, headless=args.headless, debug_port=args.debug_port)

    try:
        bot.buka_browser()
        bot.navigasi_ke_gemini()
        bot.pilih_model_argon_jika_ada()

        # 3. Bentuk linimasa livechat teragregasi dan lampirkan bersama transkrip
        berkas_terlampir = False
        target_lampiran = []
        if chat_file and Path(chat_file).exists():
            folder_cache = base_dir / "cache_chat"
            folder_cache.mkdir(parents=True, exist_ok=True)
            stem_nama = Path(chat_file).stem
            timeline_path = folder_cache / f"{stem_nama}_timeline.csv"
            print(f"[INFO] Menyusun linimasa chat kronologis teragregasi (30s) bebas pemicu filter...")
            if ekspor_livechat_timeline_csv:
                try:
                    ekspor_livechat_timeline_csv(chats, str(timeline_path), durasi_jendela_detik=30)
                    target_lampiran.append(str(timeline_path))
                    print(f"      [OK] Berkas linimasa chat aman disiapkan: {timeline_path.name}")
                except Exception as e_tl:
                    print(f"      [WARNING] Gagal membuat linimasa teragregasi: {e_tl}. Menggunakan chat asli...")
                    target_lampiran.append(chat_file)
            else:
                target_lampiran.append(chat_file)
        if transkrip_file and Path(transkrip_file).exists():
            target_lampiran.append(transkrip_file)

        if target_lampiran:
            print(f"\n[4/6] Melampirkan {len(target_lampiran)} berkas sumber aman ke Gemini Web:")
            berkas_terlampir = bot.lampirkan_berkas(target_lampiran)
        else:
            print("\n[4/6] Tidak ada berkas lampiran yang ditemukan, menggunakan data klaster prompt...")

        # 4. Injeksi prompt ringkas dan kirim
        print("\n[5/6] Menginjeksi prompt ringkas & mengirim ke model Argon...")
        prompt = buat_prompt_gemini_web(klaster, vtuber_name=vtuber, vod_title=vod, files_attached=berkas_terlampir)

        bot.injeksi_prompt(prompt)
        laporan_md = bot.kirim_dan_tunggu_respon(batas_waktu_detik=600)
        laporan_md = pangkas_laporan_bersih(laporan_md)

        # 5. Simpan hasil
        print("\n[6/6] Menyimpan hasil laporan markdown...")
        laporan_path = base_dir / "cache_chat" / "hasil_rangkuman.md"
        laporan_path.parent.mkdir(parents=True, exist_ok=True)
        laporan_path.write_text(laporan_md, encoding="utf-8")
        print(f"      Tersimpan di: {laporan_path}")

        if auto_folder and auto_folder.exists():
            safe_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in vod).strip()
            (auto_folder / f"FULL_{safe_title}_hasil_rangkuman.md").write_text(laporan_md, encoding="utf-8")
            (auto_folder / "hasil_rangkuman.md").write_text(laporan_md, encoding="utf-8")
            print(f"      • Rangkuman terarsip di channel: {auto_folder.name}")

        # 6. Urai timestamp ke sections.txt & DaVinci Markers
        segmen = ekstrak_segmen_dari_markdown(laporan_md)
        if segmen:
            target_sections = str(base_dir / args.output_sections)
            jumlah = simpan_ke_sections_txt(segmen, target_sections, youtube_url=url)
            print(f"      Berhasil menulis {jumlah} segmen ke: {target_sections}")

            # Ekspor Marker Hybrid
            edl_out = str(base_dir / "cache_chat" / "davinci_markers.edl")
            csv_out = str(base_dir / "cache_chat" / "davinci_markers.csv")
            if ekspor_ke_edl:
                ekspor_ke_edl(segmen, edl_out, fps=30.0, title="VTuber_Highlights")
                ekspor_ke_csv(segmen, csv_out, fps=30.0)
                print(f"      • File EDL : {edl_out}")
                print(f"      • File CSV : {csv_out}")

                if auto_folder and auto_folder.exists():
                    safe_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in vod).strip()
                    shutil.copy2(edl_out, auto_folder / f"FULL_{safe_title}_davinci_markers.edl")
                    shutil.copy2(edl_out, auto_folder / "davinci_markers.edl")
                    shutil.copy2(csv_out, auto_folder / f"FULL_{safe_title}_davinci_markers.csv")
                    shutil.copy2(csv_out, auto_folder / "davinci_markers.csv")
                    print(f"      • Marker terarsip di channel: {auto_folder.name}")

            if args.auto_marker and injeksi_marker_ke_resolve:
                sukses, pesan = injeksi_marker_ke_resolve(segmen)
                print(f"      • Injeksi DaVinci: {pesan}")
        else:
            print("      [WARNING] Timestamp tidak terdeteksi otomatis dari teks.")

        print("\n✨ SELESAI! Automasi Gemini Web (Mode B) berhasil tanpa biaya API.")
        print("=" * 60)

    except Exception as e:
        import traceback
        print("\n" + "=" * 60)
        print(f"[ERROR] Terjadi kesalahan fatal pada automasi: {e}")
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)
    finally:
        bot.tutup()


if __name__ == "__main__":
    main()
