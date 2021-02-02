# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

wd = os.path.realpath('.')
icon_path = os.path.join(wd, 'resources', 'images', 'logo.ico')

print(f'wd: {wd}, icon_path: {icon_path}')

a = Analysis(['qmlview.py'],
             pathex=[wd],
             binaries=[],
             datas=[(os.path.join(wd, "_qmlview_resource_.rcc"), ".")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='qmlview',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon=icon_path,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='qmlview')
