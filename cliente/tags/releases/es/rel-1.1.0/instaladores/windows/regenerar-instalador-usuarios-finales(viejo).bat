copy ..\..\cliente.conf ArchivosDefault\cliente.conf /Y
copy ..\..\conf\confspec.ini ArchivosDefault\confspec.ini /Y

cd kerberus-daemon
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR cliente.spec
cd ..

cd kerberus-sync
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR sincronizadorCliente.spec
cd ..

cd Navegadores
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR navegadores.spec
cd ..

cd desinstalador
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR desinstalador.spec
cd ..

"C:\Archivos de programa\NSIS\makensis.exe" kerberus-usuarios-finales.nsi
pause


