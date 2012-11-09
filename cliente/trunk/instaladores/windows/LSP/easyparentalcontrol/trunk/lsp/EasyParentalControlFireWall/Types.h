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


#pragma once
// Name of the Winsock DDL which is needed by the installer to determine if
// WSCUpdateProvider is available.

// Function definition for the GetLspGuid export which returns an LSPs dummy provider GUID
typedef
   void (__stdcall *LPFN_GETLSPGUID) (GUID *lpGuid) ; 

// For 64-bit systems, we need to know which catalog to operate on
typedef enum
{
    LspCatalogBoth = 0,
    LspCatalog32Only,
    LspCatalog64Only
} WINSOCK_CATALOG;

//
// Extended proc table containing all the Microsoft specific Winsock functions
//
typedef struct _EXT_WSPPROC_TABLE
{
    LPFN_ACCEPTEX             lpfnAcceptEx;
    LPFN_TRANSMITFILE         lpfnTransmitFile;
    LPFN_GETACCEPTEXSOCKADDRS lpfnGetAcceptExSockaddrs;
    LPFN_TRANSMITPACKETS      lpfnTransmitPackets;
    LPFN_CONNECTEX            lpfnConnectEx;
    LPFN_DISCONNECTEX         lpfnDisconnectEx;
    LPFN_WSARECVMSG           lpfnWSARecvMsg;
} EXT_WSPPROC_TABLE;

//
// Describes a single catalog entry over which this LSP is layered on. It keeps track
// of the lower provider's dispatch table as well as a list of all the sockets
// created from our provider
//
typedef struct _PROVIDER
{
    WSAPROTOCOL_INFOW   NextProvider,           // Next provider in chain
                        LayerProvider;          // This layered provider
    WSPPROC_TABLE       NextProcTable;          // Proc table of next provider
    EXT_WSPPROC_TABLE   NextProcTableExt;       // Proc table of next provider's extension

    DWORD               LspDummyId;

    WCHAR               ProviderPathW[MAX_PATH],
                        LibraryPathW[MAX_PATH];
    INT                 ProviderPathLen;

    LPWSPSTARTUP        fnWSPStartup;
    WSPDATA             WinsockVersion;
    HMODULE             Module;

    INT                 StartupCount;

    LIST_ENTRY          SocketList;             // List of socket objects belonging to LSP

    CRITICAL_SECTION    ProviderCritSec;
} PROVIDER, * LPPROVIDER;


////////////////////////////////////////////////////////////////////////////////
//
// Provider.cpp prototypes
//
////////////////////////////////////////////////////////////////////////////////

// Moved to Provider.h

////////////////////////////////////////////////////////////////////////////////
//
// LINK list:
////////////////////////////////////////////////////////////////////////////////
//
// Definitions for a double link list.


//
// Calculate the address of the base of the structure given its type, and an
// address of a field within the structure.
//
#ifndef CONTAINING_RECORD
#define CONTAINING_RECORD(address, type, field) \
    ((type *)((PCHAR)(address) - (ULONG_PTR)(&((type *)0)->field)))
#endif


#ifndef InitializeListHead
//
//  VOID
//  InitializeListHead(
//      PLIST_ENTRY ListHead
//      );
//

#define InitializeListHead(ListHead) (\
    (ListHead)->Flink = (ListHead)->Blink = (ListHead))

//
//  BOOLEAN
//  IsListEmpty(
//      PLIST_ENTRY ListHead
//      );
//

#define IsListEmpty(ListHead) \
    ((ListHead)->Flink == (ListHead))

//
//  PLIST_ENTRY
//  RemoveHeadList(
//      PLIST_ENTRY ListHead
//      );
//

#define RemoveHeadList(ListHead) \
    (ListHead)->Flink;\
    {RemoveEntryList((ListHead)->Flink)}

//
//  PLIST_ENTRY
//  RemoveTailList(
//      PLIST_ENTRY ListHead
//      );
//

#define RemoveTailList(ListHead) \
    (ListHead)->Blink;\
    {RemoveEntryList((ListHead)->Blink)}

//
//  VOID
//  RemoveEntryList(
//      PLIST_ENTRY Entry
//      );
//

#define RemoveEntryList(Entry) {\
    PLIST_ENTRY _EX_Blink;\
    PLIST_ENTRY _EX_Flink;\
    _EX_Flink = (Entry)->Flink;\
    _EX_Blink = (Entry)->Blink;\
    _EX_Blink->Flink = _EX_Flink;\
    _EX_Flink->Blink = _EX_Blink;\
    }

//
//  VOID
//  InsertTailList(
//      PLIST_ENTRY ListHead,
//      PLIST_ENTRY Entry
//      );
//

