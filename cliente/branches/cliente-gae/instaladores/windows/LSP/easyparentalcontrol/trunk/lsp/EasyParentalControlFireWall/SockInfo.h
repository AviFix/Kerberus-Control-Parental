////////////////////////////////////////////////////////////////////////////////
//
// Sockinfo.cpp prototypes
//
////////////////////////////////////////////////////////////////////////////////

SOCK_INFO *
GetCallerSocket(
    PROVIDER   *provider, 
    SOCKET      ProviderSocket
    );

// Allocates a SOCK_INFO structure, initializes it, and inserts into the provider list
SOCK_INFO *
CreateSockInfo(
    PROVIDER   *Provider, 
    SOCKET      ProviderSocket, 
    SOCK_INFO  *Inherit, 
    BOOL        Insert,
    int        *lpErrno
    );

// Looks up the socket context structure associated with the application socket
SOCK_INFO *
FindAndRefSocketContext(
    SOCKET  s, 
    int    *err
    );

// Decrements the reference count on the given socket context object
void 
DerefSocketContext(
    SOCK_INFO  *context, 
    int        *err
    );

// Frees a previously allocated SOCK_INFO structure
void 
FreeSockInfo(
    SOCK_INFO *info
    );

// Inserts the SOCK_INFO structure at the tail of the given provider's socket list
void 
InsertSocketInfo(
    PROVIDER   *provider, 
    SOCK_INFO  *sock
    );

// Removes the given SOCK_INFO structure from the provider's socket list
void 
RemoveSocketInfo(
    PROVIDER   *provider, 
    SOCK_INFO  *sock
    );

// Enters the SOCK_INFO structure's critical section preventing other threads from accessing it
void 
AcquireSocketLock(
    SOCK_INFO  *SockInfo
    );

// Releases the SOCK_INFO structure's critical section
void 
ReleaseSocketLock(
    SOCK_INFO  *SockInfo
    );

// Closes all the sockets and frees all resources associated with a provider
void 
CloseAndFreeSocketInfo(
    PROVIDER   *provider,
    BOOL        processDetach
    );

