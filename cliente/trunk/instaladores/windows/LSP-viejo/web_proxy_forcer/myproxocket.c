/*
    by Luigi Auriemma
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock.h>
#include <windows.h>



#define VER         "web proxy forcer 0.1"
#define PROXYIP     "127.0.0.1"     // the IP of the proxy to use
#define PROXYPORT   8080            // the port of the proxy
#define MAXMYDB     64              // don't need to be big, 2 was more than enough



unsigned int    proxy_ip    = 0;
unsigned short  proxy_port  = 0;
struct {
    SOCKET          s;
    unsigned int    ip;
    unsigned short  port;
} mydb[MAXMYDB]             = {{0,0,0}};
// mydb is required because it's not possible to see what is send() done at the beginning of the connection because
// proxocket can't monitor the connections but the single calls so with this temporary db it's a joke to do the job



static HMODULE wsock = NULL;
static WINAPI int (*real_send)(SOCKET s, char *buf, int len, int flags) = NULL;



unsigned int str2ip(unsigned char *data) {
    unsigned    a, b, c, d;

    if(!data[0]) return(0);
    sscanf(data, "%u.%u.%u.%u", &a, &b, &c, &d);
    return((a & 0xff) | ((b & 0xff) << 8) | ((c & 0xff) << 16) | ((d & 0xff) << 24));
}



unsigned char *ip2str(unsigned int ip) {
    static unsigned char  data[16];

    sprintf(data, "%hhu.%hhu.%hhu.%hhu",
        (ip & 0xff), ((ip >> 8) & 0xff), ((ip >> 16) & 0xff), ((ip >> 24) & 0xff));
    return(data);
}



unsigned short net16(unsigned short num) {
    int         endian = 1; // big endian

    if(!*(char *)&endian) return(num);
    return((num << 8) | (num >> 8));
}



unsigned int net32(unsigned int num) {
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



void init_myproxocket(void) {   // in this example I use this function for loading the real sockets function in case we want to use them
    char    winpath[MAX_PATH];

    if(wsock) return;

    GetSystemDirectory(winpath, sizeof(winpath));
    strcat(winpath, "\\ws2_32_orig.dll");

    wsock = LoadLibrary(winpath);
    if(!wsock) return;

    real_send   = (void *)GetProcAddress(wsock, "send");

    proxy_ip    = inet_addr(PROXYIP);
    proxy_port  = htons(PROXYPORT);
}



void free_myproxocket(void) {
    if(wsock) {
        FreeLibrary(wsock);
        wsock = NULL;
    }
}



int myconnect(SOCKET s, const struct sockaddr *name, int namelen) {
    unsigned int    ip;
    unsigned short  port;
    int             i;

    ip   = ((struct sockaddr_in *)name)->sin_addr.s_addr;
    port = ntohs(((struct sockaddr_in *)name)->sin_port);

    // skip local IP, Firefox REQUIRES at least that 127.0.0.1 is not proxified at the beginning
    if(((ip & 0xff) == 127) || ((ip & 0xff) == 192) || ((ip & 0xff) == 10)) return(0);

    ((struct sockaddr_in *)name)->sin_addr.s_addr = proxy_ip;
    ((struct sockaddr_in *)name)->sin_port        = proxy_port;

    for(i = 0; i < MAXMYDB; i++) {
        if(mydb[i].s) continue; // already occupied
        mydb[i].s    = s;       // fill the field
        mydb[i].ip   = ip;
        mydb[i].port = port;
        break;
    }
    return(0);
}



int mysend(SOCKET s, u_char **retbuf, int len, int flags) {
    int     i,
            tmplen;
    u_char  *buf = *retbuf, // do NOT touch this
            tmp[100],
            *p;

    for(i = 0; i < MAXMYDB; i++) {
        if(!mydb[i].s) continue;
        if(mydb[i].s != s) continue;
        mydb[i].s = 0;          // reset it

        for(p = buf; p < (buf + len); p++) {
            if(*p == ' ') {
                p++;
                real_send(s, buf, p - buf, 0);

                tmplen = sprintf(tmp,
                    "http://%hhu.%hhu.%hhu.%hhu:%hu",
                    (mydb[i].ip & 0xff), ((mydb[i].ip >> 8) & 0xff), ((mydb[i].ip >> 16) & 0xff), ((mydb[i].ip >> 24) & 0xff),
                    mydb[i].port);
                real_send(s, tmp, tmplen, 0);

                len -= (p - buf);
                buf = p;
                break;
            }
        }
        break;
    }

    *retbuf = buf;  // do NOT touch this
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


