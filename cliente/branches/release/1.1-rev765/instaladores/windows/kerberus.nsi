;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"
;Seleccionamos el algoritmo de compresión utilizado para comprimir nuestra aplicación
SetCompressor lzma

;--------------------------------
;Con esta opción alertamos al usuario cuando pulsa el botón cancelar y le pedimos confirmación para abortar
;la instalación
;Esta macro debe colocarse en esta posición del script sino no funcionara
  !define mui_abortwarning
  
; Iconos
  !define MUI_ICON "kerby2.ico"
  !define MUI_UNICON "kerby2.ico"


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
; Configuración General ;
;;;;;;;;;;;;;;;;;;;;;;;;;

;Nombre del instalador
OutFile Kerberus-multiuser-1.1.exe

;Aquí comprobamos que en la versión Inglesa se muestra correctamente el mensaje:
;Welcome to the $Name Setup Wizard
;Al tener reservado un espacio fijo para este mensaje, y al ser
;la frase en español mas larga:
; Bienvenido al Asistente de Instalación de Aplicación $Name
; no se ve el contenido de la variable $Name si el tamaño es muy grande
Name "Kerberus"
Caption "Kerberus"

;Comprobacion de integridad del fichero activada
CRCCheck on

;Estilos visuales del XP activados
XPStyle on

;Indicamos cual será el directorio por defecto donde instalaremos nuestra
;aplicación, el usuario puede cambiar este valor en tiempo de ejecución.
InstallDir "$PROGRAMFILES\Kerberus"

; check if the program has already been installed, if so, take this dir
; as install dir
InstallDirRegKey HKLM SOFTWARE\KERBERUS "Install_Dir"

;Mensaje que mostraremos para indicarle al usuario que seleccione un directorio
DirText "Elija un directorio donde instalar la aplicación:"

;Indicamos que cuando la instalación se complete no se cierre el instalador automáticamente
AutoCloseWindow false

;Mostramos todos los detalles del la instalación al usuario.
ShowInstDetails nevershow

;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on

;Optimizamos nuestro paquete en tiempo de compilación, es altamente recomendable habilitar siempre esta opción
SetDatablockOptimize on

;Habilitamos la compresión de nuestro instalador
SetCompress auto

;Personalizamos el mensaje de desinstalación
UninstallText "Desinstalar kerberus CPW."

# default section start
section
 
    # call userInfo plugin to get user info.  The plugin puts the result in the stack
    userInfo::getAccountType
   
    # pop the result from the stack into $0
    pop $0
 
    # compare the result with the string "Admin" to see if the user is admin.
    # If match, jump 3 lines down.
    strCmp $0 "Admin" +3
 
    # if there is not a match, print message and return
    abort "Debe tener Permisos de Administrador para instalar Kerberus: $0"
    return
    
    

# default section end
sectionEnd


##########################
# chequeo si esta instalado previamente
Function .onInit
  ;Verifico que sea administrador el usuario
  userInfo::getAccountType  
  pop $0
  strCmp $0 "Admin" +3
  MessageBox MB_OK|MB_ICONEXCLAMATION "Debe tener permisos de administrador para instalar Kerberus. Pruebe ejecutar el instalador desde una cuenta con privilegios de administrador, o utilizando la opción Ejecutar como..."
  Abort

  ;Definimos el valor de la variable VERSION, en caso de no definirse en el script
  ;podria ser definida en el compilador
  Var /GLOBAL VERSION
  StrCpy $VERSION "1.1"

  ReadRegStr $R0 HKLM \
  "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
  "UninstallString"
  StrCmp $R0 "" done

  MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
  "Kerberus ya esta instalado. $\n$\nDesea desinstalar la \
  version actualmente instalada, para luego instalar esta nueva?." \
  IDOK uninst
  Abort

;Run the uninstaller
uninst:
  ClearErrors
  ExecWait '$R0 _?=$INSTDIR\$VERSION' ;Do not copy the uninstaller to a temp file
  Abort
  IfErrors no_remove_uninstaller done
    ;You can either use Delete /REBOOTOK in the uninstaller or add some code
    ;here to remove the uninstaller. Use a registry key to check
    ;whether the user has chosen to uninstall. If you are using an uninstaller
    ;components page, make sure all sections are uninstalled.
  no_remove_uninstaller:
  Abort
done:

FunctionEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta sección añadimos los ficheros que forman nuestra aplicación ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Section "Programa"

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

SetOutPath $SYSDIR
File ArchivosDefault\klsp.dll

; Instalo .Net Framework
;DetailPrint "Instalando .NET Framework"
;ExecWait '"$INSTDIR\$VERSION\dotNetFx40_Full_x86_x64.exe" /q'
; Instalo visual c++ 2010 redistributable
;DetailPrint "Instalando VcRedist"
;ExecWait '"$INSTDIR\$VERSION\vcredist_x86.exe" /q'

; Doy permisos
AccessControl::GrantOnFile \
"$INSTDIR\$VERSION" "(BU)" "GenericRead + GenericWrite + AddFile"

;Hacemos que la instalacin se realice para todos los usuarios del sistema
SetShellVarContext all

