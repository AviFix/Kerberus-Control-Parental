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
                regex_ip = '.*network.proxy.http..*127.0.0.1.*'
                regex_port = '.*network.proxy.http_port..*8080.*'
                ip_encontrada = False
                port_encontrado = False
                for linea in archivo.readlines():
                    if re.match(regex_ip, linea):
                        ip_encontrada=True
                    if re.match(regex_port, linea):
                        port_encontrado=True
                if ip_encontrada and port_encontrado:
                    return True
            return False

    def setFirefox(self):
        if self.estaFirefoxInstalado():
            for perfil in self.getFirefoxProfiles(os.environ['USERNAME']):
                if not self.estaSeteadoFirefox(perfil):
                        print "seteando el perfil %s" % perfil
                        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
                        path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                        mozilla_config_file="\"%s\\user.js\"" % path_common_kerberus
                        destino = "\"%s\\user.js\"" % perfil
                        comando = "copy %s %s /y" % (mozilla_config_file, destino)
                        print "El comando es: %s" % comando
                        result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                        print "Se termino de setear firefox para el perfil %s" % perfil

    def unsetFirefox(self):
        if self.estaFirefoxInstalado():
            for perfil in self.getFirefoxProfiles(os.environ['USERNAME']):
                if self.estaSeteadoFirefox(perfil):
                        print "desseteando el perfil %s" % perfil
                        # busco el seteo de proxy en pref.js
                        archivo_config="%s\\prefs.js" % perfil
                        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
                        path_common_kerberus = _winreg.QueryValueEx(key,'kerberus-common')[0]
                        mozilla_config_file= "%s\\user.js" % path_common_kerberus
                        archivo_user = open(mozilla_config_file,'r').read()
                        lineas_a_borrar = []
                        print "cargando lineas a borrar"
                        for linea in archivo_user.split('\n'):
                            lineas_a_borrar.append(linea)
                        lineas_a_borrar = lineas_a_borrar[0:-1]
                        data = open(archivo_config,'r').read()
                        print "data antes: %s" % data
                        for linea in lineas_a_borrar:
                            data=re.sub(re.escape(linea),'', data)
                        archivo = open(archivo_config,'w')
                        print "data despues: %s" % data
                        archivo.write( data )
                        archivo.close()
                        destino = "\"%s\\user.js\"" % perfil
                        comando = "del %s" % (destino)
                        result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
                        print "Se termino de dessetear firefox para el perfil %s" % perfil
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
