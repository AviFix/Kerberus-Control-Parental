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
            return True
        except:
            return False

    def estaSeteadoFirefox():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            firefoxSeteado = _winreg.QueryValueEx(key,'firefoxSet')[0]
            return firefoxSeteado
        except:
            return False

    def setearFirefox():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            _winreg.SetValueEx(key,"firefoxSet",0, REG_SZ, r"True")
            _winreg.CloseKey(key)

            key_path = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Mozilla\Mozilla Firefox')
            firefox_version =  _winreg.QueryValueEx(key_path,'CurrentVersion')[0]
            firefox_key_path=r'Software\Mozilla\Mozilla Firefox\%s\Main' % firefox_version
            Firefox_path_reg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, firefox_key_path)
            firefox_install_dir= _winreg.QueryValueEx(Firefox_path_reg,'Install Directory')[0]
            filename = "%s\\defaults\\pref\\all-kerberus.js" % firefox_install_dir
            file = open(filename, 'w')
            configuracion="pref(\"general.config.filename\", \"mozilla.cfg\");"
            file.write(configuracion)
            file.close()
            mozilla_config_file="\"%s\\mozilla.cfg\"" % path_common
            destino = "\"%s\\.\"" % firefox_install_dir
            comando = "copy %s %s /y" % (mozilla_config_file, destino)
            result = subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
        except:
            return "No se pudo setear firefox, a pesar de estar instalado"

    def estaSeteadoIE():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            ieSeted = _winreg.QueryValueEx(key,'IESet')[0]
            return ieSeted
        except:
            return False
            
    def setearIE():
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            _winreg.SetValueEx(key,"IESet",0, REG_SZ, r"True")
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'\Software\Microsoft\Internet Explorer\Main')
            _winreg.SetValueEx(key,"Start Page",0, REG_SZ, r"http://www.kerberus.com.ar/inicio.php")
            _winreg.CloseKey(key)
        except:
            print "Problema seteando IE"

