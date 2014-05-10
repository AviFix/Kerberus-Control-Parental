////////////////////////////////////////////////////////////////////////////////
//
// External variable definitions
//
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//
// External defines from lspguid.cpp and provider.cpp
//
////////////////////////////////////////////////////////////////////////////////

// Private heap used for all allocations in LSP as well as install time


class GlobalVars
{
public:
	// Global GUID under which the LSP dummy entry is installed under
	static GUID gProviderGuid;                // GUID of our dummy hidden entry
	// Critical section for printing debug info (to prevent intermingling of messages)
	static CRITICAL_SECTION gDebugCritSec;
	static CRITICAL_SECTION gOverlappedCS;    // Used in overlapped IO handling
	static CRITICAL_SECTION gCriticalSection; // Critical section for initialization and socket list manipulation

	static HINSTANCE gDllInstance;            // Instance passed to DllMain
	static INT gLayerCount;                   // Number of layered protocol entries for LSP
	static PROVIDER* gBaseInfo;               // Provider structures for each layered protocol
	static HANDLE gAddContextEvent;   // Event signaled whenver new socket context is added to a PROVIDER
	static HANDLE gIocp;              // Completion port handle
	static WSPUPCALLTABLE   gMainUpCallTable;   // Upcall functions given to us by Winsock
	static HANDLE gLspHeap;
};
