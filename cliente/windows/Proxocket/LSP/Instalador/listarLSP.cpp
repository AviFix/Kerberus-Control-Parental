#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#define WINSOCK_API_LINKAGE
#include <winsock2.h>
#include <ws2spi.h>
#include <wtypes.h>
#include <assert.h>
#include <winnt.h>
#include <stdlib.h>
#include <stdio.h>

char *ExpandServiceFlags(DWORD serviceFlags)
{
	/* A little utility function to make sense of all those bit flags */
	/* The following code leaks. Yeah, I know.. Go find Buffer 0v3rfl0w$ :-) */

	char *serviceFlagsText = (char *) malloc (2048);

	memset (serviceFlagsText, '\0', 2048);

	char *strip_comma;

	/* Hey - it's only for printing and demo purposes.. */

	if (serviceFlags & XP1_CONNECTIONLESS)
	{
		strcat (serviceFlagsText, "Connectionless, ");
	}

	if (serviceFlags & XP1_GUARANTEED_ORDER)
	{
		strcat (serviceFlagsText, "Guaranteed Order, ");
	}

	if (serviceFlags & XP1_GUARANTEED_DELIVERY)
	{
		strcat (serviceFlagsText, "Message Oriented, ");
	}

	if (serviceFlags & XP1_MESSAGE_ORIENTED)
	{
		strcat (serviceFlagsText, "Message Oriented, ");
	}

	if (serviceFlags & XP1_CONNECT_DATA )
	{
		strcat (serviceFlagsText, "Connect Data, ");
	}

	if (serviceFlags & XP1_DISCONNECT_DATA )
	{
		strcat (serviceFlagsText, "Disconnect Data, ");
	}

	if (serviceFlags & XP1_SUPPORT_BROADCAST )
	{
		strcat (serviceFlagsText, "Broadcast Supported, ");
	}

	if (serviceFlags & XP1_EXPEDITED_DATA )
	{
		strcat (serviceFlagsText, "Urgent Data, ");
	}

	if (serviceFlags & XP1_QOS_SUPPORTED )
	{
		strcat (serviceFlagsText, "QoS supported, ");
	}

	/*
	* While we're quick and dirty, let's get as dirty as possible..
	*/

	strip_comma = strrchr(serviceFlagsText,',');
	
	if (strip_comma)
		*strip_comma = '\0';
		
	return (serviceFlagsText);
}

void PrintProtocolInfo (LPWSAPROTOCOL_INFOW prot)
{
	wprintf (L"Protocol Name: %s\n",prot->szProtocol); /* #%^@$! UNICODE...*/
	printf ("\tServiceFlags1: %d (%s)\n",
	prot->dwServiceFlags1,
	ExpandServiceFlags(prot->dwServiceFlags1));
	printf ("\tProvider Flags: %d\n",prot->dwProviderFlags);
	printf ("\tNetwork Byte Order: %s\n",
	(prot->iNetworkByteOrder == BIGENDIAN) ? "Big Endian" : "Little Endian");
	printf ("\tVersion: %d\n", prot->iVersion);
	printf ("\tAddress Family: %d\n", prot->iAddressFamily);
	printf ("\tSocket Type: ");
	switch (prot->iSocketType)
	{
		case SOCK_STREAM:
			printf ("STREAM\n");
			break;
		case SOCK_DGRAM:
			printf ("DGRAM\n");
			break;
		case SOCK_RAW:
			printf ("RAW\n");
			break;
		default:
			printf (" Some other type\n");
	}
	printf ("\tProtocol: ");
	switch (prot->iProtocol)
	{
		case IPPROTO_TCP:
			printf ("TCP/IP\n");
			break;
		case IPPROTO_UDP:
			printf ("UDP/IP\n");
			break;
		default:
			printf ("some other protocol\n");
	}
}

int _cdecl main( int argc, char** argv)
{
	LPWSAPROTOCOL_INFOW bufProtocolInfo = NULL;
	DWORD
	dwSize = 0;
	INT
	dwError;
	INT
	iNumProt;
	
	/*
	* Enum Protocols - First, obtain size required
	*/
	
	printf("Sample program to enumerate Protocols\n");
	WSCEnumProtocols(NULL,
	// lpiProtocols
	bufProtocolInfo,
	// lpProtocolBuffer
	& dwSize,
	// lpdwBufferLength
	& dwError);
	// lpErrno
	bufProtocolInfo = (LPWSAPROTOCOL_INFOW) malloc(dwSize);
	if (!bufProtocolInfo){
		fprintf (stderr,"SHOOT! Can't MALLOC!!\n");
		exit(1);
	}
	
	/* Now, Enum */
	
	iNumProt = WSCEnumProtocols(
	NULL,
	bufProtocolInfo,
	&dwSize,
	&dwError);
	// lpiProtocols
	// lpProtocolBuffer
	// lpdwBufferLength
	if (SOCKET_ERROR == iNumProt)
	{
		fprintf(stderr,"Darn! Can't Enum!!\n");
		exit(1);
	}
	printf("%d Protocols detected:\n", iNumProt);
	for (int i=0; i < iNumProt;	i++)
	{
		PrintProtocolInfo(&bufProtocolInfo[i]);
		printf ("-------\n");
	}
	printf("Done");
	return(0);
}
