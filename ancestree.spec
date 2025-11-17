# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Ancestree launcher

import os
import sys

block_cipher = None

# Platform-specific icon handling
icon_file = None
if sys.platform == 'win32':
    if os.path.exists('assets/icon.ico'):
        icon_file = 'assets/icon.ico'
elif sys.platform == 'darwin':
    if os.path.exists('assets/icon.icns'):
        icon_file = 'assets/icon.icns'
elif sys.platform.startswith('linux'):
    if os.path.exists('assets/icon.png'):
        icon_file = 'assets/icon.png'

a = Analysis(
    ['scripts/launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('docs/FOR_USERS.md', 'docs'),
        ('docs/FOR_DEVELOPERS.md', 'docs'),
        ('docs/INSTALLATION_GUIDE.md', 'docs'),
        ('docker-compose.yml', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'subprocess',
        'threading',
        'webbrowser',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Ancestree',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window on Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

# macOS app bundle (only created on macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Ancestree.app',
        icon=icon_file,
        bundle_identifier='com.ancestree.launcher',
        info_plist={
            'CFBundleName': 'Ancestree',
            'CFBundleDisplayName': 'Ancestree',
            'CFBundleGetInfoString': "Build and explore your family tree",
            'CFBundleIdentifier': "com.ancestree.launcher",
            'CFBundleVersion': "1.0.0",
            'CFBundleShortVersionString': "1.0.0",
            'NSHumanReadableCopyright': "Copyright © 2024 Ancestree",
            'NSHighResolutionCapable': 'True',
        },
    )
