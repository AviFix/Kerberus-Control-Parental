//   This file is part of the EasyParentalControl Project.
//
//   EasyParentalControl is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   EasyParentalControl is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.

//   You should have received a copy of the GNU General Public License
//   along with EasyParentalControl.  If not, see <http://www.gnu.org/licenses/>.

// Parts of this file is derived from the winsock lsp sample, that can be found in the Microsoft Windows SDK v7.0 

//
// Module Name: instlsp.cpp
//
// Description:
//
//    This sample illustrates how to develop a layered service provider.
//    This LSP is simply a pass through sample which counts the bytes transfered
//    on each socket. 
//
//    This file contains an installation program to insert the layered sample
//    into the Winsock catalog of providers.
//    
//
// Compile:
//
//    Compile with the Makefile:
//      nmake /f Makefile
//
// Execute:
//
// See Source function usage() for parameters
//
//    This project produces a executable file instlsp.exe. The installation app
//    allows you to install the LSP over any provider. Note however that if you
//    choose to install over a single provider, you should install over all 
//    providers of that address family (e.g. if you install over UDP, install
//    over TCP and RAW providers as well). The arguments are:
//
//
//    For example, first print out the catalog:
//       instlsp.exe -p
//        1001 - MSAFD ATM AAL5
//        1002 - MSAFD Tcpip [TCP/IP]
//        1003 - MSAFD Tcpip [UDP/IP]
//        1004 - MSAFD Tcpip [RAW/IP]
//        1005 - RSVP UDP Service Provider
//        1006 - RSVP TCP Service Provider
//        1019 - MSAFD AppleTalk [ADSP]
//        1020 - MSAFD AppleTalk [ADSP] [Pseudo Stream]
//        1021 - MSAFD AppleTalk [PAP]
//        1022 - MSAFD AppleTalk [RTMP]
//        1023 - MSAFD AppleTalk [ZIP]
//
//    To install over AppleTalk
//       instlsp.exe -i -o 1019 -o 1020 -o 1021 -o 1022 -o 1023 -n "EasyParentalControl LSP" -d c:\path\lsp.dll
//
//    Print the new catalog out:
//       instlsp.exe -p
//        1041 - EasyParentalControl LSP over [MSAFD AppleTalk [ADSP]]
//        1042 - EasyParentalControl LSP over [MSAFD AppleTalk [PAP]]
//        1043 - EasyParentalControl LSP over [MSAFD AppleTalk [RTMP]]
//        1044 - EasyParentalControl LSP over [MSAFD AppleTalk [ZIP]]
//        1001 - MSAFD ATM AAL5
//        1002 - MSAFD Tcpip [TCP/IP]
//        1003 - MSAFD Tcpip [UDP/IP]
//        1004 - MSAFD Tcpip [RAW/IP]
//        1005 - RSVP UDP Service Provider
//        1006 - RSVP TCP Service Provider
//        1019 - MSAFD AppleTalk [ADSP]
//        1020 - MSAFD AppleTalk [ADSP] [Pseudo Stream]
//        1021 - MSAFD AppleTalk [PAP]
//        1022 - MSAFD AppleTalk [RTMP]
//        1023 - MSAFD AppleTalk [ZIP]
//        1040 - EasyParentalControl LSP
//
//    To remove the LSP, supply the catalog ID of the hidden entry to remove:
//       instlsp.exe -r 1040 
//
//    In case all else fails (removes all LSPs installed):
//       instlsp.exe -f
//
#include "instlsp.h"


struct InstLspArgs
{
	char				*lpszProgramName;
    DWORD               dwCatalogIdArrayCount;       // How many to install over
	DWORD				*pdwCatalogIdArray;
    BOOL                bInstall,
						bRemove,
                        bInstallOverAll,
                        bRemoveAllLayeredEntries,
                        bPrintProviders,
                        bDisplayOnlyLayeredEntries,
                        bVerbose,
                        bMapLsp,
                        bIFSProvider;
    char                *lpszLspName,
                        *lpszLspPathAndFile,
                        *lpszLspPathAndFile32;
	DWORD               dwRemoveCatalogId;
    WINSOCK_CATALOG     eCatalog;
	char				*lpszDebugExecutable;
};
 
