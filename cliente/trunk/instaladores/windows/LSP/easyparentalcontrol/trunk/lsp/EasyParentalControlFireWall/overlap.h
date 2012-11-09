////////////////////////////////////////////////////////////////////////////////
//
// Overlap.cpp prototypes
//
////////////////////////////////////////////////////////////////////////////////

// Initialize the overlapped system for handing asynchronous (overlapped) I/O
int 
InitOverlappedManager(
    );

// Issues the shutdown command for all worker threads to exit
int 
StopOverlappedManager(
    );

// Queue an overlapped operation for execution
int 
QueueOverlappedOperation(
    WSAOVERLAPPEDPLUS  *lpOverlapped, 
    SOCK_INFO          *Context
    );

// Allocate and initialize a WSAOVERLAPPEDPLUS structure which describes an overlapped operation
WSAOVERLAPPEDPLUS *
PrepareOverlappedOperation(
    SOCK_INFO                         *SocketContext,
    LspOperation                       operation,
    WSABUF                            *lpBuffers,
    DWORD                              dwBufferCount,
    LPWSAOVERLAPPED                    lpOverlapped,
    LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine,
    LPWSATHREADID                      lpThreadId,
    int                               *lpErrno
    );

// This function handles the completion of an overlapped operation
void CALLBACK 
IntermediateCompletionRoutine(
    DWORD           dwError, 
    DWORD           cbTransferred,
    LPWSAOVERLAPPED lpOverlapped, 
    DWORD           dwFlags
    );

// If an overlapped operation fails inline, we must undo some state
void
UndoOverlappedOperation( 
    SOCK_INFO         *SocketContext,
    WSAOVERLAPPEDPLUS *ProviderOverlapped
    );

// Frees all cached WSAOVERLAPPEDPLUS structures when the LSP is unloaded
void
FreeOverlappedLookasideList(
    );