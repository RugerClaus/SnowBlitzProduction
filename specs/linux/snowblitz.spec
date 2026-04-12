# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/home/rugerclaus/SnowBlitzProduction/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/rugerclaus/SnowBlitzProduction/assets', 'assets'), ('/home/rugerclaus/SnowBlitzProduction/logs', 'logs'), ('/home/rugerclaus/SnowBlitzProduction/saves', 'saves'), ('/home/rugerclaus/SnowBlitzProduction/environment', 'environment')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='snowblitz',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/images/build/linux.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='snowblitz',
)
