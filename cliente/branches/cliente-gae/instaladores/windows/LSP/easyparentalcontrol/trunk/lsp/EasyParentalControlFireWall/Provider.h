////////////////////////////////////////////////////////////////////////////////
//
// Provider.cpp prototypes
//
////////////////////////////////////////////////////////////////////////////////

BOOL
FindLspEntries(
        PROVIDER  **lspProviders,
        int        *lspProviderCount,
        int        *lpErrno
        );

PROVIDER *
FindMatchingLspEntryForProtocolInfo(
        WSAPROTOCOL_INFOW *inInfo,
        PROVIDER          *lspProviders,
        int                lspCount,
        BOOL               fromStartup = FALSE
        );

// Initialize the given provider by calling its WSPStartup
int
InitializeProvider(
        PROVIDER *provider,
        WORD wVersion,
        WSAPROTOCOL_INFOW *lpProtocolInfo,
        WSPUPCALLTABLE UpCallTable,
        int *Error
        );

BOOL
LoadProviderPath(
        PROVIDER    *loadProvider,
        int         *lpErrno
        );

// Verifies all the function pointers in the proc table are non-NULL
int 
VerifyProcTable(
        LPWSPPROC_TABLE lpProcTable
        );

// Returns an array of protocol entries from the given Winsock catalog
LPWSAPROTOCOL_INFOW 
EnumerateProviders(
        WINSOCK_CATALOG Catalog, 
        LPINT           TotalProtocols
        );

// Enumerates the given Winsock catalog into the already allocated buffer
int
EnumerateProvidersExisting(
        WINSOCK_CATALOG     Catalog, 
        WSAPROTOCOL_INFOW  *ProtocolInfo,
        LPDWORD             ProtocolInfoSize
        );

// Free the array of protocol entries returned from EnumerateProviders
void 
FreeProviders(
        LPWSAPROTOCOL_INFOW ProtocolInfo
        );

// Prints a protocol entry to the console in a readable, formatted form
void 
PrintProtocolInfo(
        WSAPROTOCOL_INFOW  *ProtocolInfo
        );

// Allocates a buffer from the LSP private heap
void *
LspAlloc(
        SIZE_T  size,
        int    *lpErrno
        );

// Frees a buffer previously allocated by LspAlloc
void
LspFree(
        LPVOID  buf
       );

// Creates the private heap used by the LSP and installer
int
LspCreateHeap(
        int    *lpErrno
        );

// Destroys the private heap
void
LspDestroyHeap(
        );
