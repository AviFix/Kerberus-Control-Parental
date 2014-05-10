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
#pragma unmanaged

#include "StdAfx.h"
#include "Types.h"
#include "GlobalVars.h"


//
// This is the hardcoded guid for our dummy (hidden) catalog entry
//
GUID GlobalVars::gProviderGuid = { // Created by Pascal for EasyParentalControlFireWall on 06 july 2010
    0x30052007,
    0x9736,
    0x11d1,
    {0x93, 0x7f, 0x00, 0xc0, 0x4f, 0xad, 0x86, 0x0d}
};

CRITICAL_SECTION GlobalVars::gOverlappedCS;
CRITICAL_SECTION GlobalVars::gDebugCritSec;

HINSTANCE GlobalVars::gDllInstance = NULL;// DLL instance handle
INT GlobalVars::gLayerCount = 0;    // Number of base providers we're layered over

// Handle to a private heap used by the LSP and the installer
HANDLE GlobalVars::gLspHeap = NULL;

CRITICAL_SECTION    GlobalVars::gCriticalSection;   // Critical section for initialization and socket list
WSPUPCALLTABLE      GlobalVars::gMainUpCallTable;   // Winsock upcall table
LPPROVIDER          GlobalVars::gBaseInfo = NULL;   // Provider information for each layer under us
HANDLE              GlobalVars::gAddContextEvent=NULL;  // Event to set when adding socket context

