/*
  Example of myproxocket.dll by Luigi Auriemma

  if you don't know it, myproxocket.dll is a dll read by proxocket (ws2_32.dll/wsock32.dll)
  and used to control some functions like send, recv, connect and so on.
  all you need to do is just creating a myproxocket.dll file exporting the CDECL functions
  explained below

  The following are all the available functions under your control:

  myfunction <- original functions     execution BEFORE or AFTER the original functions and return value
  ------------------------------------------------------------------------------------------------------
  mysocket   <- socket, WSASocket      BEFORE  >= 0: returns your value: INVALID_SOCKET: returns INVALID_SOCKET, any_other_value: calls the original function
  myconnect  <- connect, WSAConnect    BEFORE  0: calls real connect, SOCKET_ERROR: returns SOCKET_ERROR, any_other_value: bypasses the real connect and returns 0
  myaccept   <- accept, WSAAccept      AFTER   the main program will receive the same return value returned by you
  mybind     <- bind                   BEFORE  0: calls real bind, SOCKET_ERROR: returns SOCKET_ERROR, any_other_value: bypasses the real bind and returns 0
  myclose    <- closesocket            AFTER   the main program will receive the same return value returned by you
  myrecv     <- recv, WSARecv          AFTER   the main program will receive the same return value returned by you
  myrecvfrom <- recvfrom, WSARecvFrom  AFTER   the main program will receive the same return value returned by you
  mysend     <- send, WSASend          BEFORE  >= 0: calls real send, SOCKET_ERROR: returns SOCKET_ERROR, any_other_value: bypasses the real send/WSASend and returns the original len
  mysendto   <- sendto, WSASendTo      BEFORE  >= 0: calls real sendto, SOCKET_ERROR: returns SOCKET_ERROR, any_other_value: bypasses the real sendto/WSASendTo and returns the original len

  in the AFTER functions remember that, obviously, they are called only if the original function succeded
  so if the real recv() returned SOCKET_ERROR myrecv() will be NOT called.
  note: in case you are asking what is the value of SOCKET_ERROR/INVALID_SOCKET it's -1

  as visible in this code, all the my* functions have the same prototype of the original homonym functions
  (except mysend and mysendto due to technical reasons) so there are no possibilities of errors or
  misunderstandings.

  for example, in myrecv and myrecvfrom the len value is the one returned by recv/recvfrom and buf
  contains the data received, while in myaccept the s value is the socket returned by accept().
  so, if the original recv failed (connection lost) myrecv will be NOT called.

  in mysend, instead, you can control the content and length of the data before the real sending, and the
  return value will be used as length for the original function, if you return a value which is not
  SOCKET_ERROR and is minor than 0 (for example -0x77777777) the original send() will be NOT called
  allowing you to drop a packet or to generate a socket error visible by the main program.

  use the following instructions for retrieving IP and port from a sockaddr structure:
    u32     ip   = 0;
    u16     port = 0;
    if(name) {
        ip   = ((struct sockaddr_in *)name)->sin_addr.s_addr;
        port = ntohs(((struct sockaddr_in *)name)->sin_port);
    }

  remember that you SHOULD delete ALL the my* functions that you don't use, so if you need only to modify
  the incoming UDP packets you can remove mysocket, myconnect, mybind, myaccept and all the other functions
  except myrecvfrom (even DllMain can be removed).

  as visible, in this example there are already various real socket functions which can be used in any
  moment without losing time to implement them: socket connect, accept, bind, close, recv, recvfrom, send
  and sendto.

  at the moment this plugin must be considered experimental so any feedback about improving it is highly
  welcome and needed.

  gcc -o myproxocket.dll myproxocket.c -shared 
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock.h>
#include <windows.h>



u_int str2ip(u_char *data) {
    unsigned    a, b, c, d;

    if(!data[0]) return(0);
    sscanf(data, "%u.%u.%u.%u", &a, &b, &c, &d);
    return((a & 0xff) | ((b & 0xff) << 8) | ((c & 0xff) << 16) | ((d & 0xff) << 24));
}



u_char *ip2str(u_int ip) {
    static u_char  data[16];

    sprintf(data, "%hhu.%hhu.%hhu.%hhu",
        (ip & 0xff), ((ip >> 8) & 0xff), ((ip >> 16) & 0xff), ((ip >> 24) & 0xff));
    return(data);
}


u_short net16(u_short num) {
    int         endian = 1; // big endian

    if(!*(char *)&endian) return(num);
    return((num << 8) | (num >> 8));
}



u_int net32(u_int num) {
    int         endian = 1; // big endian

    if(!*(char *)&endian) return(num);
    return(((num & 0xff000000) >> 24) |
           ((num & 0x00ff0000) >>  8) |
           ((num & 0x0000ff00) <<  8) |
           ((num & 0x000000ff) << 24));
}



#define htons       net16
#define ntohs       net16
#define htonl       net32
#define ntohl       net32
#define inet_ntoa   ip2str
#define inet_addr   str2ip



    /* code which adds Winsock support to your hook, so you can use the original functions everytime you want! */
    /* it's not (easily) possible to link the winsock functions directly in this dll otherwise will be loaded the */
    /* bridge functions of proxocket (ws2_32.dll is in the same folder) */

