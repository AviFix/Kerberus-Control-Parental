!include <win32.mak>

.cpp.obj:
	cl -c -DCRTAPI1=_cdecl -DCRTAPI2=_cdecl -nologo -GS -D_X86_=1  -DWIN32 -D_WIN32 -W3 -D_WINNT -D_WIN32_WINNT=0x0500 -DNTDDI_VERSION=0x05000000 -D_WIN32_IE=0x0500 -DWINVER=0x0500  -D_MT -D_DLL -MD -DSTRICT -DNODEBUG  $<

CPP_FILES= dbuffmgr.cpp\
           doverlap.cpp\
	     dasyncw.cpp\
          dworker.cpp\
           dcatalog.cpp\
           dcatitem.cpp\
           dllmain.cpp\
           dprovide.cpp\
           dsocket.cpp\
           spi.cpp\
           trace.cpp\
           dthook.cpp


OBJS= $(CPP_FILES:.cpp=.obj)

all: klsp.dll inst_lsp.exe

klsp.dll: $(OBJS)
	$(link) $(dlllflags) \
    -map \
	-export:WSPStartup \
	-out:$*.dll $(OBJS) $(guilibsdll) ws2_32.lib

inst_lsp.obj: inst_lsp.cpp
	cl -c -DCRTAPI1=_cdecl -DCRTAPI2=_cdecl -nologo -GS -D_X86_=1  -DWIN32 -D_WIN32 -W3 -D_WINNT -D_WIN32_WINNT=0x0500 -DNTDDI_VERSION=0x05000000 -D_WIN32_IE=0x0500 -DWINVER=0x0500  -D_MT -MT inst_lsp.cpp

inst_lsp.exe: inst_lsp.obj
	$(link) $(conlflags) -out:$*.exe inst_lsp.obj\
        rpcrt4.lib $(conlibs) ws2_32.lib sporder.lib

clean:
    -del *.obj
	-del *.dll
	-del *.pch
	-del *.exp
	-del lsp.lib