#define InsertTailList(ListHead,Entry) {\
    PLIST_ENTRY _EX_Blink;\
    PLIST_ENTRY _EX_ListHead;\
    _EX_ListHead = (ListHead);\
    _EX_Blink = _EX_ListHead->Blink;\
    (Entry)->Flink = _EX_ListHead;\
    (Entry)->Blink = _EX_Blink;\
    _EX_Blink->Flink = (Entry);\
    _EX_ListHead->Blink = (Entry);\
    }

//
//  VOID
//  InsertHeadList(
//      PLIST_ENTRY ListHead,
//      PLIST_ENTRY Entry
//      );
//

#define InsertHeadList(ListHead,Entry) {\
    PLIST_ENTRY _EX_Flink;\
    PLIST_ENTRY _EX_ListHead;\
    _EX_ListHead = (ListHead);\
    _EX_Flink = _EX_ListHead->Flink;\
    (Entry)->Flink = _EX_Flink;\
    (Entry)->Blink = _EX_ListHead;\
    _EX_Flink->Blink = (Entry);\
    _EX_ListHead->Flink = (Entry);\
    }



BOOL IsNodeOnList(PLIST_ENTRY ListHead, PLIST_ENTRY Entry);


#endif //InitializeListHead



////////////////////////////////////////////////////////////////////////////////
//
// Macro definitions
//
////////////////////////////////////////////////////////////////////////////////

#ifdef ASSERT
#undef ASSERT
#endif 

#ifdef DBG

// Prints a message to the debugger
void 
dbgprint(        char *format,
        ...
        );