//
// Global variable: Function pointer to WSCUpdateProvider if on Windows XP or greater.
//                  Uninstalling an LSP when other LSPs are layered over it is really
//                  difficult; however on Windows XP and greater the WSCUpdateProvider
//                  function makes this much simpler. On older platforms its a real
//                  pain.
LPWSCUPDATEPROVIDER fnWscUpdateProvider   = NULL,
                    fnWscUpdateProvider32 = NULL;
HMODULE             gModule = NULL;
GUID                gProviderGuid;

// Prototype for usage information
void usage( __in_z char *progname );





////////////////////////////////////////////////////////////////////////////////
//
// Implementation
//
////////////////////////////////////////////////////////////////////////////////
bool ParseArgs(
	int argc, char* argv[],
	InstLspArgs& args)
{	
	INT i;
    int                 rc;

	args.lpszProgramName = argv[ 0 ];
    args.dwCatalogIdArrayCount = 0;
	args.pdwCatalogIdArray = NULL;
    args.bInstall = false;
	args.bRemove = false;
    args.bInstallOverAll = false;
    args.bRemoveAllLayeredEntries = false;
    args.bPrintProviders = false;
    args.bDisplayOnlyLayeredEntries = false;
    args.bVerbose = false;
    args.bMapLsp = false;
    args.bIFSProvider = false;
    args.lpszLspName = NULL;
    args.lpszLspPathAndFile = NULL;
    args.lpszLspPathAndFile32 = NULL;
	args.dwRemoveCatalogId = 0;
	args.lpszDebugExecutable = NULL;
#ifdef _WIN64
    args.eCatalog        = LspCatalog64Only;
#else
    args.eCatalog        = LspCatalog32Only;
#endif
    // First count how many catalog parameters are supplied so we can dynamically
    // allocate the right sized buffer
    for(i=1; i < argc ;i++)
    {
        if ( strncmp( argv[ i ], "-o", 2 ) == 0 )
            args.dwCatalogIdArrayCount++;
    }

    // Allocate space for the array of catalog IDs
    if ( args.dwCatalogIdArrayCount > 0 )
    {
        args.pdwCatalogIdArray = (DWORD *) LspAlloc(
                sizeof( DWORD ) * args.dwCatalogIdArrayCount, // this star as multiply
                &rc
                );
        if ( NULL == args.pdwCatalogIdArray )
        {
            return false;
        }
    }

    // Set back to zero so we can use it as the index into our array
    int dwCatalogIdArrayCount = 0;

    // Parse the command line
    for(i=1; i < argc ;i++)
    {
        if ( ( 2   != strlen( argv[i] ) ) && 
             ( '-' != argv[i][0] ) && 
             ( '/' != argv[i][0] )
           )
        {
            return false;
        }

        switch ( tolower( argv[i][1] ) )
        {
            case 'a':               // Install LSP over all currently installed providers
                args.bInstallOverAll = TRUE;
                break;

            case 'c':               // For 64-bit: which catalog to operate on?
                if (i+1 >= argc) return false;

                switch (tolower(argv[i+1][0]))
                {
                    case 'b':       // Both Winsock catalogs
                        args.eCatalog = LspCatalogBoth;
                        break;
                    case '6':       // 64-bit Winsock catalog only
                        args.eCatalog = LspCatalog64Only;
                        break;
                    case '3':       // 32-bit Winsock catalog only
                        args.eCatalog = LspCatalog32Only;
                        break;
                    default:
                        return false;
                        break;
                }
                i++;
                break;

            case 'd':               // Full path and filename to LSP
                if ( i+1 >= argc ) return false;
                if (_strnicmp(argv[i], "-d32", 4)==0)
				{
                    args.lpszLspPathAndFile32 = argv[ ++i ];
				}
                else
				{
                    args.lpszLspPathAndFile = argv[ ++i ];
				}

                break;

            case 'f':               // Uninstall all layered providers
                args.bRemoveAllLayeredEntries = TRUE;
                args.bRemove = TRUE;
                break;

            case 'h':               // Install as an IFS provider
                args.bIFSProvider = TRUE;
                break;

            case 'i':               // install
                args.bInstall = TRUE;
                break;

            case 'l':               // print the layered providers only
                args.bPrintProviders = TRUE;
                args.bDisplayOnlyLayeredEntries = TRUE;
                break;

            case 'm':               // Map and print the LSP structure
                args.bMapLsp = TRUE;
                args.bInstall = FALSE;
                break;

            case 'n':               // name of the LSP to install (not the DLL name)
                if (i+1 >= argc) return false;

                args.lpszLspName = argv[++i];
                break;

            case 'o':               // catalog id (to install over)
                if (i+1 >= argc) return false;

                args.pdwCatalogIdArray[dwCatalogIdArrayCount++] = atoi(argv[++i]);
                break;

            case 'p':               // print the catalog
                args.bPrintProviders = TRUE;
                args.bDisplayOnlyLayeredEntries = FALSE;
                break;

            case 'r':               // remove an LSP
                args.bInstall = FALSE;
                if (i+1 >= argc) return false;
                args.dwRemoveCatalogId = atol(argv[++i]);
                break;

            case 'v':               // verbose mode (when printing with -p option)
                args.bVerbose = TRUE;
                break;

			case 'x':
				args.bInstall = true;
				args.bRemove = true;
				if (i+1>=argc) return false;
				args.lpszDebugExecutable = argv[ ++i ];
				break;

            default:
                return false;
                break;
        }
    }
	return true;
}


