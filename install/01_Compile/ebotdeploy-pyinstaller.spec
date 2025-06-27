# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['ecuapass_commander.py'],
    pathex=[],
    binaries=[],
    datas=[('info', 'info'), ('resources/data_ecuapass/*.txt', 'resources/data_ecuapass/'), ('resources/docs/*.png', 'resources/docs/'), ('resources/docs/*.pdf', 'resources/docs/'), ('resources/docs/*.json', 'resources/docs/')],
    hiddenimports=['info', 'googleapiclient', 'googleapiclient.discovery'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # Exclude source files
    noarchive=False,
    optimize=0,
)

#
## Ensure only compiled files are included
#for d in a.datas[:]:
#    if d[0].endswith('.py'):
#        a.datas.remove(d)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ecuapass_commander',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    manifest="admin.manifest"
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ecuapass_commander',
)
