# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['start.py'],
    pathex=[],
    binaries=[],
    datas=[('IFPSystem', 'IFPSystem'), ('IFPWebApp', 'IFPWebApp'), ('IFPWebApp/templates', 'IFPWebApp/templates'), ('staticfiles', 'staticfiles'), ('newdb', '.'), ('homeaffairsdb', '.'), ('venv\\Lib\\site-packages\\face_recognition_models\\models', 'face_recognition_models/models')],
    hiddenimports=['IFPWebApp', 'IFPWebApp.templatetags', 'IFPWebApp.routers', 'channels', 'channels.layers', 'rest_framework', 'rest_framework.authtoken', 'django.contrib.auth', 'django.contrib.sessions', 'django.contrib.admin', 'django.contrib.contenttypes', 'django.contrib.messages', 'django.contrib.staticfiles.templatetags.staticfiles', 'face_recognition_models'],
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
    name='InsuranceSystem',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InsuranceSystem',
)
