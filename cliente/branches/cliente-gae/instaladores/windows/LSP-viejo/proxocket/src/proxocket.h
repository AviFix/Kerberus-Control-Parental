/*
    Copyright 2008,2009,2010 Luigi Auriemma

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

    http://www.gnu.org/licenses/gpl-2.0.txt
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "proxocket_defines.h"

#define ACPDUMP_LOCK // thread-safe writing
#include "acpdump2.h"



#define MAX_SOCKETS     0xffff  // more than enough
#define FREEPORT        1024
#define CALLIT(X)       static X##_(*_##X) = NULL; \
                        X##_(X)



typedef struct {
    SOCKET      s;
    uint32_t    sip;
    uint16_t    sport;
    uint32_t    dip;
    uint16_t    dport;
    uint8_t     type;
    uint8_t     protocol;
    uint32_t    seq1;
    uint32_t    ack1;
    uint32_t    seq2;
    uint32_t    ack2;
} sockets_t;



static  sockets_t   *sockets    = NULL;
static  FILE        *fdcap      = NULL,
                    *fddbg      = NULL;
static  uint16_t    freeport    = FREEPORT;



static HMODULE myproxocket = NULL;
static __cdecl SOCKET (*mysocket)(int af, int type, int protocol) = NULL;
static __cdecl int (*myconnect)(SOCKET s, const struct sockaddr *name, int namelen) = NULL;
static __cdecl SOCKET (*myaccept)(SOCKET s, const struct sockaddr *name, int *namelen) = NULL;
static __cdecl int (*mybind)(SOCKET s, const struct sockaddr *name, int namelen) = NULL;
static __cdecl int (*myclose)(SOCKET s) = NULL;
static __cdecl int (*myrecv)(SOCKET s, char *buf, int len, int flags) = NULL;
static __cdecl int (*myrecvfrom)(SOCKET s, char *buf, int len, int flags, struct sockaddr *from, int *fromlen) = NULL;
static __cdecl int (*mysend)(SOCKET s, char **retbuf, int len, int flags) = NULL;
static __cdecl int (*mysendto)(SOCKET s, char **retbuf, int len, int flags, const struct sockaddr *to, int tolen) = NULL;



void free_proxocket(void) {
    if(fdcap) {
        fclose(fdcap);
        fdcap = NULL;
    }
    if(fddbg) {
        fclose(fddbg);
        fddbg = NULL;
    }
    if(myproxocket) {
        FreeLibrary(myproxocket);
        myproxocket = NULL;
    }
    if(sockets) {
        free(sockets);
        sockets = NULL;
    }
}



int proxocket_basename(char *fname, int fnamesz, int type) {
    int     i;
    char    *p;

    if(!GetModuleFileName(NULL, fname, fnamesz)) goto quit;
    if(type < 0) {          // fullname
        p = fname + strlen(fname);

    } else if(!type) {      // path
        p = strrchr(fname, '\\');
        if(!p) p = strrchr(fname, '/');
        if(!p) goto quit;
        *p++ = '\\';
        *p   = 0;

    } else {                // basename / filename
        p = strrchr(fname, '\\');
        if(!p) p = strrchr(fname, '/');
        if(p) {
            p++;
            for(i = 0;; i++) {
                fname[i] = p[i];
                if(!fname[i]) break;
            }
        }
        if(type > 1) {      // basename
            p = strrchr(fname, '.');
            if(p) *p = 0;
        }
    }
    return(strlen(fname));
quit:
    fname[0] = 0;
    return(0);
}



void init_proxocket(void) {
    static const char *months[12] = {
            "jan","feb","mar","apr","may","jun",
            "jul","aug","sep","oct","nov","dec" };
    struct  tm  *tmx;
    time_t  datex;
    int     cnt;
    char    fname[4096],
            *ext,
            *p;

    #ifdef DEBUG
    if(!fddbg) {
        p = fname + proxocket_basename(fname, sizeof(fname) - 100, 0);
        if(p != fname) *p++ = '_';
        strcpy(p, "proxocket_debug.txt");
        fddbg = fopen(fname, "ab");
        if(!fddbg) {
            MessageBox(0, "the debug file can't be created", "Proxocket", MB_OK | MB_ICONERROR);
            exit(1);
        }
        if(fddbg) setbuf(fddbg, NULL);
    }
    #endif

    if(fdcap) return;
    if(myproxocket) return;

    myproxocket = LoadLibrary("myproxocket.dll");
    if(myproxocket) {
        mysocket    = (void *)GetProcAddress(myproxocket, "mysocket");
        myconnect   = (void *)GetProcAddress(myproxocket, "myconnect");
        myaccept    = (void *)GetProcAddress(myproxocket, "myaccept");
        mybind      = (void *)GetProcAddress(myproxocket, "mybind");
        myclose     = (void *)GetProcAddress(myproxocket, "myclose");
        myrecv      = (void *)GetProcAddress(myproxocket, "myrecv");
        myrecvfrom  = (void *)GetProcAddress(myproxocket, "myrecvfrom");
        mysend      = (void *)GetProcAddress(myproxocket, "mysend");
        mysendto    = (void *)GetProcAddress(myproxocket, "mysendto");

        #ifdef DEBUG
        if(fddbg) {
            fprintf(fddbg,
                "myproxocket.dll found and loaded:\n"
                "  mysocket    %p\n"
                "  myconnect   %p\n"
                "  myaccept    %p\n"
                "  mybind      %p\n"
                "  myclose     %p\n"
                "  myrecv      %p\n"
                "  myrecvfrom  %p\n"
                "  mysend      %p\n"
                "  mysendto    %p\n"
                "\n", mysocket, myconnect, myaccept, mybind, myclose, myrecv, myrecvfrom, mysend, mysendto);
        }
        #endif
    } else {
        p = fname + proxocket_basename(fname, sizeof(fname) - 100, -1);
        if(p != fname) *p++ = '_';

        time(&datex);
        tmx = localtime(&datex);
        sprintf(p,
            "proxocket_%02u.%s.%02u-%02u.%02u.%02u.cap",
            tmx->tm_mday, months[tmx->tm_mon], 1900 + tmx->tm_year,
            tmx->tm_hour, tmx->tm_min, tmx->tm_sec);

        ext = strrchr(fname, '.');
        if(!ext) ext = fname + strlen(fname);
        for(cnt = 0;; cnt++) {
            fdcap = fopen(fname, "rb");
            if(!fdcap) break;
            sprintf(ext, "_%d.cap", cnt);
        }
        fdcap = fopen(fname, "wb");
        if(!fdcap) {
            MessageBox(0, "the tcpdump capture file can't be created", "Proxocket", MB_OK | MB_ICONERROR);
            exit(1);
        }
        setbuf(fdcap, NULL);
        create_acp(fdcap);
    }

    sockets = calloc(sizeof(sockets_t), MAX_SOCKETS);
    if(!sockets) free_proxocket();
}



uint32_t get_ip(const struct sockaddr *addr) {
    uint32_t    ip;

    if(addr) {
        ip = ((struct sockaddr_in *)addr)->sin_addr.s_addr;
        if((ip != net32(INADDR_NONE)) && (ip != net32(INADDR_ANY))) return(ip);
    }
    return(net32(INADDR_LOOPBACK));
}



uint16_t get_freeport(void) {
    if(freeport < FREEPORT) freeport = FREEPORT;
    freeport++;
    return(freeport);
}



uint16_t get_port(const struct sockaddr *addr) {
    uint16_t    port;

    if(addr) {
        port = ((struct sockaddr_in *)addr)->sin_port;
        if(port) return(port);
    }
    return(net16(get_freeport()));
}



int return_sockets_num(SOCKET s) {
    int     i;

    if(!fdcap) return(-1);
    for(i = 0; i < MAX_SOCKETS; i++) {
        if(sockets[i].s == s) return(i);
    }
    return(-1);
}



int create_new_socket(SOCKET s, int type, int protocol) {
    int     n;

    if(type     < 0) type     = 1;  // WSASocket!
    if(protocol < 0) protocol = 6;  // WSASocket!

    n = return_sockets_num(0);    // new
    if(n < 0) {
        MessageBox(0, "max limit of monitored sockets reached by Proxocket, the program will quit", "Proxocket", MB_OK | MB_ICONERROR);
        exit(1);
    }
    sockets[n].s        = s;
    sockets[n].type     = type;
    sockets[n].protocol = protocol;
    sockets[n].sip      = net32(INADDR_LOOPBACK);
    sockets[n].sport    = net16(get_freeport());
    return(n);
}



void connect_socket(SOCKET s, const struct sockaddr *name, SOCKET sl) {
    int     n,
            nl;

    n = return_sockets_num(s);      // check if s is already indexed
    if(n < 0) {                     // otherwise index it
        n = create_new_socket(s, SOCK_STREAM, IPPROTO_TCP);
    }
    sockets[n].dip      = get_ip(name);
    sockets[n].dport    = get_port(name);
    sockets[n].seq1     = 0;
    sockets[n].ack1     = 0;
    sockets[n].seq2     = 0;
    sockets[n].ack2     = 0;
    if(sl > 0) {  // accept
        nl = return_sockets_num(sl);
        if(nl >= 0) {
            sockets[n].sip      = sockets[nl].sip;
            sockets[n].sport    = sockets[nl].sport;
        }
        acp_dump_handshake(
            fdcap, sockets[n].type, sockets[n].protocol,
            sockets[n].dip, sockets[n].dport, sockets[n].sip, sockets[n].sport,
            NULL, 0,
            &sockets[n].seq2, &sockets[n].ack2, &sockets[n].seq1, &sockets[n].ack1);
    } else {        // connect
        acp_dump_handshake(
            fdcap, sockets[n].type, sockets[n].protocol,
            sockets[n].sip, sockets[n].sport, sockets[n].dip, sockets[n].dport,
            NULL, 0,
            &sockets[n].seq1, &sockets[n].ack1, &sockets[n].seq2, &sockets[n].ack2);
    }
}



// return value: If successful, the WSAStartup function returns zero. Otherwise, it returns one of the error codes listed below: WSASYSNOTREADY, WSAVERNOTSUPPORTED, WSAEINPROGRESS, WSAEPROCLIM, WSAEFAULT
#define WSAStartup_(X) int CALLING_CONVENTION (X)(WORD wVersionRequested, LPWSADATA lpWSAData)
CALLIT(WSAStartup) {
    int     ret;

    init_proxocket();
    ret = _WSAStartup(wVersionRequested, lpWSAData);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSAStartup %d,%d: %d\n", wVersionRequested & 0xff, wVersionRequested >> 8, ret);
    #endif
    return(ret);
}



// return value: If no error occurs, socket returns a descriptor referencing the new socket. Otherwise, a value of INVALID_SOCKET is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define socket_(X) SOCKET CALLING_CONVENTION (X)(int af, int type, int protocol)
CALLIT(socket) {
    SOCKET  ret;

    if(mysocket) {
        ret = mysocket(af, type, protocol);
        if(ret >= 0) {
            return(ret);    // return your socket
        } else if(ret == INVALID_SOCKET) {
            return(ret);    // return the error
        } else {
            // call the original function
        }
    }
    ret = _socket(af, type, protocol);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "socket %d,%d: %d\n", type, protocol, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) create_new_socket(ret, type, protocol);
    }
    return(ret);
}



// return value: If no error occurs, WSASocket returns a descriptor referencing the new socket. Otherwise, a value of INVALID_SOCKET is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define WSASocketA_(X) SOCKET CALLING_CONVENTION (X)(int af, int type, int protocol, LPWSAPROTOCOL_INFOA lpProtocolInfo, GROUP g, DWORD dwFlags)
CALLIT(WSASocketA) {
    SOCKET  ret;

    if(mysocket) {
        ret = mysocket(af, type, protocol);
        if(ret >= 0) {
            return(ret);    // return our socket
        } else if(ret == INVALID_SOCKET) {
            return(ret);    // return the error
        } else {
            // call the original function
        }
    }
    ret = _WSASocketA(af, type, protocol, lpProtocolInfo, g, dwFlags);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSASocketA %d,%d: %d\n", type, protocol, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) create_new_socket(ret, type, protocol);
    }
    return(ret);
}



// return value: If no error occurs, WSASocket returns a descriptor referencing the new socket. Otherwise, a value of INVALID_SOCKET is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define WSASocketW_(X) SOCKET CALLING_CONVENTION (X)(int af, int type, int protocol, LPWSAPROTOCOL_INFOW lpProtocolInfo, GROUP g, DWORD dwFlags)
CALLIT(WSASocketW) {
    SOCKET  ret;

    if(mysocket) {
        ret = mysocket(af, type, protocol);
        if(ret >= 0) {
            return(ret);    // return our socket
        } else if(ret == INVALID_SOCKET) {
            return(ret);    // return the error
        } else {
            // call the original function
        }
    }
    ret = _WSASocketW(af, type, protocol, lpProtocolInfo, g, dwFlags);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSASocketW %d,%d: %d\n", type, protocol, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) create_new_socket(ret, type, protocol);
    }
    return(ret);
}



// return value: If no error occurs, closesocket returns zero. Otherwise, a value of SOCKET_ERROR is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define closesocket_(X) int CALLING_CONVENTION (X)(SOCKET s)
CALLIT(closesocket) {
    int     n,
            ret;

    ret = _closesocket(s);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "closesocket %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) {
                sockets[n].s = 0;
                if(sockets[n].type == SOCK_STREAM) acp_dump(    // useless, requires more stuff to close the connection correctly
                    fdcap, sockets[n].type, sockets[n].protocol,
                    sockets[n].sip, sockets[n].sport, sockets[n].dip, sockets[n].dport,
                    NULL, -1,
                    &sockets[n].seq1, &sockets[n].ack1, &sockets[n].seq2, &sockets[n].ack2);
            }
        }
        if(myclose) ret = myclose(s);
    }
    return(ret);
}



// return value: If no error occurs, connect returns zero. Otherwise, it returns SOCKET_ERROR, and a specific error code can be retrieved by calling WSAGetLastError.
#define connect_(X) int CALLING_CONVENTION (X)(SOCKET s, const struct sockaddr *name, int namelen)
CALLIT(connect) {
    int     ret;

    if(myconnect) {
        ret = myconnect(s, name, namelen);
        if(ret == 0) {
            // call the original function
        } else if(ret == SOCKET_ERROR) {
            return(ret);    // return the error
        } else {
            return(0);      // return ok, bypass the real one
        }
    }
    if(fdcap) connect_socket(s, name, -1);
    ret = _connect(s, name, namelen);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "connect %d: %d\n", s, ret);
    #endif
    return(ret);
}



// return value: If no error occurs, WSAConnect returns zero. Otherwise, it returns SOCKET_ERROR, and a specific error code can be retrieved by calling WSAGetLastError. On a blocking socket, the return value indicates success or failure of the connection attempt.
#define WSAConnect_(X) int CALLING_CONVENTION (X)(SOCKET s, const struct sockaddr *name, int namelen, LPWSABUF lpCallerData, LPWSABUF lpCalleeData, LPQOS lpSQOS, LPQOS lpGQOS)
CALLIT(WSAConnect) {
    int     ret;

    if(myconnect) {
        ret = myconnect(s, name, namelen);
        if(ret == 0) {
            // call the original function
        } else if(ret == SOCKET_ERROR) {
            return(ret);    // return the error
        } else {
            return(0);      // return ok, bypass the real one
        }
    }
    if(fdcap) connect_socket(s, name, -1);
    ret = _WSAConnect(s, name, namelen, lpCallerData, lpCalleeData, lpSQOS, lpGQOS);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSAConnect %d: %d\n", s, ret);
    #endif
    return(ret);
}



// return value: If no error occurs, bind returns zero. Otherwise, it returns SOCKET_ERROR, and a specific error code can be retrieved by calling WSAGetLastError.
#define bind_(X) int CALLING_CONVENTION (X)(SOCKET s, const struct sockaddr *name, int namelen)
CALLIT(bind) {
    int     n,
            ret;

    if(mybind) {
        ret = mybind(s, name, namelen);
        if(ret == 0) {
            // call the original function
        } else if(ret == SOCKET_ERROR) {
            return(ret);    // return the error
        } else {
            return(0);      // return ok, bypass the real one
        }
    }
    ret = _bind(s, name, namelen);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "recv %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) {
                sockets[n].sip   = get_ip(name);
                sockets[n].sport = get_port(name);
            }
        }
    }
    return(ret);
}



// return value: If no error occurs, accept returns a value of type SOCKET that is a descriptor for the new socket. This returned value is a handle for the socket on which the actual connection is made.
#define accept_(X) SOCKET CALLING_CONVENTION (X)(SOCKET s, const struct sockaddr *name, int *namelen)
CALLIT(accept) {
    SOCKET  ret;

    ret = _accept(s, name, namelen);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "accept %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) connect_socket(ret, name, s);
        if(myaccept) ret = myaccept(ret, name, namelen);
    }
    return(ret);
}



// return value:  If no error occurs, WSAAccept returns a value of type SOCKET that is a descriptor for the accepted socket. Otherwise, a value of INVALID_SOCKET is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define WSAAccept_(X) SOCKET CALLING_CONVENTION (X)(SOCKET s, struct sockaddr *addr, LPINT addrlen, LPCONDITIONPROC lpfnCondition, DWORD dwCallbackData)
CALLIT(WSAAccept) {
    int     ret;

    ret = _WSAAccept(s, addr, addrlen, lpfnCondition, dwCallbackData);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSAAccept %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) connect_socket(ret, addr, s);
        if(myaccept) ret = myaccept(ret, addr, addrlen);
    }
    return(ret);
}



// return value:  If no error occurs, recv returns the number of bytes received and the buffer pointed to by the buf parameter will contain this data received. If the connection has been gracefully closed, the return value is zero.
#define recv_(X) int CALLING_CONVENTION (X)(SOCKET s, char *buf, int len, int flags)
CALLIT(recv) {
    int     n,
            ret;

    ret = _recv(s, buf, len, flags);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "recv %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) acp_dump(
                fdcap, sockets[n].type, sockets[n].protocol,
                sockets[n].dip, sockets[n].dport, sockets[n].sip, sockets[n].sport,
                (uint8_t *)buf, ret,
                &sockets[n].seq2, &sockets[n].ack2, &sockets[n].seq1, &sockets[n].ack1);
        }
        if(myrecv) ret = myrecv(s, buf, ret, flags);
    }
    return(ret);
}



// return value: If no error occurs, recvfrom returns the number of bytes received. If the connection has been gracefully closed, the return value is zero. Otherwise, a value of SOCKET_ERROR is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define recvfrom_(X) int CALLING_CONVENTION (X)(SOCKET s, char *buf, int len, int flags, struct sockaddr *from, int *fromlen)
CALLIT(recvfrom) {
    int     n,
            ret;

    ret = _recvfrom(s, buf, len, flags, from, fromlen);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "recvfrom %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) acp_dump(
                fdcap, sockets[n].type, (sockets[n].type == SOCK_RAW) ? IPPROTO_RAW : sockets[n].protocol,
                get_ip(from), get_port(from), sockets[n].sip, sockets[n].sport,
                (uint8_t *)buf, ret,
                NULL, NULL, NULL, NULL);
        }
        if(myrecvfrom) ret = myrecvfrom(s, buf, ret, flags, from, fromlen);
    }
    return(ret);
}



// return value: If no error occurs and the receive operation has completed immediately, WSARecv returns zero
#define WSARecv_(X) int CALLING_CONVENTION (X)(SOCKET s, LPWSABUF lpBuffers, DWORD dwBufferCount, LPDWORD lpNumberOfBytesRecvd, LPDWORD lpFlags, LPWSAOVERLAPPED lpOverlapped, LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine)
CALLIT(WSARecv) {
    DWORD   i,
            rem;
    int     n,
            len,
            ret;

    ret = _WSARecv(s, lpBuffers, dwBufferCount, lpNumberOfBytesRecvd, lpFlags, lpOverlapped, lpCompletionRoutine);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSARecv %d: %d\n", s, ret);
    #endif
    if((ret >= 0) && lpNumberOfBytesRecvd) {    // overlapped is NOT supported
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) {
                rem = *lpNumberOfBytesRecvd;
                for(i = 0; i < dwBufferCount; i++) {
                    if((int)rem <= 0) break;
                    acp_dump(
                        fdcap, sockets[n].type, sockets[n].protocol,
                        sockets[n].dip, sockets[n].dport, sockets[n].sip, sockets[n].sport,
                        (uint8_t *)lpBuffers[i].buf, (rem > lpBuffers[i].len) ? lpBuffers[i].len : rem,
                        &sockets[n].seq2, &sockets[n].ack2, &sockets[n].seq1, &sockets[n].ack1);
                    rem -= lpBuffers[i].len;
                }
            }
        }
        if(myrecv) {
            rem = *lpNumberOfBytesRecvd;
            *lpNumberOfBytesRecvd = 0;
            for(i = 0; i < dwBufferCount; i++) {
                if((int)rem <= 0) break;
                len = myrecv(s, lpBuffers[i].buf, (rem > lpBuffers[i].len) ? lpBuffers[i].len : rem, *lpFlags);
                if(len < 0) return(SOCKET_ERROR);
                *lpNumberOfBytesRecvd += len;
                rem -= lpBuffers[i].len;
            }
        }
    }
    return(ret);
}



// return value: If no error occurs and the receive operation has completed immediately, WSARecvFrom returns zero
#define WSARecvFrom_(X) int CALLING_CONVENTION (X)(SOCKET s, LPWSABUF lpBuffers, DWORD dwBufferCount, LPDWORD lpNumberOfBytesRecvd, LPDWORD lpFlags, struct sockaddr *lpFrom, LPINT lpFromlen, LPWSAOVERLAPPED lpOverlapped, LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine)
CALLIT(WSARecvFrom) {
    DWORD   i,
            rem;
    int     n,
            len,
            ret;

    ret = _WSARecvFrom(s, lpBuffers, dwBufferCount, lpNumberOfBytesRecvd, lpFlags, lpFrom, lpFromlen, lpOverlapped, lpCompletionRoutine);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSARecvFrom %d: %d\n", s, ret);
    #endif
    if((ret >= 0) && lpNumberOfBytesRecvd) {    // overlapped is NOT supported
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) {
                rem = *lpNumberOfBytesRecvd;
                for(i = 0; i < dwBufferCount; i++) {
                    if((int)rem <= 0) break;
                    acp_dump(
                        fdcap, sockets[n].type, (sockets[n].type == SOCK_RAW) ? IPPROTO_RAW : sockets[n].protocol,
                        get_ip(lpFrom), get_port(lpFrom), sockets[n].sip, sockets[n].sport,
                        (uint8_t *)lpBuffers[i].buf, (rem > lpBuffers[i].len) ? lpBuffers[i].len : rem,
                        NULL, NULL, NULL, NULL);
                    rem -= lpBuffers[i].len;
                }
            }
        }
        if(myrecvfrom) {
            rem = *lpNumberOfBytesRecvd;
            *lpNumberOfBytesRecvd = 0;
            for(i = 0; i < dwBufferCount; i++) {
                if((int)rem <= 0) break;
                len = myrecvfrom(s, lpBuffers[i].buf, (rem > lpBuffers[i].len) ? lpBuffers[i].len : rem, *lpFlags, lpFrom, lpFromlen);
                if(len < 0) return(SOCKET_ERROR);
                *lpNumberOfBytesRecvd += len;
                rem -= lpBuffers[i].len;
            }
        }
    }
    return(ret);
}



// return value: If no error occurs, WSARecvEx returns the number of bytes received. If the connection has been closed, it returns zero. Additionally, if a partial message was received, the MSG_PARTIAL bit is set in the flags parameter. If a complete message was received, MSG_PARTIAL is not set in flags
#define WSARecvEx_(X) int CALLING_CONVENTION (X)(SOCKET s, char *buf, int len, int *flags)
CALLIT(WSARecvEx) {
    int     n,
            ret;

    ret = _WSARecvEx(s, buf, len, flags);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSARecvEx %d: %d\n", s, ret);
    #endif
    if(ret >= 0) {
        if(fdcap) {
            n = return_sockets_num(s);
            if(n >= 0) acp_dump(
                fdcap, sockets[n].type, sockets[n].protocol,
                sockets[n].dip, sockets[n].dport, sockets[n].sip, sockets[n].sport,
                (uint8_t *)buf, ret,
                &sockets[n].seq2, &sockets[n].ack2, &sockets[n].seq1, &sockets[n].ack1);
        }
        if(myrecv) ret = myrecv(s, buf, ret, *flags);
    }
    return(ret);
}



// return value:  If no error occurs, send returns the total number of bytes sent, which can be less than the number requested to be sent in the len parameter. Otherwise, a value of SOCKET_ERROR is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define send_(X) int CALLING_CONVENTION (X)(SOCKET s, char *buf, int len, int flags)
CALLIT(send) {
    int     n,
            ret     = SOCKET_ERROR,
            oldlen  = 0;    // needed because the main program could use "if(send(s, "hello", 5, 0) != 5) exit(1);"
    char    *oldbuf = NULL; // so returning the value it expects even if we have modified it will save the execution

    if(fdcap) {
        n = return_sockets_num(s);
        if(n >= 0) acp_dump(
            fdcap, sockets[n].type, sockets[n].protocol,
            sockets[n].sip, sockets[n].sport, sockets[n].dip, sockets[n].dport,
            (uint8_t *)buf, len,
            &sockets[n].seq1, &sockets[n].ack1, &sockets[n].seq2, &sockets[n].ack2);
    }
    if(mysend) {
        oldbuf = buf;
        oldlen = len;
        ret = mysend(s, &buf, len, flags);
        if(ret >= 0) {
            // call real function
        } else if(ret == SOCKET_ERROR) {
            goto quit_and_free;
        } else {
            ret = oldlen;
            goto quit_and_free;
        }
        len = ret;
    }
    ret = _send(s, buf, len, flags);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "send %d: %d\n", s, ret);
    #endif
quit_and_free:
    if(mysend) {
        if(oldbuf != buf) free(buf);    // free if it has been allocated by us
        if(ret == len) ret = oldlen;    // restore the old len if there have been no errors
    }
    return(ret);
}



// return value: If no error occurs, sendto returns the total number of bytes sent, which can be less than the number indicated by len. Otherwise, a value of SOCKET_ERROR is returned, and a specific error code can be retrieved by calling WSAGetLastError.
#define sendto_(X) int CALLING_CONVENTION (X)(SOCKET s, char *buf, int len, int flags, const struct sockaddr *to, int tolen)
CALLIT(sendto) {
    int     n,
            ret     = SOCKET_ERROR,
            oldlen  = 0;    // needed because the main program could use "if(send(s, "hello", 5, 0) != 5) exit(1);"
    char    *oldbuf = NULL; // so returning the value it expects even if we have modified it will save the execution

    if(fdcap) {
        n = return_sockets_num(s);
        if(n >= 0) acp_dump(
            fdcap, sockets[n].type, sockets[n].protocol,
            sockets[n].sip, sockets[n].sport, get_ip(to), get_port(to),
            (uint8_t *)buf, len,
            NULL, NULL, NULL, NULL);
    }
    if(mysendto) {
        oldbuf = buf;
        oldlen = len;
        ret = mysendto(s, &buf, len, flags, to, tolen);
        if(ret >= 0) {
            // call real function
        } else if(ret == SOCKET_ERROR) {
            goto quit_and_free;
        } else {
            ret = oldlen;
            goto quit_and_free;
        }
        len = ret;
    }
    ret = _sendto(s, buf, len, flags, to, tolen);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "sendto %d: %d\n", s, ret);
    #endif
quit_and_free:
    if(mysendto) {
        if(oldbuf != buf) free(buf);
        if(ret == len) ret = oldlen;    // restore the old len if there have been no errors
    }
    return(ret);
}



// return value: If no error occurs and the send operation has completed immediately, WSASend returns zero
#define WSASend_(X) int CALLING_CONVENTION (X)(SOCKET s, LPWSABUF lpBuffers, DWORD dwBufferCount, LPDWORD lpNumberOfBytesSent, DWORD dwFlags, LPWSAOVERLAPPED lpOverlapped, LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine)
CALLIT(WSASend) {
    DWORD   i;
    int     n,
            bypass      = 0,
            ret         = SOCKET_ERROR,
            *oldlen     = 0;
    char    **oldbuf    = NULL;

    if(fdcap) {
        n = return_sockets_num(s);
        if(n >= 0) {
            for(i = 0; i < dwBufferCount; i++) {
                acp_dump(
                    fdcap, sockets[n].type, sockets[n].protocol,
                    sockets[n].sip, sockets[n].sport, sockets[n].dip, sockets[n].dport,
                    (uint8_t *)lpBuffers[i].buf, lpBuffers[i].len,
                    &sockets[n].seq1, &sockets[n].ack1, &sockets[n].seq2, &sockets[n].ack2);
            }
        }
    }
    if(mysend) {
        oldbuf = calloc(sizeof(char *), dwBufferCount);
        oldlen = calloc(sizeof(int), dwBufferCount);
        for(i = 0; i < dwBufferCount; i++) {
            oldbuf[i] = lpBuffers[i].buf;
            oldlen[i] = lpBuffers[i].len;
            lpBuffers[i].len = mysend(s, &lpBuffers[i].buf, lpBuffers[i].len, dwFlags);
            if((int)lpBuffers[i].len >= 0) {
                // ok
            } else if((int)lpBuffers[i].len == SOCKET_ERROR) {
                ret = SOCKET_ERROR; // re-specify it
                goto quit_and_free;
            } else {
                ret = 0;
                bypass = 1;
            }
        }
        if(bypass) goto quit_and_free;
    }
    ret = _WSASend(s, lpBuffers, dwBufferCount, lpNumberOfBytesSent, dwFlags, lpOverlapped, lpCompletionRoutine);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSASend %d: %d\n", s, ret);
    #endif
quit_and_free:
    if(mysend) {
        for(i = 0; i < dwBufferCount; i++) {    // the data has been already sent, so now it's needed only to restore the original situation
            if(oldbuf[i] != lpBuffers[i].buf) { // means that the buffer has been reallocated/modified
                free(lpBuffers[i].buf);
                lpBuffers[i].buf = oldbuf[i];
            }
            lpBuffers[i].len = oldlen[i];
        }
        free(oldbuf);   // free it, don't worry it's only an index
        free(oldlen);
    }
    return(ret);
}



// return value: If no error occurs and the send operation has completed immediately, WSASendTo returns zero
#define WSASendTo_(X) int CALLING_CONVENTION (X)(SOCKET s, LPWSABUF lpBuffers, DWORD dwBufferCount, LPDWORD lpNumberOfBytesSent, DWORD dwFlags, const struct sockaddr *lpTo, int iToLen, LPWSAOVERLAPPED lpOverlapped, LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine)
CALLIT(WSASendTo) {
    DWORD   i;
    int     n,
            bypass      = 0,
            ret         = SOCKET_ERROR,
            *oldlen     = 0;
    char    **oldbuf    = NULL;

    if(fdcap) {
        n = return_sockets_num(s);
        if(n >= 0) {
            for(i = 0; i < dwBufferCount; i++) {
                acp_dump(
                    fdcap, sockets[n].type, sockets[n].protocol,
                    sockets[n].sip, sockets[n].sport, get_ip(lpTo), get_port(lpTo),
                    (uint8_t *)lpBuffers[i].buf, lpBuffers[i].len,
                    NULL, NULL, NULL, NULL);
            }
        }
    }
    if(mysendto) {
        oldbuf = calloc(sizeof(char *), dwBufferCount);
        oldlen = calloc(sizeof(int), dwBufferCount);
        for(i = 0; i < dwBufferCount; i++) {
            oldbuf[i] = lpBuffers[i].buf;
            oldlen[i] = lpBuffers[i].len;
            lpBuffers[i].len = mysendto(s, &lpBuffers[i].buf, lpBuffers[i].len, dwFlags, lpTo, iToLen);
            if((int)lpBuffers[i].len >= 0) {
                // ok
            } else if((int)lpBuffers[i].len == SOCKET_ERROR) {
                ret = SOCKET_ERROR; // re-specify it
                goto quit_and_free;
            } else {
                ret = 0;
                bypass = 1;
            }
        }
        if(bypass) goto quit_and_free;
    }
    ret = _WSASendTo(s, lpBuffers, dwBufferCount, lpNumberOfBytesSent, dwFlags, lpTo, iToLen, lpOverlapped, lpCompletionRoutine);
    #ifdef DEBUG
        if(fddbg) fprintf(fddbg, "WSASendTo %d: %d\n", s, ret);
    #endif
quit_and_free:
    if(mysendto) {
        for(i = 0; i < dwBufferCount; i++) {    // the data has been already sent, so now it's needed only to restore the original situation
            if(oldbuf[i] != lpBuffers[i].buf) { // means that the buffer has been reallocated/modified
                free(lpBuffers[i].buf);
                lpBuffers[i].buf = oldbuf[i];
            }
            lpBuffers[i].len = oldlen[i];
        }
        free(oldbuf);   // free it, don't worry it's only an index
        free(oldlen);
    }
    return(ret);
}



// AcceptEx, maybe in future but for the moment I'm not aware of programs which use it


