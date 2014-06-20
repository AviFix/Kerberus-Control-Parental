copy ..\..\cliente.conf ArchivosDefault\cliente.conf /Y
copy ..\..\kerby.ico ArchivosDefault\kerby.ico /Y

copy ..\..\conf\confspec.ini ArchivosDefault\confspec.ini /Y
copy "LSP - Kerberus\inst_lsp.exe" ArchivosDefault\inst_lsp.exe /Y
copy "LSP - Kerberus\klsp.dll" ArchivosDefault\klsp.dll /Y

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

cd kerberus-systemTray
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR systemtray.spec
cd ..

cd desinstalador
rmdir /S /Q build
rmdir /S /Q dist
python ../../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR desinstalador.spec
cd ..

"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 desinstalador\dist\uninstall\uninstall.exe
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 kerberus-daemon\dist\client\kerberus.exe
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 kerberus-sync\dist\sync\kerberus-sync.exe
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 Navegadores\dist\checkNavs\kerberus-nav.exe
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 kerberus-systemtray\dist\systemtray\kerberusTray.exe
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 ArchivosDefault\klsp.dll
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 ArchivosDefault\inst_lsp.exe
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 ArchivosDefault\klsp32.dll
"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 ArchivosDefault\inst_lsp32.exe

"C:\Archivos de programa\NSIS\makensis.exe" kerberus-undirectorio.nsi

"C:\Archivos de programa\Microsoft SDKs\Windows\v7.0A\bin\signtool" sign -t http://time.certum.pl -f F:\kerberus.p12 -p cr1pt0man0 Kerberus.exe

copy Kerberus.exe f:\ /Y

pause