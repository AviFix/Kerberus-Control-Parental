;--------------------------------
;Include Modern UI
!include "nsProcess.nsh"
!include "MUI.nsh"

;Seleccionamos el algoritmo de compresin utilizado para comprimir nuestra aplicacin
SetCompressor lzma

;--------------------------------
;Con esta opcin alertamos al usuario cuando pulsa el botn cancelar y le pedimos confirmacin para abortar
;la instalacin
;Esta macro debe colocarse en esta posicin del script sino no funcionara
  !define mui_abortwarning




;--------------------------------
;Pages

  ;Mostramos la pgina de bienvenida
  !insertmacro MUI_PAGE_WELCOME
  ; License page
  !insertmacro MUI_PAGE_LICENSE "ArchivosDefault/licencia.txt"   ; text file with license terms
  ;pgina donde se selecciona el directorio donde instalar nuestra aplicacion
  !insertmacro MUI_PAGE_DIRECTORY
  ;pgina de instalacin de ficheros
  !insertmacro MUI_PAGE_INSTFILES
  ;pgina final
  !insertmacro MUI_PAGE_FINISH
;pginas referentes al desinstalador
!include MUI2.nsh
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
OutFile update.exe

;Aqu comprobamos que en la versin Inglesa se muestra correctamente el mensaje:
;Welcome to the $Name Setup Wizard
;Al tener reservado un espacio fijo para este mensaje, y al ser
;la frase en espaol mas larga:
; Bienvenido al Asistente de Instalacin de Aplicacin $Name
; no se ve el contenido de la variable $Name si el tamao es muy grande
Name "Kerberus"
; Le dice que use privilegios de usuario nomas
RequestExecutionLevel user

; Esto hace que sea en modo silenciosa la instalación.s
SilentInstall silent


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
DirText "Elija un directorio donde instalar la aplicacion:"
;Indicamos que cuando la instalacin se complete no se cierre el instalador automticamente
AutoCloseWindow false
;Mostramos todos los detalles del la instalacin al usuario.
ShowInstDetails nevershow
;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on
;Optimizamos nuestro paquete en tiempo de compilacin, es altamente recomendable habilitar siempre esta opcin
SetDatablockOptimize on
;Habilitamos la compresin de nuestro instalador
SetCompress auto
;Personalizamos el mensaje de desinstalacin
UninstallText "Desinstalar kerberus CPW."


##########################
# chequeo si esta instalado previamente
Function .onInit

  ;Definimos el valor de la variable VERSION, en caso de no definirse en el script
  ;podria ser definida en el compilador
  Var /GLOBAL VERSION
  StrCpy $VERSION "1.1"
FunctionEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta seccin aadimos los ficheros que forman nuestra aplicacin ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Section "Programa"

; Copio el installdir anterior
Var /GLOBAL ANTERIOR_INSTALLDIR
ReadRegStr $ANTERIOR_INSTALLDIR HKCU "Software\Kerberus" "InstallDir"


CreateDirectory $INSTDIR\$VERSION

SetOutPath $INSTDIR\$VERSION
File ArchivosDefault\*.*

SetOutPath $INSTDIR\$VERSION\checkNavs
File Navegadores\dist\navegadores\*.*

;Incluimos todos los ficheros que componen nuestra aplicacin
SetOutPath $INSTDIR\$VERSION\client
File   kerberus-daemon\dist\cliente\*.*

SetOutPath $INSTDIR\$VERSION\sync
File   kerberus-sync\dist\sincronizadorCliente\*.*

SetOutPath $INSTDIR\$VERSION
File   desinstalador\dist\uninstall\*.*

SetOutPath $INSTDIR\$VERSION\templates
File   ..\..\templates\*.*

SetOutPath $INSTDIR\$VERSION	
File   migrador\dist\migrador\*.*

; Doy permisos
AccessControl::GrantOnFile \
"$INSTDIR\$VERSION\kerberus" "(BU)" "GenericRead + GenericWrite + AddFile"
AccessControl::GrantOnFile \
"$INSTDIR\$VERSION\checkNavs" "(BU)" "GenericRead + GenericWrite + AddFile"

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
"DisplayName" "Kerberus-control-parental"

WriteUninstaller $INSTDIR\$VERSION\kcpwu.dat


writeRegDWord HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"MigrateProxy" 1

writeRegDWord HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyEnable" 1

writeRegDWord HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyHttp1.1" 1

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyServer" "127.0.0.1:8080"

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
"ProxyOverride" "127.0.0.1,localhost"