;;;;;;;;;;;;;;;;;;;;;;;
; Claves del registro ;
;;;;;;;;;;;;;;;;;;;;;;;
;HKCR - HKEY_CLASSES_ROOT
;HKLM - HKEY_LOCAL_MACHINE
;HKCU - HKEY_CURRENT_USER
;HKU - HKEY_USERS


WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"DisplayName" "Kerberus-control-parental"

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus" \
"UninstallString" '"$INSTDIR\$VERSION\uninstall.exe"'

WriteUninstaller $INSTDIR\$VERSION\kcpwu.dat

WriteRegStr HKLM "Software\Kerberus" "InstallDir" $INSTDIR\$VERSION

WriteRegStr HKLM "Software\Kerberus" "Version" "$VERSION"

WriteRegStr HKLM "Software\Kerberus" "kerberus-common" "$INSTDIR\$VERSION"

writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-client" "$INSTDIR\$VERSION\client\kerberus.exe"

writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" \
"Kerberus-sync" "$INSTDIR\$VERSION\sync\kerberus-sync.exe"

WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" \
"checkNavs" "$INSTDIR\$VERSION\checkNavs\kerberus-nav.exe"

;writeRegDWord HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
;"MigrateProxy" 1

;writeRegDWord HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
;"ProxyEnable" 1

;writeRegDWord HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
;"ProxyHttp1.1" 1

;writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
;"ProxyServer" "127.0.0.1:4200"

;writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" \
;"ProxyOverride" "127.0.0.1,localhost"

; Seteando google chrome, sacado de http://www.chromium.org/administrators/policy-list-3
writeRegStr HKLM "Software\Policies\Google\Chrome" "HomepageLocation" "http://inicio.kerberus.com.ar"
writeRegStr HKLM "Software\Policies\Google\Chrome" "ProxyMode" "system"
;writeRegStr HKLM "Software\Policies\Google\Chrome" "DefaultSearchProviderSearchURL" "http://inicio.kerberus.com.ar/buscador.php?cx=partner-pub-5233852436544664%3A0998292818&ie=UTF-8&sa=Search&q={searchTerms}"
writeRegDWord HKLM "Software\Policies\Google\Chrome" "HomepageIsNewTabPage" 0


ExecWait '"$INSTDIR\$VERSION\sync\kerberus-sync.exe"'
;ExecWait '"$INSTDIR\$VERSION\instlsp.exe" -i -a -n KLSP -d "$INSTDIR\$VERSION\klsp.dll"'
nsExec::ExecToStack /OEM "$INSTDIR\$VERSION\inst_lsp.exe"

MessageBox MB_YESNO|MB_ICONQUESTION "Es necesario reiniciar para completar la instalacion. Desea reiniciar ahora?" IDNO +2
	reboot

SectionEnd


;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;
!include "nsProcess.nsh"

Function un.onInit

  ;Verifico que sea administrador el usuario
  userInfo::getAccountType  
  pop $0
  strCmp $0 "Admin" +3
  MessageBox MB_OK|MB_ICONEXCLAMATION "Debe tener permisos de administrador para desinstalar Kerberus. Pruebe desinstalarlo desde una cuenta con privilegios de administrador."
  Abort
 
  # Me fijo si esta firefox corriendo
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
        SetShellVarContext all
        ;DeleteRegKey HKLM "Software\Kerberus"
        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Kerberus"
        DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "Kerberus-client"
        DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "Kerberus-sync"
        ;DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "checkNavs"
        ;DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "MigrateProxy"
        ;DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyEnable"
        ;DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyHttp1.1"
        ;DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyServer"
        ;DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Internet Settings" "ProxyOverride"
        DeleteRegValue HKLM "Software\Policies\Google\Chrome" "HomepageLocation"
        DeleteRegValue HKLM "Software\Policies\Google\Chrome" "system"
        ;DeleteRegValue HKLM "Software\Policies\Google\Chrome" "DefaultSearchProviderSearchURL"
        DeleteRegValue HKLM "Software\Policies\Google\Chrome" "HomepageIsNewTabPage"

        ExecWait '"$INSTDIR\$VERSION\checkNavs\navegadores.exe" unset'
        ;ExecWait '"$INSTDIR\$VERSION\instlsp.exe" -f '
        nsExec::ExecToStack /OEM "$INSTDIR\$VERSION\inst_lsp.exe"
        ; No se borra checknavs, porque sino no se desconfiguran los navegadores
        ;RMDir /r /REBOOTOK $INSTDIR\$VERSION
        ;RMDir /r /REBOOTOK $INSTDIR\$VERSION\client
        ;RMDir /r /REBOOTOK $INSTDIR\$VERSION\sync
        ;RMDir /r /REBOOTOK $INSTDIR\$VERSION\templates
        ;RMDir /REBOOTOK $INSTDIR\$VERSION\*.*

MessageBox MB_YESNO|MB_ICONQUESTION "Es necesario reiniciar para completar la desinstalacion. Desea reiniciar ahora?" IDNO +2
	reboot
SectionEnd

