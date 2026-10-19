"""
PyInstaller Hook khusus untuk pustaka Playwright.
Memastikan seluruh driver Node.js bawaan Playwright (node.exe dan bundle package),
metadata, dan hidden imports (greenlet, pyee, dll) terbawa utuh ke dalam biner distribusi.
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Kumpulkan seluruh data, biner, dan submodul Playwright
datas, binaries, hiddenimports = collect_all("playwright")

# Tambahkan hidden imports penting yang sering terlewat oleh PyInstaller
hiddenimports += [
    "playwright.sync_api",
    "playwright._impl._driver",
    "greenlet",
    "pyee",
    "pyee.asyncio",
    "pyee.base"
]

# Pastikan folder driver Playwright (driver/node.exe dan driver/package) terkumpul
try:
    datas += collect_data_files("playwright.driver")
except Exception:
    pass
