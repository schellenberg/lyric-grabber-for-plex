# -*- mode: python ; coding: utf-8 -*-
"""
Example build.spec file

This hits most of the major notes required for
building a stand alone version of your Gooey application.
"""


import os
import platform
import gooey
gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

from PyInstaller.building.api import EXE, PYZ, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.osx import BUNDLE

block_cipher = None

a = Analysis(['lyric-grabber-for-plex.py'],  # replace me with your path
             pathex=['/Users/dan/Documents/GitHub/plex-lyric-grabber/lyric-grabber-for-plex.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False
             )
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

options = [('u', None, 'OPTION'), ('v', None, 'OPTION'), ('w', None, 'OPTION')]


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Lyric Grabber for Plex',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon=os.path.join(gooey_root, 'images', 'program_icon.ico'))

info_plist = {'NSHighResolutionCapable': 'True'}
app = BUNDLE(exe,
             name='Lyric Grabber for Plex.app',
             bundle_identifier=None,
             info_plist=info_plist
            )
