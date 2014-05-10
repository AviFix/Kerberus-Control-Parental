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

// Parts of this file is derived from the winsock lsp sample, that can be found in the Microsoft Windows SDK v7.0 
#pragma unmanaged

#include "StdAfx.h"
#include "Types.h"
#include "GlobalVars.h"

//
// Function: GetLspGuid
//
// Description:
//      This function is exported by the DLL and it returns the GUID under
//      which the LSP (hidden) entry is to be installed. Note that this export
//      is not required to write an LSP but it is here to make the installer code
//      easier since the LSP DLL and the installer at least need to know the GUID
//      of the hidden dummy entry of the LSP. Using this export allows the installer
//      to query each LSP instance of its GUID so that it may install it.
//
void WSPAPI GetLspGuid(
    LPGUID lpGuid
    )
{
    memcpy( lpGuid, &GlobalVars::gProviderGuid, sizeof( GUID ) );
}