static HMODULE wsock = NULL;
static WINAPI SOCKET (*real_socket)(int af, int type, int protocol) = NULL;
static WINAPI int (*real_connect)(SOCKET s, const struct sockaddr *name, int namelen) = NULL;
static WINAPI SOCKET (*real_accept)(SOCKET s, const struct sockaddr *name, int *namelen) = NULL;
static WINAPI int (*real_bind)(SOCKET s, const struct sockaddr *name, int namelen) = NULL;
static WINAPI int (*real_close)(SOCKET s) = NULL;
static WINAPI int (*real_recv)(SOCKET s, char *buf, int len, int flags) = NULL;
static WINAPI int (*real_recvfrom)(SOCKET s, char *buf, int len, int flags, struct sockaddr *from, int *fromlen) = NULL;
static WINAPI int (*real_send)(SOCKET s, char *buf, int len, int flags) = NULL;
static WINAPI int (*real_sendto)(SOCKET s, char *tbuf, int len, int flags, const struct sockaddr *to, int tolen) = NULL;



void init_myproxocket(void) {   // in this example I use this function for loading the real sockets function in case we want to use them
    char    winpath[MAX_PATH];

    if(wsock) return;   // already set

    GetSystemDirectory(winpath, sizeof(winpath));
    strcat(winpath, "\\ws2_32.dll");

    wsock = LoadLibrary(winpath);
    if(!wsock) return;

    real_socket    = (void *)GetProcAddress(wsock, "socket");
    real_connect   = (void *)GetProcAddress(wsock, "connect");
    real_accept    = (void *)GetProcAddress(wsock, "accept");
    real_bind      = (void *)GetProcAddress(wsock, "bind");
    real_close     = (void *)GetProcAddress(wsock, "close");
    real_recv      = (void *)GetProcAddress(wsock, "recv");
    real_recvfrom  = (void *)GetProcAddress(wsock, "recvfrom");
    real_send      = (void *)GetProcAddress(wsock, "send");
    real_sendto    = (void *)GetProcAddress(wsock, "sendto");
}



void free_myproxocket(void) {
    if(wsock) {
        FreeLibrary(wsock);
        wsock = NULL;
    }
}



    // this function can be used also to know only if a string exists or not, it's enough to use NULL instead of new like in the example in myrecv
