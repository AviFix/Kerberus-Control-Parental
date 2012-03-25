# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '../../../cliente/sincronizadorCliente.py'],
             pathex=['../../../cliente/conf','../../../cliente/clases','../../../cliente/password'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/sincronizadorCliente', 'sincronizadorCliente.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=0 )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'sincronizadorCliente'))
