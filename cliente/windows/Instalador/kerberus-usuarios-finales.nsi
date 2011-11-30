;--------------------------------
;Include Modern UI

  !include "MUI.nsh"
;Seleccionamos el algoritmo de compresin utilizado para comprimir nuestra aplicacin
SetCompressor lzma

;--------------------------------
;Con esta opcin alertamos al usuario cuando pulsa el botn cancelar y le pedimos confirmacin para abortar
;la instalacin
;Esta macro debe colocarse en esta posicin del script sino no funcionara
  !define mui_abortwarning

;Definimos el valor de la variable VERSION, en caso de no definirse en el script
;podria ser definida en el compilador
!define VERSION "0.6"

;--------------------------------
;Pages

  ;Mostramos la pgina de bienvenida
  !insertmacro MUI_PAGE_WELCOME
  ;pgina donde se selecciona el directorio donde instalar nuestra aplicacion
  !insertmacro MUI_PAGE_DIRECTORY
  ;pgina de instalacin de ficheros
  !insertmacro MUI_PAGE_INSTFILES
  ;pgina final
  !insertmacro MUI_PAGE_FINISH

;pginas referentes al desinstalador
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

!insertmacro MUI_LANGUAGE "Spanish"

;;;;;;;;;;;;;;;;;;;;;;;;;
; Configuracin General ;
;;;;;;;;;;;;;;;;;;;;;;;;;
;Nombre del instalador
OutFile Kerberus-control-parental.exe

;Aqu comprobamos que en la versin Inglesa se muestra correctamente el mensaje:
;Welcome to the $Name Setup Wizard
;Al tener reservado un espacio fijo para este mensaje, y al ser
;la frase en espaol mas larga:
; Bienvenido al Asistente de Instalacin de Aplicacin $Name
; no se ve el contenido de la variable $Name si el tamao es muy grande
Name "Kerberus"
; Le dice que use privilegios de usuario nomas
RequestExecutionLevel user

Caption "Kerberus"

;Comprobacion de integridad del fichero activada
CRCCheck on
;Estilos visuales del XP activados
XPStyle on

;Indicamos cual ser el directorio por defecto donde instalaremos nuestra
;aplicacin, el usuario puede cambiar este valor en tiempo de ejecucin.
InstallDir "$APPDATA\Kerberus"
; check if the program has already been installed, if so, take this dir
; as install dir
InstallDirRegKey HKCU SOFTWARE\KERBERUS "Install_Dir"

;Mensaje que mostraremos para indicarle al usuario que seleccione un directorio
DirText "Elija un directorio donde instalar la aplicacin:"
;Indicamos que cuando la instalacin se complete no se cierre el instalador automticamente
AutoCloseWindow false
;Mostramos todos los detalles del la instalacin al usuario.
ShowInstDetails show
;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on
;Optimizamos nuestro paquete en tiempo de compilacin, es altamente recomendable habilitar siempre esta opcin
SetDatablockOptimize on
;Habilitamos la compresin de nuestro instalador
SetCompress auto
;Personalizamos el mensaje de desinstalacin
UninstallText "Desinstalar kerberus CPW."


# default section start
;section

    # call userInfo plugin to get user info.  The plugin puts the result in the stack
;    userInfo::getAccountType

    # pop the result from the stack into $0
;    pop $0

    # compare the result with the string "Admin" to see if the user is admin.
    # If match, jump 3 lines down.
;    strCmp $0 "Admin" +3

    # if there is not a match, print message and return
;    messageBox MB_OK "Debe tener Permisos de Administrador para instalar Kerberus: $0"
;    return

# default section end
;sectionEnd


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta seccin aadimos los ficheros que forman nuestra aplicacin ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Section "Programa"

CreateDirectory $INSTDIR

SetOutPath $INSTDIR
File ArchivosDefault\*.*
File libs\vcredist_x86.exe

SetOutPath $INSTDIR\checkNavs
File Navegadores\dist\*.*

