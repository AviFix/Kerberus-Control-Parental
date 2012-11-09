////////////////////////////////////////////////////////////////////////////////
//
// Extension.cpp prototypes
//
////////////////////////////////////////////////////////////////////////////////

BOOL PASCAL FAR 
ExtTransmitFile (
    IN SOCKET hSocket,
    IN HANDLE hFile,
    IN DWORD nNumberOfBytesToWrite,
    IN DWORD nNumberOfBytesPerSend,
    IN LPOVERLAPPED lpOverlapped,
    IN LPTRANSMIT_FILE_BUFFERS lpTransmitBuffers,
    IN DWORD dwReserved
    );

BOOL PASCAL FAR 
ExtAcceptEx(
    IN SOCKET sListenSocket,
    IN SOCKET sAcceptSocket,
    IN PVOID lpOutputBuffer,
    IN DWORD dwReceiveDataLength,
    IN DWORD dwLocalAddressLength,
    IN DWORD dwRemoteAddressLength,
    OUT LPDWORD lpdwBytesReceived,
    IN LPOVERLAPPED lpOverlapped
    );

BOOL PASCAL FAR 
ExtConnectEx(
    IN SOCKET s,
    IN const struct sockaddr FAR *name,
    IN int namelen,
    IN PVOID lpSendBuffer OPTIONAL,
    IN DWORD dwSendDataLength,
    OUT LPDWORD lpdwBytesSent,
    IN LPOVERLAPPED lpOverlapped
    );

BOOL PASCAL FAR 
ExtTransmitPackets(
    SOCKET hSocket,
    LPTRANSMIT_PACKETS_ELEMENT lpPacketArray,
    DWORD nElementCount,
    DWORD nSendSize,
    LPOVERLAPPED lpOverlapped,
    DWORD dwFlags
    );

BOOL PASCAL FAR 
ExtDisconnectEx(
    IN SOCKET s,
    IN LPOVERLAPPED lpOverlapped,
    IN DWORD  dwFlags,
    IN DWORD  dwReserved
    );

INT PASCAL FAR 
ExtWSARecvMsg(
    IN SOCKET s,
    IN OUT LPWSAMSG lpMsg,
    OUT LPDWORD lpdwNumberOfBytesRecvd,
    IN LPWSAOVERLAPPED lpOverlapped,
    IN LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine
    );

INT PASCAL FAR
ExtWSASendMsg(
    IN SOCKET s,
    IN WSASENDMSG *sendMsg,
    IN LPWSATHREADID lpThreadId,
    OUT LPINT lpErrno
    );

INT PASCAL FAR
ExtWSAPoll(
    IN SOCKET s,
    IN WSAPOLLDATA *pollData,
    IN LPWSATHREADID lpThreadId,
    OUT LPINT lpErrno
    );

// Loads the given extension function from the lower provider
BOOL
LoadExtensionFunction(
    FARPROC   **func,
    GUID        ExtensionGuid,
    LPWSPIOCTL  fnIoctl,
    SOCKET      s
    );
