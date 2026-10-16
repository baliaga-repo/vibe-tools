# 🔄 Panduan Sinkronisasi Git Submodule `vibe_tools`

Dokumen ini menjelaskan alur lengkap untuk **mengambil pembaruan (Pull)** dari repositori induk [baliaga-repo/vibe-tools](https://github.com/baliaga-repo/vibe-tools.git) ke dalam proyek kerja Anda, serta **mengirimkan kontribusi lokal (Push)** kembali ke GitHub.

---

## 🧭 Gambaran Arsitektur

Direktori `vibe_tools/` di dalam proyek ini didaftarkan sebagai **Git Submodule** melalui file `.gitmodules`:

```ini
[submodule "vibe_tools"]
	path = vibe_tools
	url = https://github.com/baliaga-repo/vibe-tools.git
```

Artinya:
- Proyek utama (misal: `Scrapper_new_acmt`) menyimpan referensi **ID Commit** tertentu dari repositori `vibe-tools`.
- Repositori `vibe-tools` memiliki siklus *commit* dan riwayat Git independen.

---

## 📥 Skenario 1: Mengambil Pembaruan dari GitHub (Pull / Sync)

Gunakan alur ini saat repositori https://github.com/baliaga-repo/vibe-tools.git telah diperbarui (fitur baru, perbaikan bug, atau penambahan skrip) dan Anda ingin menyinkronkannya ke dalam proyek ini.

### Langkah 1: Bersihkan Gangguan `desktop.ini` (Khusus Windows / Google Drive)
Jika repositori berada di dalam folder yang disinkronkan Google Drive di Windows, berkas tersembunyi `desktop.ini` sering terbuat di dalam struktur folder internal Git (`.git/modules/vibe_tools/refs/`), memicu pesan error:
```text
fatal: bad object refs/desktop.ini
```

Jalankan perintah PowerShell ini untuk membersihkannya secara aman:
```powershell
Get-ChildItem -Path .git -Filter "desktop.ini" -Recurse -Force | Remove-Item -Force
```

### Langkah 2: Ambil Pembaruan Terbaru (Fetch & Pull)

**Opsi A: Langsung dari Root Proyek via Submodule CLI (Direkomendasikan)**
```powershell
git submodule update --remote --merge vibe_tools
```

**Opsi B: Menggunakan Perintah Git Terarah ke Subfolder**
```powershell
# Simpan perubahan lokal sementara jika ada file yang diedit
git -C vibe_tools stash

# Tarik commit terbaru dari branch main
git -C vibe_tools pull origin main

# Kembalikan perubahan lokal jika sebelumnya di-stash
git -C vibe_tools stash pop
```

### Langkah 3: Catat Referensi Commit Baru di Proyek Utama
Setelah isi `vibe_tools` terbarui, Git pada repositori utama akan mendeteksi perubahan pointer subproject:
```powershell
git status -s
# Hasil: M vibe_tools
```

Simpan perubahan pointer commit ini ke riwayat Git proyek utama Anda:
```powershell
git add vibe_tools
git commit -m "chore: perbarui submodule vibe_tools ke versi terbaru"
```

---

## 📤 Skenario 2: Mengirimkan Pembaruan Lokal ke GitHub (Push)

Gunakan alur ini jika Anda baru saja menambahkan atau memodifikasi berkas di dalam `vibe_tools/` (misalnya menambah skrip baru atau memperbarui panduan) dan ingin mempublikasikannya ke repositori GitHub `vibe-tools`.

### Langkah 1: Menggunakan Skrip Otomatis `push_to_github.py`
Di dalam `vibe_tools/` sudah tersedia skrip pembantu yang otomatis membersihkan `desktop.ini`, memvalidasi remote, dan meminta pesan commit:

```powershell
# Jalankan skrip pendorong
python vibe_tools/push_to_github.py
```

### Langkah 2: Alternatif Manual via Git CLI
Jika Anda ingin mengeksekusinya secara manual langkah-demi-langkah:
```powershell
# Bersihkan desktop.ini di dalam vibe_tools
Get-ChildItem -Path vibe_tools -Filter "desktop.ini" -Recurse -Force | Remove-Item -Force

# Lakukan commit di dalam folder submodule
git -C vibe_tools add .
git -C vibe_tools commit -m "feat/fix: deskripsi perubahan fitur"
git -C vibe_tools push origin main
```

### Langkah 3: Perbarui Pointer di Proyek Utama
Setelah berhasil di-push ke GitHub, perbarui juga pointer submodule di proyek utama:
```powershell
git add vibe_tools
git commit -m "chore: perbarui pointer commit vibe_tools setelah push"
```

---

## 🚀 Skenario 3: Clone Proyek Baru yang Memiliki `vibe_tools`

Jika Anda berpindah komputer atau melakukan clone proyek dari awal:

### Opsi 1: Clone Sekaligus Submodule (1 Langkah)
```bash
git clone --recurse-submodules https://github.com/baliaga-repo/Scrapper_new_acmt.git
```

### Opsi 2: Inisialisasi Submodule Setelah Clone Biasa
Jika proyek sudah terlanjur di-clone tanpa flag `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

---

## 📋 Tabel Rangkuman Perintah Singkat

| Tindakan | Perintah PowerShell / Bash |
| :--- | :--- |
| **Bersihkan Cache GDrive** | `Get-ChildItem -Path .git -Filter "desktop.ini" -Recurse -Force \| Remove-Item -Force` |
| **Pull Update GitHub** | `git submodule update --remote --merge vibe_tools` |
| **Cek Perubahan Lokal** | `git -C vibe_tools status -s` |
| **Push via Skrip Helper** | `python vibe_tools/push_to_github.py` |
| **Push Manual** | `git -C vibe_tools add . && git -C vibe_tools commit -m "update" && git -C vibe_tools push origin main` |
| **Kunci Pointer di Induk** | `git add vibe_tools && git commit -m "chore: update submodule pointer"` |
