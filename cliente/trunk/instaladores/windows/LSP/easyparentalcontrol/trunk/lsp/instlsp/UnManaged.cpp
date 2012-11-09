
#pragma unmanaged

#include <ws2spi.h>
#include <windows.h>
#define STRSAFE_NO_DEPRECATE
#include <strsafe.h>
#include <mswsock.h>
#include <ws2tcpip.h>
#include <mstcpip.h>
#include <winsock2.h>
#include <stdio.h>
#include <stdlib.h>
#include <sporder.h>

//#include "GlobalVars.h"


//
// Function: DllMain
//
// Description:
//    Provides initialization when the LSP DLL is loaded. In our case we simply,
//    initialize some critical sections used throughout the DLL.
//
//BOOL WINAPI 
//DllMain(
//    IN HINSTANCE hinstDll, 
//    IN DWORD dwReason, 
//    LPVOID lpvReserved
//    )
//{
//    switch (dwReason)
//    {
//
//        case DLL_PROCESS_ATTACH:
//			
//        case DLL_THREAD_ATTACH:
//            break;
//
//        case DLL_THREAD_DETACH:
//            break;
//
//        case DLL_PROCESS_DETACH:
//            break;
//    }
//
//    return TRUE;
//
//cleanup:
//
//    return FALSE;
//}


void dbgprint(
    char *format,
    ...
    )
{
    va_list vl;
    char    dbgbuf1[2048],
            dbgbuf2[2048];


    va_start(vl, format);
    StringCbVPrintf(dbgbuf1, sizeof(dbgbuf1),format, vl);
    StringCbPrintf(dbgbuf2, sizeof(dbgbuf2),"%s\r\n",  dbgbuf1);
    va_end(vl);

    OutputDebugString(dbgbuf2);
}