void main1(
	InstLspArgs& args,
	LPWSAPROTOCOL_INFOW& pProtocolInfo,
    LSP_ENTRY*& pLspMap,
    INT& iLspCount
	)
{
    WSADATA             wsd;
    INT                 iTotalProtocols = 0,
                        i;
    int                 rc;

    ////////////////////////////////////////////////////////////////////////////
    //
    // Initialization and Command Line Parsing
    //
    ////////////////////////////////////////////////////////////////////////////

    // Load Winsock
    rc = WSAStartup( MAKEWORD(2,2), &wsd );
    if ( 0 != rc )
    {
        fprintf( stderr, "Unable to load Winsock: %d\n", rc );
        return;
    }

    // Initialize data structures
    LspCreateHeap( &rc );

    __try
    {
        InitializeCriticalSection( &gDebugCritSec );
    }
    __except( EXCEPTION_EXECUTE_HANDLER )
    {
        return;
    }




#ifndef _WIN64
    if ( LspCatalog64Only == args.eCatalog )
    {
        fprintf(stderr, "\n\nUnable to manipulate 64-bit Winsock catalog from 32-bit process!\n\n");
        return;
    }
#endif


    gModule = LoadUpdateProviderFunction();

    if ( TRUE == args.bPrintProviders )
    {
        // Print the 32-bit catalog
        if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog32Only == args.eCatalog ) )
        {
            printf( "\n\nWinsock 32-bit Catalog:\n" );
            printf( "=======================\n" );
            PrintProviders( LspCatalog32Only, args.bDisplayOnlyLayeredEntries, args.bVerbose );
        }
        // Print the 64-bit catalog
        if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog64Only == args.eCatalog ) )
        {
            printf( "\n\nWinsock 64-bit Catalog:\n" );
            printf( "=======================\n" );
            PrintProviders( LspCatalog64Only, args.bDisplayOnlyLayeredEntries, args.bVerbose );
        }
    }
    if ( TRUE == args.bInstall )
    {
        if ( NULL == args.lpszLspPathAndFile )
        {
            fprintf( stderr, "\n\nError! Please specify path and filename of LSP!\n\n");
            return;
        }

        if ( TRUE == args.bInstallOverAll )
        {
            // Make sure user didn't specify '-a' and '-o' flags
            if ( 0 != args.dwCatalogIdArrayCount )
            {
                fprintf( stderr, "\n\nError! Cannot specify both '-a' and '-o' flags!\n\n" );
                return;
            }

            // Enumerate the appropriate catalog we will be working on
            pProtocolInfo = EnumerateProviders( args.eCatalog, &iTotalProtocols );
            if ( NULL == pProtocolInfo )
            {
                fprintf( stderr, "%s: EnumerateProviders: Unable to enumerate Winsock catalog\n",
                        args.lpszProgramName
                        );
                return;
            }

            // Count how many non layered protocol entries there are
            for(i=0; i < iTotalProtocols ;i++)
            {
                if ( LAYERED_PROTOCOL != pProtocolInfo[ i ].ProtocolChain.ChainLen )
                    args.dwCatalogIdArrayCount++;
            }
			
            // Allocate space for all the entries
            args.pdwCatalogIdArray = (DWORD *) LspAlloc(
                    sizeof( DWORD ) * args.dwCatalogIdArrayCount,
                   &rc
                    );
            // perhaps we should free the old one?

			if ( NULL == args.pdwCatalogIdArray )
            {
                fprintf( stderr, "%s: LspAlloc failed: %d\n", args.lpszProgramName, rc );
                return;
            }

            // Get the catalog IDs for all existing providers
            args.dwCatalogIdArrayCount = 0 ;

	    // Agregado por mi
	    const wchar_t* protocoloTCPIP = L"[TCP/IP]";
	    //

            for(i=0; i < iTotalProtocols ;i++)
            {
                if ( LAYERED_PROTOCOL != pProtocolInfo[ i ].ProtocolChain.ChainLen )
                {
					// Agregado por  mi					
					if ( wcsstr(pProtocolInfo[ i ].szProtocol, protocoloTCPIP ) != NULL ){
						printf("Detectado el protocolo TCP-IP en: %S - ID: %d\n, agregando", pProtocolInfo[ i ].szProtocol, pProtocolInfo[ i ].dwCatalogEntryId);
						args.pdwCatalogIdArray[ args.dwCatalogIdArrayCount++ ] = pProtocolInfo[ i ].dwCatalogEntryId;
					}
                }
            }

            FreeProviders( pProtocolInfo );
            pProtocolInfo = NULL;
        }

        // Install the LSP with the supplied parameters
        rc = InstallLsp(
                args.eCatalog,
                args.lpszLspName,
                args.lpszLspPathAndFile,
                args.lpszLspPathAndFile32,
                args.dwCatalogIdArrayCount,
                args.pdwCatalogIdArray,
                args.bIFSProvider,
                args.bInstallOverAll
                );
    }
    if ( TRUE == args.bMapLsp )
    {
        // Display the 32-bit LSP catalog map
        if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog32Only == args.eCatalog ) )
        {
            printf("\n32-bit Winsock LSP Map:\n\n");

            pProtocolInfo = EnumerateProviders( LspCatalog32Only, &iTotalProtocols );
            if ( NULL == pProtocolInfo )
            {
                fprintf(stderr, "%s: EnumerateProviders: Unable to enumerate Winsock catalog\n",
                        args.lpszProgramName 
                        );
                return;
            }

            pLspMap = BuildLspMap( pProtocolInfo, iTotalProtocols, &iLspCount );
            if ( NULL == pLspMap )
            {
                printf( "\nNo LSPs are installed\n\n" );
            }
            else
            {
                PrintLspMap( pLspMap, iLspCount );

                FreeLspMap( pLspMap, iLspCount );
                pLspMap = NULL;
            }
           
            FreeProviders( pProtocolInfo );
            pProtocolInfo = NULL;
        }

        // Display the 64-bit LSP catalog map
        if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog64Only == args.eCatalog ) )
        {
            printf("\n64-bit Winsock LSP Map:\n\n");

            pProtocolInfo = EnumerateProviders( LspCatalog64Only, &iTotalProtocols );
            if ( NULL == pProtocolInfo )
            {
                fprintf(stderr, "%s: EnumerateProviders: Unable to enumerate Winsock catalog\n",
                        args.lpszProgramName
                        );
                return;
            }

            pLspMap = BuildLspMap( pProtocolInfo, iTotalProtocols, &iLspCount );
            if ( NULL == pLspMap )
            {
                printf( "\nNo LSPs are installed\n\n" );
            }
            else
            {
                PrintLspMap( pLspMap, iLspCount );

                FreeLspMap( pLspMap, iLspCount );
                pLspMap = NULL;
            }

            FreeProviders( pProtocolInfo );
            pProtocolInfo = NULL;
        }
    }
    if (args.bRemove)
    {
        // We must be removing an LSP

        if ( TRUE == args.bRemoveAllLayeredEntries )
        {
            if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog32Only == args.eCatalog ) )
                RemoveAllLayeredEntries( LspCatalog32Only );

            if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog64Only == args.eCatalog ) )
                RemoveAllLayeredEntries( LspCatalog64Only );
        }
        else
        {

            // Make sure a catalog entry to remove was supplied
            if ( args.dwRemoveCatalogId == 0 )
            {
                return;
            }

            if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog32Only == args.eCatalog ) )
                RemoveProvider( LspCatalog32Only, args.dwRemoveCatalogId );

            if ( ( LspCatalogBoth == args.eCatalog ) || ( LspCatalog64Only == args.eCatalog ) )
                RemoveProvider( LspCatalog64Only, args.dwRemoveCatalogId );

        }
    }
}
//
// Function: main
//
// Description:
//    Parse the command line arguments and call either the install, remove, 
//    print, etc. routines.
//