u_char *find_replace_string(u_char *buf, int *len, u_char *old, u_char *new) {
    int     i,
            tlen,
            oldlen,
            newlen,
            found;
    u_char  *nbuf,
            *p;

    found  = 0;
    oldlen = strlen(old);
    tlen   = *len - oldlen;

    for(i = 0; i <= tlen; i++) {
        if(!strnicmp(buf + i, old, oldlen)) found++;
    }
    if(!found) return(buf); // nothing to change: return buf or a positive value

    if(!new) return(NULL);  // if we want to know only if the searched string has been found, we will get NULL if YES and buf if NOT!!!
    newlen = strlen(new);

    if(newlen <= oldlen) {  // if the length of new string is equal/minor than the old one don't waste space for another buffer
        nbuf = buf;
    } else {                // allocate the new size
        nbuf = malloc(*len + ((newlen - oldlen) * found));
    }

    p = nbuf;
    for(i = 0; i <= tlen;) {
        if(!strnicmp(buf + i, old, oldlen)) {
            memcpy(p, new, newlen);
            p += newlen;
            i += oldlen;
        } else {
            *p++ = buf[i];
            i++;
        }
    }
    while(i < *len) {
        *p++ = buf[i];
        i++;
    }
    *len = p - nbuf;
    return(nbuf);
}



SOCKET __cdecl mysocket(int af, int type, int protocol) {
    // example: convert a TCP connection in a TCP packets-oriented stream... I guess doesn't work
    if(type == SOCK_STREAM) {
        return(real_socket(af, SOCK_DGRAM, protocol));
    }

    // example: convert a TCP connection in an UDP connection, indeed also UDP can be handled with connect, send and recv
    if(protocol == IPPROTO_TCP) {
        return(real_socket(af, type, IPPROTO_UDP));
    }

    // example: if the family is AF_INET we return an error which is received by the main program
    if(af == AF_INET) {
        return(INVALID_SOCKET);
    }

    // call the real socket/WSASocket
    return(-0x77777777); // negative and different than INVALID_SOCKET
}



int __cdecl myconnect(SOCKET s, const struct sockaddr *name, int namelen) {
    // example: avoid the connection to host 1.2.3.4
    if(((struct sockaddr_in *)name)->sin_addr.s_addr == inet_addr("1.2.3.4")) {
        return(SOCKET_ERROR);
    }

    // example: avoid the connection to any port 1234
    if(ntohs(((struct sockaddr_in *)name)->sin_port) == 1234) {
        return(SOCKET_ERROR);
    }

    // example: redirect any connection from host 1.2.3.4 to host 192.168.0.2
    if(((struct sockaddr_in *)name)->sin_addr.s_addr == inet_addr("1.2.3.4")) {
        ((struct sockaddr_in *)name)->sin_addr.s_addr = inet_addr("192.168.0.2");
    }
    return(0);
}



SOCKET __cdecl myaccept(SOCKET s, const struct sockaddr *name, int *namelen) {
    // at the moment this function can't be really used to avoid connections from a specific host
    // but if we want to avoid connection from 1.2.3.4 we can "try" the following although it's not very good
    if(((struct sockaddr_in *)name)->sin_addr.s_addr == inet_addr("1.2.3.4")) {
        return(0);  // don't return SOCKET_ERROR or the main program could decide to exit/quit
    }
    return(s);
}



int __cdecl mybind(SOCKET s, const struct sockaddr *name, int namelen) {
    // example: avoid the binding of interface 192.168.0.1, the main program could quit
    if(((struct sockaddr_in *)name)->sin_addr.s_addr == inet_addr("192.168.0.1")) {
        return(SOCKET_ERROR);
    }

    // example: avoid the binding of port 1234, the main program could quit
    if(ntohs(((struct sockaddr_in *)name)->sin_port) == 1234) {
        return(SOCKET_ERROR);
    }

    // example: substituite the binding of interface 192.168.0.1 with 10.10.10.10
    if(((struct sockaddr_in *)name)->sin_addr.s_addr == inet_addr("192.168.0.1")) {
        ((struct sockaddr_in *)name)->sin_addr.s_addr = inet_addr("10.10.10.10");
    }

    // example: as above but uses 127.0.0.1 instead of 0.0.0.0 (INADDR_ANY) so the main program can be used only locally
    if(((struct sockaddr_in *)name)->sin_addr.s_addr == htonl(INADDR_ANY)) {
        ((struct sockaddr_in *)name)->sin_addr.s_addr = inet_addr("127.0.0.1");
    }
    return(0);
}



int __cdecl myclose(SOCKET s) {
    // example: this function has only for your internal use
    // for example if you need to track all the sockets and you need to know when they are closed to free memory or remove an entry
    return(0);
}



