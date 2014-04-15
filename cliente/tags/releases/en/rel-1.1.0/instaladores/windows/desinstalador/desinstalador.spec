# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '../../../password/uninstall.py'],
             pathex=['../../../clases','../../../','../../../conf','../../../password'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/uninstall', 'uninstall.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=0,
          icon='../kerby.ico' )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'uninstall'))