#define ASSERT(exp)                                              \
        if ( !(exp) )                                            \
            dbgprint("\n*** Assertion failed: %s\n"              \
                       "***      Source file: %s, line: %d\n\n", \
                       #exp,__FILE__,__LINE__), DebugBreak()
#else

// On free builds, define these to be empty
#define ASSERT(exp)
#define dbgprint

#endif


#define WM_SOCKET ( WM_USER + 321 )     // Message for our async window events

//
// This is the socket context data that we associate with each socket
//  that is passed back to the user app. That way when another API
//  is called we can query for this context information and find out
//  the socket handle to the lower provider.
//
typedef struct _SOCK_INFO
{
    SOCKET ProviderSocket;      // lower provider socket handle
    SOCKET LayeredSocket;       // app's socket handle
    DWORD  dwOutstandingAsync;  // count of outstanding async operations
    BOOL   bClosing;            // has the app closed the socket?

    volatile LONG  RefCount;    // How many threads are accessing this info?

    ULONGLONG  BytesSent;       // Byte counts
    ULONGLONG  BytesRecv;
    HANDLE     hIocp;           // associated with an IOCP?
    
    int    LastError;           // Last error that occured on this socket

    HWND   hWnd;                // Window (if any) associated with socket
    UINT   uMsg;                // Message for socket events

    CRITICAL_SECTION   SockCritSec; // Synchronize access to this object

    PROVIDER          *Provider;// Pointer to the provider from which socket was created

    LIST_ENTRY         Link;

} SOCK_INFO;

//
// Structure for mapping upper layer sockets to lower provider sockets in WSPSelect
//
typedef struct _FD_MAP
{
    SOCKET      ClientSocket;       // Upper layer socket handle
    SOCKET      ProvSocket;         // Lower layer socket handle
    SOCK_INFO  *Context;            // Pointer to the socket context
} FD_MAP;

////////////////////////////////////////////////////////////////////////////////
//
// Structures for each overlapped enabled API containing the arguments to that
//    function.
//
////////////////////////////////////////////////////////////////////////////////

// Argument list for the AcceptEx API
typedef struct _ACCEPTEXARGS
{
    SOCKET       sAcceptSocket,
                 sProviderAcceptSocket;
    PVOID        lpOutputBuffer;
    DWORD        dwReceiveDataLength,
                 dwLocalAddressLength,
                 dwRemoteAddressLength;
    DWORD        dwBytesReceived;
} ACCEPTEXARGS;

// Argument list for the TransmitFile API
typedef struct _TRANSMITFILEARGS
{
    HANDLE        hFile;
    DWORD         nNumberOfBytesToWrite,
                  nNumberOfBytesPerSend;
    LPTRANSMIT_FILE_BUFFERS lpTransmitBuffers;
    DWORD         dwFlags;
} TRANSMITFILEARGS;

// Argument list for the ConnectEx API
typedef struct _CONNECTEXARGS
{
    SOCKET           s;
    SOCKADDR_STORAGE name;
    int              namelen;
    PVOID            lpSendBuffer;
    DWORD            dwSendDataLength;
    DWORD            dwBytesSent;
} CONNECTEXARGS;

// Argument list for TransmitPackets API
typedef struct _TRANSMITPACKETSARGS
{
    SOCKET          s;
    LPTRANSMIT_PACKETS_ELEMENT lpPacketArray;
    DWORD           nElementCount;
    DWORD           nSendSize;
    DWORD           dwFlags;
} TRANSMITPACKETSARGS;

// Argument list for DisconnectEx API
typedef struct _DISCONNECTEXARGS
{
    SOCKET          s;
    DWORD           dwFlags;
    DWORD           dwReserved;
} DISCONNECTEXARGS;

// Argument list for WSARecvMsg API
typedef struct _WSARECVMSGARGS
{
    WSAMSG          WsaMsg;
    DWORD           dwNumberOfBytesRecvd;
} WSARECVMSGARGS;

// Argument list for the WSARecv API
typedef struct _RECVARGS
{
    LPWSABUF       lpBuffers;
    DWORD          dwBufferCount;
    DWORD          dwNumberOfBytesRecvd,
                   dwFlags;
} RECVARGS;

// Argument list for the WSARecvFrom API
typedef struct _RECVFROMARGS
{
    LPWSABUF       lpBuffers;
    DWORD          dwBufferCount;
    DWORD          dwNumberOfBytesRecvd,
                   dwFlags;
    LPSOCKADDR     lpFrom;
    LPINT          lpFromLen;
} RECVFROMARGS;

// Argument list for the WSASend API
typedef struct _SENDARGS
{
    LPWSABUF       lpBuffers;
    DWORD          dwBufferCount;
    DWORD          dwNumberOfBytesSent;
    DWORD          dwFlags;
} SENDARGS;

// Argument list for the WSASendTo API
typedef struct _SENDTOARGS
{
    LPWSABUF         lpBuffers;
    DWORD            dwBufferCount;
    DWORD            dwNumberOfBytesSent;
    DWORD            dwFlags;
    SOCKADDR_STORAGE To;
    int              iToLen;
} SENDTOARGS;

// Argument list for the WSASendMsg API
typedef struct _WSASENDMSGARGS
{
    WSASENDMSG      SendMsg;
    WSAMSG          WsaMsg;
    DWORD           dwNumberOfBytesSent;
} WSASENDMSGARGS;

// Argument list for the WSAIoctl API
typedef struct _IOCTLARGS
{
    DWORD          dwIoControlCode;
    LPVOID         lpvInBuffer;
    DWORD          cbInBuffer;
    LPVOID         lpvOutBuffer;
    DWORD          cbOutBuffer;
    DWORD          cbBytesReturned;
} IOCTLARGS;

// Enumerated type of all asynchronous Winsock operations
typedef enum
{
    LSP_OP_IOCTL         = 1,
    LSP_OP_RECV,
    LSP_OP_RECVFROM,
    LSP_OP_SEND,
    LSP_OP_SENDTO,
    LSP_OP_TRANSMITFILE,
    LSP_OP_ACCEPTEX,
    LSP_OP_CONNECTEX,
    LSP_OP_DISCONNECTEX,
    LSP_OP_TRANSMITPACKETS,
    LSP_OP_RECVMSG,
    LSP_OP_SENDMSG
} LspOperation;

//
// Our OVERLAPPED structure that includes state and argument
//  information. This structure is used for all overlapped IO
//  operations. Whenever the user app requests overlapped IO
//  we intercept this and make our own call with our own 
//  structure. This way we will receive notification first
//  at which time we can perform post processesing. When we
//  are done we can then post the completion to the user app.
//
typedef struct _WSAOVERLAPPEDPLUS
{
    WSAOVERLAPPED   ProviderOverlapped;     // Overlap to pass to lower layer
    PROVIDER       *Provider;               // Reference to provider who owns this socket
    SOCK_INFO      *SockInfo;               // Socket initiating this operation
    SOCKET          CallerSocket;           // Upper layer's socket handle
    SOCKET          ProviderSocket;         // Lower layer's socket handle
    HANDLE          Iocp;                   
    int             Error;                  // Error that operation completed with

    BOOL            CloseThread;            // Indicates whether we need to close thread we opened

    union 
    {
        // Various arguments to the call being made
        ACCEPTEXARGS        AcceptExArgs;
        TRANSMITFILEARGS    TransmitFileArgs;
        CONNECTEXARGS       ConnectExArgs;
        TRANSMITPACKETSARGS TransmitPacketsArgs;
        DISCONNECTEXARGS    DisconnectExArgs;
        WSARECVMSGARGS      RecvMsgArgs;
        RECVARGS            RecvArgs;
        RECVFROMARGS        RecvFromArgs;
        SENDARGS            SendArgs;
        SENDTOARGS          SendToArgs;
        IOCTLARGS           IoctlArgs;
        WSASENDMSGARGS      SendMsgArgs;
    };

    LspOperation            Operation;              // Type of operation posted
    WSATHREADID             CallerThreadId;         // Which thread initiated operation
    LPWSAOVERLAPPED         lpCallerOverlapped;     // Upper layer's overlapped structure
    LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCallerCompletionRoutine;   // APC to queue upon completion

    LIST_ENTRY              Link;           // Linked list entry

} WSAOVERLAPPEDPLUS, * LPWSAOVERLAPPEDPLUS;

