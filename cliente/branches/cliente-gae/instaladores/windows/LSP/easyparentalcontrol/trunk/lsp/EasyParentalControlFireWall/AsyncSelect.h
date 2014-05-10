////////////////////////////////////////////////////////////////////////////////
//
// AsyncSelect.cpp prototypes
//
////////////////////////////////////////////////////////////////////////////////

// Retrieves the async worker window and creates it if it hasn't already been
HWND 
GetWorkerWindow(
    );

// Issues the shutdown command to thread handling window messages
int 
StopAsyncWindowManager(
    );