;Incluimos todos los ficheros que componen nuestra aplicacin
SetOutPath $INSTDIR\client
File   kerberus-daemon\dist\*.*

SetOutPath $INSTDIR\sync
File   kerberus-sync\dist\*.*


ExecWait '"$INSTDIR\vcredist_x86.exe" /q'


; Doy permisos
AccessControl::GrantOnFile \
"$INSTDIR\kerberus" "(BU)" "GenericRead + GenericWrite + AddFile"
AccessControl::GrantOnFile \
"$INSTDIR\checkNavs" "(BU)" "GenericRead + GenericWrite + AddFile"

;Hacemos que la instalacin se realice para todos los usuarios del sistema
;SetShellVarContext all
;Hacemos que la instalacin se realice para el usuario que ejecuta el instalador
SetShellVarContext current

;;;;;;;;;;;;;;;;;;;;;;;
; Claves del registro ;
;;;;;;;;;;;;;;;;;;;;;;;
;HKCR - HKEY_CLASSES_ROOT
;HKLM - HKEY_LOCAL_MACHINE
;HKCU - HKEY_CURRENT_USER
;HKU - HKEY_USERS


WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"DisplayName" "Kerbers-client-${VERSION}"

WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"UninstallString" '"$INSTDIR\uninstall.exe"'

WriteUninstaller "uninstall.exe"

WriteRegStr HKCU "Software\Kerberus" "InstallDir" $INSTDIR

WriteRegStr HKCU "Software\Kerberus" "Version" "${VERSION}"

WriteRegStr HKCU "Software\Kerberus" "kerberus-common" "$INSTDIR"

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-client" "$INSTDIR\client\cliente.exe"

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-sync" "$INSTDIR\sync\sincronizadorCliente.exe"

WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
"checkNavs" "$INSTDIR\checkNavs\navegadores.exe"

;writeRegDword HKCU "SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\Internet Settings" \
;"ProxySettingsPerUser" 0

writeRegDWord HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"MigrateProxy" 1

writeRegDWord HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyEnable" 1

writeRegDWord HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyHttp1.1" 1

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyServer" "http://127.0.0.1:8080"


writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyOverride" "127.0.0.1,localhost"


; Make the directory "$INSTDIR\database" read write accessible by all users
;AccessControl::GrantOnFile \
;"$COMMONFILES\kerberus" "(BU)" "GenericRead + GenericWrite + AddFile"

;SimpleSC::InstallService "kerberus-daemon" "kerberus Daemon Service" "16" "2" "$INSTDIR\client\cliente.exe" "" "" ""
;SimpleSC::InstallService "kerberus-sync" "kerberus sync Service" "16" "2" "$INSTDIR\sync\sincronizadorCliente.exe" "" "" ""


ExecWait '"$INSTDIR\client\cliente.exe"'

MessageBox MB_YESNO|MB_ICONQUESTION "Se debe reiniciar para completar la instalacin. Desea reiniciar ahora?" IDNO +2
	reboot

SectionEnd



;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;

Section "Uninstall"
        ;SetShellVarContext all
        SetShellVarContext current
        ExecWait '"$INSTDIR\checkNavs\navegadores.exe" unset'
        DeleteRegKey HKCU "Software\Kerberus"
        DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Kerberus-client"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Kerberus-sync"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "MigrateProxy"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyEnable"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyHttp1.1"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyServer"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyOverride"
        RMDir /r /REBOOTOK $INSTDIR

;	writeRegDword HKCU "SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxySettingsPerUser" 1

;        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "MigrateProxy"
;        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyEnable"
;        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyHttp1.1"
;        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyServer"
;        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyOverride"

;SimpleSC::RemoveService "kerberus-daemon"
;SimpleSC::RemoveService "kerberus-sync"

MessageBox MB_YESNO|MB_ICONQUESTION "Se debe reiniciar para completar la desinstalacin. Desea reiniciar ahora?" IDNO +2
	reboot
SectionEnd

