#!/usr/bin/python
# -*- coding: utf-8 -*- 

class navegadores:

    def estaFirefoxInstalado():
        try:
            key_path = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Mozilla\Mozilla Firefox')
            firefox_version =  _winreg.QueryValueEx(key_path,'CurrentVersion')[0]
            firefox_key_path=r'Software\Mozilla\Mozilla Firefox\%s\Main' % firefox_version
            Firefox_path_reg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, firefox_key_path)
            firefox_install_dir= _winreg.QueryValueEx(Firefox_path_reg,'Install Directory')[0]
            if firefox_install_dir:
                self.firefoxInstallDir=firefox_install_dir
                return True
            else:
                return False
        except:
            return False

    def estaSeteadoFirefox():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            firefoxSeteado = _winreg.QueryValueEx(key,'firefoxSeteado')[0]
            return firefoxSeteado
        except:
            return False

    def setFirefox():
        if self.estaFirefoxInstalado():
            if not self.estaSeteadoFirefox():
                self.setearFirefox()
                try:
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                    _winreg.SetValueEx(key,"firefoxSet",0, REG_SZ, r"True")
                    _winreg.CloseKey(key)
                    filename = "%s\\defaults\\pref\\all-kerberus.js" % self.firefoxInstallDir
                    file = open(filename, 'w')
                    configuracion="pref(\"general.config.filename\", \"mozilla.cfg\");"
                    file.write(configuracion)
                    file.close()
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                    path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                    mozilla_config_file="\"%s\\mozilla.cfg\"" % path_common_kerberus
                    destino = "\"%s\\.\"" % self.firefoxInstallDir
                    comando = "copy %s %s /y" % (mozilla_config_file, destino)
                    result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                except:
                    return "No se pudo setear firefox, a pesar de estar instalado"

    def unsetFirefox():
        if self.estaSeteadoFirefox():
            try:
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                _winreg.deleteValue(key,"firefoxSet")
                _winreg.CloseKey(key)
                conf_file = "%s\\defaults\\pref\\all-kerberus.js" % self.firefoxInstallDir
                moz_conf="%s\\mozilla.cfg" % self.firefoxInstallDir
                comando = "del %s %s/y" % (filename,  moz_conf)
                result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
            except:
                return "No se pudo dessetear firefox, a pesar de estar instalado"

    def estaSeteadoIE():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            ieSeteado = _winreg.QueryValueEx(key,'IESeteado')[0]
            return ieSeteado
        except:
            return False

    def setIE():
        if not self.estaSeteadoIE():
            try:
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                _winreg.SetValueEx(key,"IESeteado",0, REG_SZ, r"True")
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'\Software\Microsoft\Internet Explorer\Main')
                _winreg.SetValueEx(key,"Start Page",0, REG_SZ, r"http://www.kerberus.com.ar/inicio.php")
                _winreg.CloseKey(key)
            except:
                print "Problema seteando IE"

    def unsetIE():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            _winreg.DeleteValue(key,"IESeteado")
            _winreg.CloseKey(key)            
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'\Software\Microsoft\Internet Explorer\Main')
            _winreg.SetValueEx(key,"Start Page",0, REG_SZ, r"http://www.google.com.ar")
            _winreg.CloseKey(key)
        except:
            print "Problema Desseteando IE"
            
            
if __name__ == '__main__':
    navs=navegadores()
    try:                                
        accion=sys.argv[1]
        if accion== "set":
            navs.setFirefox()
            navs.setIE()
        elif accion == "unset":
            navs.unsetFirefox()
            navs.unsetIE()
        else:
            "Parametro incorrecto, use set o unset"
    except getopt.GetoptError: 
        print "Accion incorrecta, introduzca instalar o desinstalar"
        sys.exit(2)                     
    sys.exit(0)
