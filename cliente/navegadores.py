#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, _winreg, subprocess

class navegadores:
    def estaFirefoxInstalado(self):
        try:
            key_path = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Mozilla\Mozilla Firefox')
            firefox_version =  _winreg.QueryValueEx(key_path,'CurrentVersion')[0]
            firefox_key_path=r'Software\Mozilla\Mozilla Firefox\%s\Main' % firefox_version
            Firefox_path_reg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, firefox_key_path)
            firefox_install_dir= _winreg.QueryValueEx(Firefox_path_reg,'Install Directory')[0]
            if firefox_install_dir:
                self.firefoxInstallDir=firefox_install_dir
                print "Esta instalado firefox"
                return True
            else:
                print "No esta instalado firefox"
                return False
            
        except:
            print "Problemas verificando si esta instalado firefox"
            return False

    def estaSeteadoFirefox(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            firefox_seteado = _winreg.QueryValueEx(key,'FirefoxSeteado')[0]
            if firefox_seteado:
                print "Estaba seteado Firefox"
            else:
                print "No estaba seteado Firefox"
            return key      
        except:
            print "No estaba seteado Firefox"
            return False

    def setFirefox(self):
        if self.estaFirefoxInstalado():
            if not self.estaSeteadoFirefox():
                    print "seteando firefox"
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Kerberus',0,_winreg.KEY_SET_VALUE)
                    _winreg.SetValueEx(key,"FirefoxSeteado", 0, _winreg.REG_SZ, r"True")
                    _winreg.CloseKey(key)
                    filename = "%s\\defaults\\pref\\all-kerberus.js" % self.firefoxInstallDir
                    file = open(filename, 'w')
                    configuracion="pref(\"general.config.filename\", \"mozilla-k.cfg\");"
                    file.write(configuracion)
                    file.close()
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                    path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                    mozilla_config_file="\"%s\\mozilla-k.cfg\"" % path_common_kerberus
                    destino = "\"%s\\mozilla-k.cfg\"" % self.firefoxInstallDir
                    comando = "copy %s %s /y" % (mozilla_config_file, destino)
                    result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                    print "Se termino de setear firefox"

    def unsetFirefox(self):
        if self.estaFirefoxInstalado():
            if self.estaSeteadoFirefox():
                #try:
                    print "Deseteando firefox"
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus',0,_winreg.KEY_SET_VALUE)
                    _winreg.DeleteValue(key,r'firefoxSeteado')
                    _winreg.CloseKey(key)
                    moz_conf="%s\\mozilla-k.cfg" % self.firefoxInstallDir
                    comando = "del \"%s\" /F" % (moz_conf)
                    #print comando
                    result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                    path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                    mozilla_config_file_uninstall="\"%s\\mozilla-uninstall.cfg\"" % path_common_kerberus
                    destino = "\"%s\\mozilla-k.cfg\"" % self.firefoxInstallDir
                    comando = "copy %s %s /y" % (mozilla_config_file, destino)
                    result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                    
                    print "Fin del desseteado de firefox"
                #except:
                #    return "No se pudo dessetear firefox, a pesar de estar instalado"

    def estaSeteadoIE(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            ie_seteado = _winreg.QueryValueEx(key,'IESeteado')[0]
            if ie_seteado:
                print "Estaba seteado Internet Explorer"
                return True
            else:
                print "No estaba seteado Internet Explorer"
                return False
        except:
            "Error verificando si estaba seteado IE"
            return False

    def setIE(self):
        if not self.estaSeteadoIE():
            #try:
                print "Seteando IE"
                # Seteando como seteado a IE
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"IESeteado",0, _winreg.REG_SZ, r"True")
                _winreg.CloseKey(key)
                # Seteando Start Page
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"Start Page",0,_winreg.REG_SZ, r'http://www.kerberus.com.ar/inicio.php')
                _winreg.CloseKey(key)
                # Seteando Search Page
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"Search Page",0,_winreg.REG_SZ, r'http://www.kerberus.com.ar/inicio.php')
                _winreg.CloseKey(key)
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"Start Page",0,_winreg.REG_SZ, r'http://www.kerberus.com.ar/inicio.php')
                _winreg.CloseKey(key)
                # Seteando Search Page
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"Search Page",0,_winreg.REG_SZ, r'http://www.kerberus.com.ar/inicio.php')
                _winreg.CloseKey(key)                
                print "Fin del seteo de IE"
            #except:
            #    print "Problema seteando IE"

    def unsetIE(self):
        if self.estaSeteadoIE():       
        #try:
            print "Desseteando IE"
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus',0,_winreg.KEY_SET_VALUE)
            _winreg.DeleteValue(key,r'IESeteado')
            _winreg.CloseKey(key)            
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
            _winreg.SetValueEx(key,"Start Page",0, _winreg.REG_SZ, r"http://www.google.com.ar")
            _winreg.CloseKey(key)
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
            _winreg.SetValueEx(key,"Search Page",0, _winreg.REG_SZ, r"http://www.google.com.ar")
            _winreg.CloseKey(key)
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
            _winreg.SetValueEx(key,"Start Page",0, _winreg.REG_SZ, r"http://www.google.com.ar")
            _winreg.CloseKey(key)
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
            _winreg.SetValueEx(key,"Search Page",0, _winreg.REG_SZ, r"http://www.google.com.ar")
            _winreg.CloseKey(key)            
            
            print "Fin del desseteado de IE"
        #except:
        #    print "Problema Desseteando IE"
            
            
if __name__ == '__main__':
    navs=navegadores()
    try:
        accion=sys.argv[1]
    except:
        print "Parametro incorrecto, use set o unset"
        sys.exit(2)
        
    if accion== "set":
        navs.setFirefox()
        navs.setIE()
    elif accion == "unset":
        navs.unsetFirefox()
        navs.unsetIE()
    else:
        print "Parametro incorrecto, use set o unset"
        sys.exit(2)
    sys.exit(0)
