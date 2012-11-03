cd migrador
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR migrador.spec
cd ..

"C:\Archivos de programa\NSIS\makensis.exe" update1.0-1.1-silent.nsi
pause


