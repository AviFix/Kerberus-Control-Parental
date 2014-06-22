# -*- mode: python -*-
a = Analysis(['../../../systemTray.py'],
        pathex=['../../../clases','../../../','../../../conf','../../../adminpanel'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/systemtray', 'kerberusTray.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=0,
          icon='../kerby.ico' )
coll = COLLECT( exe,
              Tree('./imagenes'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'systemtray'))