; Seteando google chrome, sacado de http://www.chromium.org/administrators/policy-list-3
writeRegStr HKCU "Software\Policies\Google\Chrome" "HomepageLocation" "http://inicio.kerberus.com.ar"
writeRegStr HKCU "Software\Policies\Google\Chrome" "ProxyMode" "system"
writeRegStr HKCU "Software\Policies\Google\Chrome" "DefaultSearchProviderSearchURL" "http://inicio.kerberus.com.ar/buscador.php?cx=partner-pub-5233852436544664%3A0998292818&ie=UTF-8&sa=Search&q={searchTerms}"
writeRegDWord HKCU "Software\Policies\Google\Chrome" "HomepageIsNewTabPage" 0


CopyFiles /SILENT $ANTERIOR_INSTALLDIR\kerberus.db $INSTDIR\$VERSION\kerberus.db

ExecWait '"$INSTDIR\$VERSION\migrador.exe"' $R0
StrCmp $R0 0 +3 0
MessageBox MB_OK|MB_ICONEXCLAMATION "Hubo un error en el cliente de kerberus. Por favor reinicie su PC."
Abort

; Modifico las variables, porque en teoria ya se copio todo y se hizo ok la migracion

WriteRegStr HKCU "Software\Kerberus" "InstallDir" $INSTDIR\$VERSION

WriteRegStr HKCU "Software\Kerberus" "Version" "$VERSION"

WriteRegStr HKCU "Software\Kerberus" "kerberus-common" "$INSTDIR\$VERSION"

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-client" "$INSTDIR\$VERSION\client\cliente.exe"

writeRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-sync" "$INSTDIR\$VERSION\sync\sincronizadorCliente.exe"

WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
"checkNavs" "$INSTDIR\$VERSION\checkNavs\navegadores.exe"

WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"UninstallString" '"$INSTDIR\$VERSION\uninstall.exe"'

; cierro el cliente y el sincronizador de la version anterior y lanzo los nuevos

${nsProcess::KillProcess} "cliente.exe" $R0
StrCmp $R0 0 +3 0
MessageBox MB_OK|MB_ICONEXCLAMATION "Hubo un error en el cliente de kerberus. Por favor reinicie su PC."
Abort
Exec '"$INSTDIR\$VERSION\client\cliente.exe"'

${nsProcess::KillProcess} "sincronizadorCliente.exe" $R0
StrCmp $R0 0 +3 0
MessageBox MB_OK|MB_ICONEXCLAMATION "Hubo un error en el cliente de kerberus. Por favor reinicie su PC."
Abort
Exec '"$INSTDIR\$VERSION\sync\sincronizadorCliente.exe"'

SectionEnd



;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;




Function un.onInit

  ${nsProcess::FindProcess} "firefox.exe" $R0
  StrCmp $R0 0 firefoxRunning done

firefoxRunning:
  MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
  "Se esta ejecuntando Mozilla Firefox. Es necesario cerrar este programa antes de continuar. Desea cerrarlo y continuar?" \
  IDOK cerrarFirefox
  Abort

cerrarFirefox:
  ${nsProcess::KillProcess} "firefox.exe" $R0
  StrCmp $R0 0 done error

error:
  MessageBox MB_OK|MB_ICONEXCLAMATION \
  "Hubo un error al tratar de cerrar Mozilla Firefox. Es necesario que cierre este programa usted mismo, y vuelva a ejecutar el desinstalador." \
  IDOK salir

salir:
  Abort


done:

FunctionEnd

Section "Uninstall"
        ;SetShellVarContext all
        SetShellVarContext current
        ExecWait '"$INSTDIR\$VERSION\checkNavs\navegadores.exe" unset'
        DeleteRegKey HKCU "Software\Kerberus"
        DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Kerberus-client"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Kerberus-sync"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "checkNavs"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "MigrateProxy"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyEnable"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyHttp1.1"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyServer"
        DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyOverride"
        DeleteRegValue HKCU "Software\Policies\Google\Chrome" "HomepageLocation"
        DeleteRegValue HKCU "Software\Policies\Google\Chrome" "system"
        DeleteRegValue HKCU "Software\Policies\Google\Chrome" "DefaultSearchProviderSearchURL"
        DeleteRegValue HKCU "Software\Policies\Google\Chrome" "HomepageIsNewTabPage"
        RMDir /r /REBOOTOK $INSTDIR\$VERSION

MessageBox MB_YESNO|MB_ICONQUESTION "Es necesario reiniciar para completar la desinstalacion. Desea reiniciar ahora?" IDNO +2
	reboot
SectionEnd

