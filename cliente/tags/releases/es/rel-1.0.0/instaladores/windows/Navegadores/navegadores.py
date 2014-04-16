#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, getopt, _winreg, subprocess, os, re

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

    def getFirefoxProfiles(self, user):
            profiles=[]
            profiles_path=os.environ['APPDATA']+"\\Mozilla\\Firefox\\Profiles"
            for entrada in os.listdir(profiles_path):
                objecto="%s\\%s" % (profiles_path,entrada,)
                if os.path.isdir(objecto):
                    profiles.append(objecto)
            return profiles

    def estaSeteadoFirefox(self, perfil):
            archivo_config="%s\\prefs.js" % perfil
            if os.path.isfile(archivo_config):
                archivo = open(archivo_config,'r')
                proxy_ip = 'user_pref(\"network.proxy.http\", \"127.0.0.1\");'
                proxy_port = 'user_pref(\"network.proxy.http_port\", 8080);'
                proxy_habilitado = 'user_pref(\"network.proxy.type\", 1);'
                ip_detectada = False
                puerto_detectado = False
                proxy_habilitado_detectado = False
                for linea in archivo.readlines():
                    print "linea: %s" % linea
                    if proxy_ip in linea:
                        ip_detectada = True
                    if proxy_port in linea:
                        puerto_detectado = True
                    if proxy_habilitado in linea:
                        proxy_habilitado_detectado = True
                if proxy_habilitado_detectado and puerto_detectado and ip_detectada:
                    print "Esta Seteado Firefox, perfil: %s" % perfil
                    return True
                else:
                    print "No esta Seteado Firefox, perfil: %s" % perfil
                    return False

    def setFirefox(self):
        if self.estaFirefoxInstalado():
            for perfil in self.getFirefoxProfiles(os.environ['USERNAME']):
                if not self.estaSeteadoFirefox(perfil):
                        print "seteando el perfil %s" % perfil
                        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
                        path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                        mozilla_config_file="%s\\user.js" % path_common_kerberus
                        destino = "%s\\user.js" % perfil
                        archivo_origen = open(mozilla_config_file, 'r')
                        archivo_destino = open(destino,'w')
                        for linea in archivo_origen.readlines():
                            archivo_destino.write(linea)
                        archivo_origen.close()
                        archivo_destino.close()
                        print "Se termino de setear firefox para el perfil %s" % perfil

    def unsetFirefox(self):
        if self.estaFirefoxInstalado():
            for perfil in self.getFirefoxProfiles(os.environ['USERNAME']):
                if self.estaSeteadoFirefox(perfil):
                    print "desseteando el perfil %s" % perfil
                    path_archivo = "%s\\prefs.js" % perfil
                    archivo = open(path_archivo,'r')
                    nuevo = []
                    for linea in archivo.readlines():
                        if "user_pref(\"network.proxy.type\", 1);" in linea:
                            nuevo.append("user_pref(\"network.proxy.type\", 0);\r\n")
                        else:
                            nuevo.append(linea)
                    archivo.close()
                    archivo = open(path_archivo,'w')
                    for linea in nuevo:
                        archivo.write(linea)
                    archivo.close()
                    archivo_user = "%s\\user.js" % perfil
                    if os.path.isfile(archivo_user):
                        os.remove(archivo_user)
                    print "Se termino de dessetear firefox para el perfil %s" % perfil

    def estaSeteadoIE(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main')
            proxy = _winreg.QueryValueEx(key,'ProxyServer')[0]
            if proxy == "127.0.0.1:8080":
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
                _winreg.SetValueEx(key,"Start Page",0,_winreg.REG_SZ, r'http://inicio.kerberus.com.ar')
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
                _winreg.SetValueEx(key,"ProxyServer",0,_winreg.REG_SZ,r'127.0.0.1:8080')
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



if __name__ == '__main__':
    navs=navegadores()
#    if navs.estaInstaladoKerberus():
#        navs.setNavegadores()
#    else:
#        navs.unsetNavegadores()
    if "unset" in sys.argv:
        navs.unsetNavegadores()
    else:
        navs.setNavegadores()
    sys.exit(0)
