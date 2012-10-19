python ../common/pyinstaller-1.5.1/Configure.py

cd migrador
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-1.5.1/Build.py -y migrador.spec
cd ..

"C:\Archivos de programa\NSIS\makensis.exe" update1.0-1.1-silent.nsi
pause