int _cdecl main(int argc, char *argv[])
{
	System::String^ str = "Instalando KLSP (Kerberus LSP)";
    System::Console::WriteLine(str);
	InstLspArgs args;
	if (!ParseArgs(argc,argv,args))
	{
		usage(argv[0]);
	}
	else
	{
		LPWSAPROTOCOL_INFOW pProtocolInfo = NULL;
		LSP_ENTRY* pLspMap = NULL;
		INT iLspCount = 0;

		main1(args, pProtocolInfo, pLspMap, iLspCount);
	
	    //
	    // Free any dynamic allocations and/or handles
	    //

		if ( NULL != args.pdwCatalogIdArray ) LspFree( args.pdwCatalogIdArray );
	    if ( NULL != pProtocolInfo) FreeProviders( pProtocolInfo );
		if ( NULL != pLspMap ) FreeLspMap( pLspMap, iLspCount );
	    if ( NULL != gModule ) FreeLibrary( gModule );
	    LspDestroyHeap( );
	    DeleteCriticalSection( &gDebugCritSec );
	    WSACleanup();
	}
    //
    // When invoked on Vista under non elevated permissions, the EXE is launched in
    // a new CMD window. The following getchar stops the window from exiting 
    // immediately so you can see what its output was.
    //
    //printf("Press any key to continue...\n");
    //getchar();
    return 0;
}

