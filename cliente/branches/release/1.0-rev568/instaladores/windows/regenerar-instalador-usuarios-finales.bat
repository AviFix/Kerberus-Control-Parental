copy ..\..\cliente\cliente.conf ArchivosDefault\cliente.conf
copy ..\..\cliente\conf\confspec.ini ArchivosDefault\confspec.ini

python ../common/pyinstaller-1.5.1/Configure.py

cd kerberus-daemon
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-1.5.1/Build.py -y cliente.spec
cd ..

cd kerberus-sync
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-1.5.1/Build.py -y sincronizadorCliente.spec
cd ..

cd Navegadores
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-1.5.1/Build.py -y navegadores.spec
cd ..

cd desinstalador
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-1.5.1/Build.py -y desinstalador.spec
cd ..

"C:\Archivos de programa\NSIS\makensis.exe" kerberus-usuarios-finales.nsi
pause


