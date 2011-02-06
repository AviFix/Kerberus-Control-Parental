int WSPAPI WSCInstallProvider(
IN LPGUID lpProviderId,
IN const WCHAR FAR * lpszProviderDllPath,
IN const LPWSAPROTOCOL_INFOW lpProtocolInfoList,
IN DWORD dwNumberOfEntries,
OUT LPINT lpErrno
);

int WSPAPI WSCDeinstallProvider(
IN LPGUID lpProviderId,
OUT LPINT lpErrno
);
