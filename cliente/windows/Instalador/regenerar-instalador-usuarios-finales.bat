copy ..\..\cliente.conf ArchivosDefault\cliente.conf
copy ..\..\conf\confspec.ini ArchivosDefault\confspec.ini
pause
cd kerberus-daemon
C:\Python27\python setup.py py2exe
cd ..
cd kerberus-sync
C:\Python27\python setup.py py2exe
cd ..
cd Navegadores
C:\Python27\python setup.py py2exe
cd ..
cd desinstalador
C:\Python27\python setup.py py2exe
cd ..
"C:\Archivos de programa\NSIS\makensis.exe" kerberus-usuarios-finales.nsi
pause


