# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

REPO_ROOT = Path(SPECPATH).resolve().parent
SOURCE_DIR = REPO_ROOT / "src"
SOURCE_FILE = SOURCE_DIR / "VideoConvertPro_EN.py"
ICON_FILE = REPO_ROOT / "assets" / "icon.ico"

datas = [(str(ICON_FILE), ".")]
binaries = []
hiddenimports = ["tkinterdnd2", "ctypes", "_ctypes"]

dnd_data, dnd_binaries, dnd_hiddenimports = collect_all("tkinterdnd2")
datas += dnd_data
binaries += dnd_binaries
hiddenimports += dnd_hiddenimports

a = Analysis(
    [str(SOURCE_FILE)],
    pathex=[str(SOURCE_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VideoConvertPro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(ICON_FILE)],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="VideoConvertPro",
)
