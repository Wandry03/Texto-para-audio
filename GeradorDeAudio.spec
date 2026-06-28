# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gerador_audio_gui.pyw'],
    pathex=[
        r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\Lib',
    ],
    binaries=[
        (r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\DLLs\_tkinter.pyd', '.'),
        (r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\DLLs\tcl86t.dll', '.'),
        (r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\DLLs\tk86t.dll', '.'),
    ],
    datas=[
        (r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\Lib\tkinter', 'tkinter'),
        (r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\tcl\tcl8.6', 'tcl/tcl8.6'),
        (r'C:\Users\pc1\AppData\Local\Python\pythoncore-3.14-64\tcl\tk8.6', 'tcl/tk8.6'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.messagebox',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[
        'pyinstaller_tk_runtime.py',
    ],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GeradorDeAudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
