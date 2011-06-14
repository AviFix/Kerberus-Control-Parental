;--------------------------------
;Include Modern UI

  !include "MUI.nsh"
;Seleccionamos el algoritmo de compresión utilizado para comprimir nuestra aplicación
SetCompressor lzma

;--------------------------------
;Con esta opción alertamos al usuario cuando pulsa el botón cancelar y le pedimos confirmación para abortar
;la instalación
;Esta macro debe colocarse en esta posición del script sino no funcionara
  !define mui_abortwarning

;Definimos el valor de la variable VERSION, en caso de no definirse en el script
;podria ser definida en el compilador
!define VERSION "0.1"

;--------------------------------
;Pages

  ;Mostramos la página de bienvenida 
  !insertmacro MUI_PAGE_WELCOME 
  ;página donde se selecciona el directorio donde instalar nuestra aplicacion 
  !insertmacro MUI_PAGE_DIRECTORY 
  ;página de instalación de ficheros 
  !insertmacro MUI_PAGE_INSTFILES 
  ;página final
  !insertmacro MUI_PAGE_FINISH

;páginas referentes al desinstalador
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

!insertmacro MUI_LANGUAGE "Spanish"

;;;;;;;;;;;;;;;;;;;;;;;;;
; Configuración General ;
;;;;;;;;;;;;;;;;;;;;;;;;;
;Nombre del instalador
OutFile Kerberus-client-${VERSION}.exe

;Aquí comprobamos que en la versión Inglesa se muestra correctamente el mensaje:
;Welcome to the $Name Setup Wizard
;Al tener reservado un espacio fijo para este mensaje, y al ser
;la frase en español mas larga:
; Bienvenido al Asistente de Instalación de Aplicación $Name
; no se ve el contenido de la variable $Name si el tamaño es muy grande
Name "Kerberus"
Caption "Kerberus ${VERSION} para Win32 Setup"

;Comprobacion de integridad del fichero activada
CRCCheck on
;Estilos visuales del XP activados
XPStyle on

Var PATH
;Indicamos cual será el directorio por defecto donde instalaremos nuestra
;aplicación, el usuario puede cambiar este valor en tiempo de ejecución.
InstallDir "$PROGRAMFILES\kerberus"
; check if the program has already been installed, if so, take this dir
; as install dir
InstallDirRegKey HKLM SOFTWARE\KERBERUS "Install_Dir"

;Mensaje que mostraremos para indicarle al usuario que seleccione un directorio
DirText "Elija un directorio donde instalar la aplicación:"
;Indicamos que cuando la instalación se complete no se cierre el instalador automáticamente
AutoCloseWindow false
;Mostramos todos los detalles del la instalación al usuario.
ShowInstDetails show
;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on
;Optimizamos nuestro paquete en tiempo de compilación, es altamente recomendable habilitar siempre esta opción
SetDatablockOptimize on
;Habilitamos la compresión de nuestro instalador
SetCompress auto
;Personalizamos el mensaje de desinstalación
UninstallText "Desinstalador de kerberus."

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta sección añadimos los ficheros que forman nuestra aplicación ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Section "Programa"
;;;StrCpy $PATH "Kerberus-client"
SetOutPath $INSTDIR\$PATH\client

;Incluimos todos los ficheros que componen nuestra aplicación
File   c:\Kerberus-client\*.*

SetOutPath $INSTDIR\$PATH\sync
File   c:\Kerberus-sync\*.*

;Hacemos que la instalación se realice para todos los usuarios del sistema
SetShellVarContext all

WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$PATH \
            "DisplayName" "Kerbers-client-${VERSION}"
WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$PATH \
            "UninstallString" '"$INSTDIR\uninstall.exe"'

WriteUninstaller "uninstall.exe"

WriteRegStr HKLM SOFTWARE\$PATH "InstallDir" $INSTDIR
       
WriteRegStr HKLM SOFTWARE\$PATH "Version" "${VERSION}"

WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Run \
            "Kerberus-client" "$INSTDIR\client\cliente.exe"

WriteRegStr HKLM \
            SOFTWARE\Microsoft\Windows\CurrentVersion\Run \
            "Kerberus-sync" "$INSTDIR\sync\sincronizadorCliente.exe"

SectionEnd



;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;

Section "Uninstall"
;;;        StrCpy $PATH "Kerberus-client"
        SetShellVarContext all
        RMDir /r $INSTDIR\$PATH
        RMDir /r $INSTDIR
        DeleteRegKey HKLM SOFTWARE\$PATH
        DeleteRegKey HKLM \
            Software\Microsoft\Windows\CurrentVersion\Uninstall\$PATH
SectionEnd
