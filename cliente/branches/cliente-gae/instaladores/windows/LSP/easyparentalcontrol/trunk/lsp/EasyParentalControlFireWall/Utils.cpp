#pragma unmanaged

#include "StdAfx.h"

#include "Types.h"
#include "GlobalVars.h"


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
    static  DWORD pid=0;
    va_list vl;
    char    dbgbuf1[2048],
            dbgbuf2[2048];

    // Prepend the process ID to the message
    if ( 0 == pid )
    {
        pid = GetCurrentProcessId();
    }

    EnterCriticalSection(&GlobalVars::gDebugCritSec);
    va_start(vl, format);
    StringCbVPrintf(dbgbuf1, sizeof(dbgbuf1),format, vl);
    StringCbPrintf(dbgbuf2, sizeof(dbgbuf2),"%lu: %s\r\n", pid, dbgbuf1);
    va_end(vl);

    OutputDebugString(dbgbuf2);
    LeaveCriticalSection(&GlobalVars::gDebugCritSec);
}
