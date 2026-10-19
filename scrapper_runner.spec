# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['I:\\My Drive\\Kerja\\Scrapper_new_acmt\\scrapper_runner.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['playwright', 'playwright.sync_api', 'playwright._impl._driver', 'greenlet', 'openpyxl', 'cryptography', 'pyautogui', 'pyperclip', 'psutil', 'xlwt', 'win32com', 'win32com.client', 'pythoncom', 'runner.security_guard'],
    hookspath=['I:\\My Drive\\Kerja\\Scrapper_new_acmt\\vibe_tools\\hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'IPython', 'matplotlib'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='scrapper_runner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='scrapper_runner',
)