int __cdecl myrecv(SOCKET s, u_char *buf, int len, int flags) {
    // example: if buf contains the word "hello" return a socket error (the main program will close the socket or will exit)
    if(!find_replace_string(buf, &len, "hello", NULL)) {
        return(SOCKET_ERROR);
    }

    // example: fill all the bytes of buf with 'A's
    memset(buf, 'A', len);

    // example: return 1 byte less than the bytes we have received (like returning 99 instead of 100)
    if(len > 1) len--;

    // remember that a value <= 0 is usually considered an error by the main program when handles TCP streams
    // while for any other packet (UDP, ICMP and so on) it can be 0 without problems
    return(len);
}



int __cdecl myrecvfrom(SOCKET s, u_char *buf, int len, int flags, struct sockaddr *from, int *fromlen) {
    // examples: watch the examples of myrecv

    // example: drop any packet from the host 1.2.3.4
    if(((struct sockaddr_in *)from)->sin_addr.s_addr == inet_addr("1.2.3.4")) {
        return(SOCKET_ERROR);
    }

    return(len);
}



int __cdecl mysend(SOCKET s, u_char **retbuf, int len, int flags) {
    u_char  *buf = *retbuf; // do NOT touch this

    // if you have allocated a new buffer it will be AUTOMATICALLY freed by proxocket so
    // remember only to NOT return a const/static buffer which cannot be freed!

    // example: send a packet of 10000 'A's if the one we want to send contains the "hello" bytes
    if(!find_replace_string(buf, &len, "hello", NULL)) {
        len = 10000;
        buf = malloc(len);
        memset(buf, 'A', len);
        goto quit;
    }

    // replace any occurrency of "hello" with that new string
    buf = find_replace_string(buf, &len, "hello", "don't tell me goodbye send()");

    // send the following message before the one in which we are: real_send and then this send
    char message[] = "yes, I can use send() in any moment!";
    real_send(s, message, strlen(message), flags);

    // do not execute this send
    len = -0x77777777;

    // "quit" because you must remember to update retbuf in case you allocated a new buf
    quit:
    *retbuf = buf;  // do NOT touch this
    // return >= 0 for calling the real send
    // return SOCKET_ERROR avoids the sending of the data but returns SOCKET_ERROR to the main program, use it to generate a socket error
    // return any other value to skip the send function
    return(len);
}



int __cdecl mysendto(SOCKET s, u_char **retbuf, int len, int flags, const struct sockaddr *to, int tolen) {
    u_char  *buf = *retbuf; // do NOT touch this

    // if you have allocated a new buffer it will be AUTOMATICALLY freed by proxocket so
    // remember only to NOT return a const/static buffer which cannot be freed!

    // example: send a packet of 10000 'A's if the one we want to send contains the "hello" bytes
    if(!find_replace_string(buf, &len, "hello", NULL)) {
        len = 10000;
        buf = malloc(len);
        memset(buf, 'A', len);
        goto quit;
    }

    // replace any occurrency of "hello" with that new string
    buf = find_replace_string(buf, &len, "hello", "don't tell me goodbye sendto()");

    // send the following message before the one in which we are: real_sendto and then this sendto
    char message[] = "yes, I can use sendto() in any moment!";
    real_sendto(s, message, strlen(message), flags, to, tolen);

    // do not execute this sendto
    len = -0x77777777;  // negative and different than SOCKET_ERROR

    // "quit" because you must remember to update retbuf in case you allocated a new buf
    quit:
    *retbuf = buf;  // do NOT touch this
    // return >= 0 for calling the real sendto
    // return SOCKET_ERROR avoids the sending of the data but returns SOCKET_ERROR to the main program, use it to generate a socket error
    // return any other value to skip the sendto function
    return(len);
}



BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    switch(fdwReason) {
        case DLL_PROCESS_ATTACH: {
            DisableThreadLibraryCalls(hinstDLL);
            init_myproxocket(); // put your init here
            break;
        }
        case DLL_PROCESS_DETACH: {
            free_myproxocket(); // put anything to free here
            break;
        }
        default: break;
    }
    return(TRUE);
}


