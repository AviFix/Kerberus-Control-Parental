@echo off
windres.exe proxocket.rc proxocket_rc.o

echo ----------
echo - ws2_32 -
echo ----------
gcc -s -O2 -mtune=generic -Wall -Wextra -Wunused -Wshadow -shared -enable-stdcall-fixup -o ..\ws2_32.dll ws2_32.c ws2_32.def proxocket_rc.o %1

echo .

echo -----------
echo - wsock32 -
echo -----------
gcc -s -O2 -mtune=generic -Wall -Wextra -Wunused -Wshadow -shared -enable-stdcall-fixup -o ..\wsock32.dll wsock32.c wsock32.def proxocket_rc.o %1

del proxocket_rc.o
