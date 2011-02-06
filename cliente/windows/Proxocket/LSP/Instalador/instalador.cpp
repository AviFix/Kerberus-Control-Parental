//~ int WSPAPI WSCInstallProvider(
//~ IN LPGUID lpProviderId,
//~ IN const WCHAR FAR * lpszProviderDllPath,
//~ IN const LPWSAPROTOCOL_INFOW lpProtocolInfoList,
//~ IN DWORD dwNumberOfEntries,
//~ OUT LPINT lpErrno
//~ );
//~ 
//~ int WSPAPI WSCDeinstallProvider(
//~ IN LPGUID lpProviderId,
//~ OUT LPINT lpErrno
//~ );


INT InstallProvider(OUT PDWORD CatalogId)
{
	WSAPROTOCOL_INFOW proto_info;
	int	rc, errno;
	GUID someGUID = { 0x10241975, 0x0000, 0x0000, 0x0000, 0x1234567890 };
	
	/* populate PROTOCOL_INFO */
	
	memset(&proto_info , ‘\0’, sizeof(proto_info)); /* Tabula Rasa */
	proto_info.dwProviderFlags = PFL_HIDDEN; /* :-) */
	proto_info.ProviderId = someGUID;
	proto_info.ProtocolChain.ChainLen = LAYERED_PROTOCOL;
	proto_info.iAddressFamily = AF_INET;
	proto_info.iSocketType = SOCK_STREAM;
	proto_info.iProtocol = IPPROTO_TCP;
	proto_info.iMaxSockAddr = proto_info.iMinSockAddr = 16;
	proto_info.iNetworkByteOrder = BIGENDIAN;
	proto_info.iSecurityScheme=SECURITY_PROTOCOL_NONE; /* Security? THIS?! HA! */
	wcscpy(proto_info.szProtocol, L”SecuredFamily”);
	
	rc = WSCInstallProvider(&LayeredProviderGuid,
	L“SecuredFamily.dll", // lpszProviderDllPath
	&proto_info,
	// lpProtocolInfoList
	1,
	// dwNumberOfEntries (1 too many..)
	&errno);
	
	// lpErrno
	/* Pass this back to our caller – for reordering.. */
	*CatalogId = proto_info.dwCatalogEntryId;
	return(rc);
}
b
