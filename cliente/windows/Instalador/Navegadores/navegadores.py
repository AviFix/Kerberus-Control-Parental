#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, _winreg, subprocess

class navegadores:

    def estaInstaladoKerberus(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
            kerberus_version =  _winreg.QueryValueEx(key,'Version')[0]
            if kerberus_version:
                print "Kerberus instalado, configurando navegadores"
                return True
            else:
                print "Kerberus no instalado, desconfigurando navegadores"
                return False
        except:
            print "Kerberus no instalado, desconfigurando navegadores"
            return False

    def setNavegadores(self):
        self.setFirefox()
        self.setIE()

    def unsetNavegadores(self):
        self.unsetFirefox()
        self.unsetIE()

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
            filename = "%s\\defaults\\pref\\all-kerberus.js" % self.firefoxInstallDir
            file = open(filename, 'r')
            if file:
                print "Esta seteado Firefox"
                file.close()
                return True
            else:
                print "No esta seteado Firefox"
                return False
        except:
            print "No esta seteado Firefox"
            return False

    def setFirefox(self):
        if self.estaFirefoxInstalado():
            if not self.estaSeteadoFirefox():
                    print "seteando firefox"
                    filename = "%s\\defaults\\pref\\all-kerberus.js" % self.firefoxInstallDir
                    file = open(filename, 'w')
                    configuracion="pref(\"general.config.filename\", \"mozilla.cfg\");"
                    file.write(configuracion)
                    file.close()
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
                    path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                    mozilla_config_file="\"%s\\mozilla.cfg\"" % path_common_kerberus
                    destino = "\"%s\\mozilla.cfg\"" % self.firefoxInstallDir
                    comando = "copy %s %s /y" % (mozilla_config_file, destino)
                    result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                    print "Se termino de setear firefox"

    def unsetFirefox(self):
        if self.estaFirefoxInstalado():
            if self.estaSeteadoFirefox():
                #try:
                    print "Deseteando firefox"
                    preference_file = "%s\\defaults\\pref\\all-kerberus.js" % self.firefoxInstallDir
                    mozilla_cfg = "\"%s\\mozilla.cfg\"" % self.firefoxInstallDir
                    comando = "del \"%s\" %s /F" % (preference_file,mozilla_cfg)
                    print comando
                    result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                    print "Fin del desseteado de firefox"
                #except:
                #    return "No se pudo dessetear firefox, a pesar de estar instalado"

    def estaSeteadoIE(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main')
            proxy = _winreg.QueryValueEx(key,'ProxyServer')[0]
            if proxy == "http://127.0.0.1:8080":
                print "Esta seteado Internet Explorer"
                return True
            else:
                print "No esta seteado Internet Explorer"
                return False
        except:
            print "no esta seteado IE"
            return False

    def setIE(self):
        if not self.estaSeteadoIE():
            #try:
                print "Seteando IE"
                # Seteando pagina de inicio
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"Start Page",0,_winreg.REG_SZ, r'http://www.kerberus.com.ar/inicio')
                _winreg.CloseKey(key)

                # Seteando proxy
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"MigrateProxy",0,_winreg.REG_DWORD, 1)
                _winreg.CloseKey(key)

                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"ProxyEnable",0,_winreg.REG_DWORD, 1)
                _winreg.CloseKey(key)

                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"ProxyHttp1.1",0,_winreg.REG_DWORD, 1)
                _winreg.CloseKey(key)

                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"ProxyServer",0,_winreg.REG_SZ,r'http://127.0.0.1:8080')
                _winreg.CloseKey(key)

                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
                _winreg.SetValueEx(key,"ProxyOverride",0,_winreg.REG_SZ,r'<local>')
                _winreg.CloseKey(key)

                print "Fin del seteo de IE"

            #except:
            #    print "Problema seteando IE"

    def unsetIE(self):
        if self.estaSeteadoIE():
        #try:
            print "Desseteando IE"
            # Saco la pagina de inicio
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main',0,_winreg.KEY_SET_VALUE)
            _winreg.SetValueEx(key,"Start Page",0,_winreg.REG_SZ, r'http://www.google.com.ar')
            _winreg.CloseKey(key)

            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
            _winreg.DeleteValue(key,r'MigrateProxy')
            _winreg.CloseKey(key)

            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
            _winreg.DeleteValue(key,r'ProxyEnable')
            _winreg.CloseKey(key)

            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
            _winreg.DeleteValue(key,r'ProxyHttp1.1')
            _winreg.CloseKey(key)

            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
            _winreg.DeleteValue(key,r'ProxyServer')
            _winreg.CloseKey(key)

            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0,_winreg.KEY_SET_VALUE)
            _winreg.DeleteValue(key,r'ProxyOverride')
            _winreg.CloseKey(key)

            print "Fin del desseteado de IE"
        #except:
        #    print "Problema Desseteando IE"

    def self.getUserDataDir(self):
        return environ['APPDATA']



if __name__ == '__main__':
    navs=navegadores()
    if navs.estaInstaladoKerberus():
        navs.setNavegadores()
    else:
        navs.unsetNavegadores()
    sys.exit(0)