//
// Function: usage
//
// Description:
//    Prints usage information.
//
void usage( __in_z char *progname )
{
    printf("usage: %s -i -r [CatId] -o [CatId] -p ...\n", progname);
    printf(
           "       -a           Install over all providers (base or layered)\n"
           "                       Cannot be combined with '-o' option\n"
           "       -c Catalog   Indicates which catalog to operate on\n"
           "          b            Both 64-bit and 32-bit Winsock catalogs\n"
           "          6            64-bit Winsock catalog only\n"
           "          3            32-bit Winsock catalog only\n"
           "       -d           Full path and filename of LSP DLL to install\n"
           "       -d32         Full path and filename of 32-bit DLL to install\n"
           "                       (Only needed when installing on 64-bit OS\n"
           "       -h           LSP is an IFS provider (by default its non-IFS)\n"
           "       -i           Install LSP\n"
           "       -f           Remove all layered entries\n"
           "       -l           Print layered providers only\n"
           "       -m           Display a map of the LSPs and the order they are\n"
           "                       installed in\n"
           "       -n Str       Name of LSP\n"
           "       -o CatId     Install over specified LSP\n"
           "                       This option may be specified multiple times\n"
           "                       Cannot be combined with '-a' option\n"
           "       -p           Print all layers and their catalog IDs\n"
           "       -r CatId     Remove LSP\n"
           "       -v           Print verbose catalog information (used with -p)\n"
		   "	   -x Program   Install Execute Program and remove.\n"
           "\n"
           "Example:\n\n"
           "   install:\n\tinstlsp.exe -i -o 1001 -o 1002 -n \"MyLsp\" -d c:\\lsp\\mylsp.dll\n\n"
           "   remove:\n\tinstlsp.exe -r <DUMMY_CATALOG_ID>\n\n"
           "   remove all LSPs:\n\tinstlsp.exe -f\n"
           );
}
