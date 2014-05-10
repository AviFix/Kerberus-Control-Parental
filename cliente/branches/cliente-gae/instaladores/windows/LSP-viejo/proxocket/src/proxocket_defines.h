/*
    Copyright 2008,2009 Luigi Auriemma

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

#define _WINSOCK_H
#define _WINSOCK2_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <windows.h>



typedef uint8_t     u8;
typedef uint16_t    u16;
typedef uint32_t    u32;

typedef uint8_t     u_char;
typedef uint16_t    u_short;
typedef uint32_t    u_int;
typedef uint32_t    u_long;
typedef uint32_t    in_addr_t;
typedef int SOCKET;
#define INVALID_SOCKET (SOCKET)(~0)
#define SOCKET_ERROR	(-1)
#define SOCK_STREAM	1
#define SOCK_DGRAM	2
#define SOCK_RAW	3
#define IPPROTO_IP	0
#define IPPROTO_ICMP 1
#define IPPROTO_IGMP 2
#define IPPROTO_TCP	6
#define IPPROTO_UDP	17
#define IPPROTO_RAW	255
#define IPPROTO_MAX	256
#define IN_CLASSA(i)	(((long)(i)&0x80000000) == 0)
#define IN_CLASSA_NET	0xff000000
#define IN_CLASSA_NSHIFT	24
#define IN_CLASSA_HOST	0x00ffffff
#define IN_CLASSA_MAX	128
#define IN_CLASSB(i)	(((long)(i)&0xc0000000)==0x80000000)
#define IN_CLASSB_NET	   0xffff0000
#define IN_CLASSB_NSHIFT	16
#define IN_CLASSB_HOST	  0x0000ffff
#define IN_CLASSB_MAX	   65536
#define IN_CLASSC(i)	(((long)(i)&0xe0000000)==0xc0000000)
#define IN_CLASSC_NET	   0xffffff00
#define IN_CLASSC_NSHIFT	8
#define IN_CLASSC_HOST	  0xff
#define INADDR_ANY	      (u_long)0
#define INADDR_LOOPBACK	 0x7f000001
#define INADDR_BROADCAST	(u_long)0xffffffff
#define INADDR_NONE	0xffffffff
struct in_addr {
	union {
		struct { u_char s_b1,s_b2,s_b3,s_b4; } S_un_b;
		struct { u_short s_w1,s_w2; } S_un_w;
		u_long S_addr;
	} S_un;
#define s_addr  S_un.S_addr
#define s_host  S_un.S_un_b.s_b2
#define s_net   S_un.S_un_b.s_b1
#define s_imp   S_un.S_un_w.s_w2
#define s_impno S_un.S_un_b.s_b4
#define s_lh    S_un.S_un_b.s_b3
};
struct sockaddr_in {
	short	sin_family;
	u_short	sin_port;
	struct	in_addr sin_addr;
	char	sin_zero[8];
};
#define WSADESCRIPTION_LEN	256
#define WSASYS_STATUS_LEN	128
typedef struct WSAData {
	WORD	wVersion;
	WORD	wHighVersion;
	char	szDescription[WSADESCRIPTION_LEN+1];
	char	szSystemStatus[WSASYS_STATUS_LEN+1];
	unsigned short	iMaxSockets;
	unsigned short	iMaxUdpDg;
	char * 	lpVendorInfo;
} WSADATA;
typedef WSADATA *LPWSADATA;
struct sockaddr {
	u_short sa_family;
	char	sa_data[14];
};
typedef struct _WSABUF {
	unsigned long len;
	char *buf;
} WSABUF, *LPWSABUF;
typedef unsigned int	SERVICETYPE;
typedef struct _flowspec {
	unsigned int	TokenRate;
	unsigned int	TokenBucketSize;
	unsigned int	PeakBandwidth;
	unsigned int	Latency;
	unsigned int	DelayVariation;
	SERVICETYPE	ServiceType;
	unsigned int	MaxSduSize;
	unsigned int	MinimumPolicedSize;
   } FLOWSPEC, *PFLOWSPEC, *LPFLOWSPEC;
typedef struct _QualityOfService {
	FLOWSPEC	SendingFlowspec;
	FLOWSPEC	ReceivingFlowspec;
	WSABUF	ProviderSpecific;
} QOS, *LPQOS;
#define	WSAOVERLAPPED	OVERLAPPED
typedef	struct _OVERLAPPED	*LPWSAOVERLAPPED;
typedef void (WINAPI *LPWSAOVERLAPPED_COMPLETION_ROUTINE)(DWORD, DWORD, LPWSAOVERLAPPED, DWORD);
typedef unsigned int	GROUP;
#define	MAX_PROTOCOL_CHAIN 7
typedef struct _WSAPROTOCOLCHAIN {
	int ChainLen;
	DWORD ChainEntries[MAX_PROTOCOL_CHAIN];
} WSAPROTOCOLCHAIN, *LPWSAPROTOCOLCHAIN;
#define WSAPROTOCOL_LEN  255
typedef struct _WSAPROTOCOL_INFOA {
	DWORD dwServiceFlags1;
	DWORD dwServiceFlags2;
	DWORD dwServiceFlags3;
	DWORD dwServiceFlags4;
	DWORD dwProviderFlags;
	GUID ProviderId;
	DWORD dwCatalogEntryId;
	WSAPROTOCOLCHAIN ProtocolChain;
	int iVersion;
	int iAddressFamily;
	int iMaxSockAddr;
	int iMinSockAddr;
	int iSocketType;
	int iProtocol;
	int iProtocolMaxOffset;
	int iNetworkByteOrder;
	int iSecurityScheme;
	DWORD dwMessageSize;
	DWORD dwProviderReserved;
	CHAR szProtocol[WSAPROTOCOL_LEN+1];
} WSAPROTOCOL_INFOA, *LPWSAPROTOCOL_INFOA;
typedef struct _WSAPROTOCOL_INFOW {
	DWORD dwServiceFlags1;
	DWORD dwServiceFlags2;
	DWORD dwServiceFlags3;
	DWORD dwServiceFlags4;
	DWORD dwProviderFlags;
	GUID ProviderId;
	DWORD dwCatalogEntryId;
	WSAPROTOCOLCHAIN ProtocolChain;
	int iVersion;
	int iAddressFamily;
	int iMaxSockAddr;
	int iMinSockAddr;
	int iSocketType;
	int iProtocol;
	int iProtocolMaxOffset;
	int iNetworkByteOrder;
	int iSecurityScheme;
	DWORD dwMessageSize;
	DWORD dwProviderReserved;
	WCHAR  szProtocol[WSAPROTOCOL_LEN+1];
} WSAPROTOCOL_INFOW, * LPWSAPROTOCOL_INFOW;
typedef int (CALLBACK *LPCONDITIONPROC)(LPWSABUF, LPWSABUF, LPQOS, LPQOS, LPWSABUF, LPWSABUF, GROUP *, DWORD);
