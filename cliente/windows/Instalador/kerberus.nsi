;--------------------------------
;Include Modern UI

  !include "MUI.nsh"
;Seleccionamos el algoritmo de compresi�n utilizado para comprimir nuestra aplicaci�n
SetCompressor lzma

;--------------------------------
;Con esta opci�n alertamos al usuario cuando pulsa el bot�n cancelar y le pedimos confirmaci�n para abortar
;la instalaci�n
;Esta macro debe colocarse en esta posici�n del script sino no funcionara
  !define mui_abortwarning

;Definimos el valor de la variable VERSION, en caso de no definirse en el script
;podria ser definida en el compilador
!define VERSION "0.2"

;--------------------------------
;Pages

  ;Mostramos la p�gina de bienvenida 
  !insertmacro MUI_PAGE_WELCOME 
  ;p�gina donde se selecciona el directorio donde instalar nuestra aplicacion 
  !insertmacro MUI_PAGE_DIRECTORY 
  ;p�gina de instalaci�n de ficheros 
  !insertmacro MUI_PAGE_INSTFILES 
  ;p�gina final
  !insertmacro MUI_PAGE_FINISH

;p�ginas referentes al desinstalador
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

!insertmacro MUI_LANGUAGE "Spanish"

;;;;;;;;;;;;;;;;;;;;;;;;;
; Configuraci�n General ;
;;;;;;;;;;;;;;;;;;;;;;;;;
;Nombre del instalador
OutFile Kerberus-${VERSION}.exe

;Aqu� comprobamos que en la versi�n Inglesa se muestra correctamente el mensaje:
;Welcome to the $Name Setup Wizard
;Al tener reservado un espacio fijo para este mensaje, y al ser
;la frase en espa�ol mas larga:
; Bienvenido al Asistente de Instalaci�n de Aplicaci�n $Name
; no se ve el contenido de la variable $Name si el tama�o es muy grande
Name "Kerberus"
Caption "Kerberus ${VERSION} para Win32 Setup"

;Comprobacion de integridad del fichero activada
CRCCheck on
;Estilos visuales del XP activados
XPStyle on

;Indicamos cual ser� el directorio por defecto donde instalaremos nuestra
;aplicaci�n, el usuario puede cambiar este valor en tiempo de ejecuci�n.
InstallDir "$PROGRAMFILES\Kerberus"
; check if the program has already been installed, if so, take this dir
; as install dir
InstallDirRegKey HKLM SOFTWARE\KERBERUS "Install_Dir"

;Mensaje que mostraremos para indicarle al usuario que seleccione un directorio
DirText "Elija un directorio donde instalar la aplicaci�n:"
;Indicamos que cuando la instalaci�n se complete no se cierre el instalador autom�ticamente
AutoCloseWindow false
;Mostramos todos los detalles del la instalaci�n al usuario.
ShowInstDetails show
;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on
;Optimizamos nuestro paquete en tiempo de compilaci�n, es altamente recomendable habilitar siempre esta opci�n
SetDatablockOptimize on
;Habilitamos la compresi�n de nuestro instalador
SetCompress auto
;Personalizamos el mensaje de desinstalaci�n
UninstallText "Desinstalador de kerberus."

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta secci�n a�adimos los ficheros que forman nuestra aplicaci�n ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Section "Programa"
;Incluimos todos los ficheros que componen nuestra aplicaci�n
SetOutPath $INSTDIR\client
File   kerberus-daemon\dist\*.*

SetOutPath $INSTDIR\sync
File   kerberus-sync\dist\*.*

;Hacemos que la instalaci�n se realice para todos los usuarios del sistema
SetShellVarContext all

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"DisplayName" "Kerbers-client-${VERSION}"

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"UninstallString" '"$INSTDIR\uninstall.exe"'

WriteUninstaller "uninstall.exe"

WriteRegStr HKLM "Software\Kerberus" "InstallDir" $INSTDIR
       
WriteRegStr HKLM "Software\Kerberus" "Version" "${VERSION}"

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-client" "$INSTDIR\client\cliente.exe"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-sync" "$INSTDIR\sync\sincronizadorCliente.exe"

SectionEnd



;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;

Section "Uninstall"
        SetShellVarContext all
        RMDir /r $INSTDIR\Kerberus
        RMDir /r $INSTDIR
        DeleteRegKey HKLM "SOFTWARE\Kerberus"
        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus"
        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Run\Kerberus-client"
        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Run\Kerberus-sync"
SectionEnd
