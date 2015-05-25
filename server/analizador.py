# -*- coding: utf-8 -*-

from server import *

CANTIDAD_PARA_IMPORTAR=50

class Analizador():
    def __init__(self):
        self.dominios_permitidos_a_agregar=[]
    
    def relevarDominiosAceptados(self):
        urls=Urls()
        urls.cargarUrls()
        urls.cargarDominios()
        dominios=[]
        dominios_unicos=[]
        dominios_unicos_aceptados_count={}        
        for url in urls.cache_urls_aceptadas:
            if url[0:7] == "http://":
                dominio=url.split("/")[2]
            else:
                dominio=url.split(":")[0]
            dominios.append(dominio)
            if dominio not in dominios_unicos and dominio not in urls.dominios_permitidos:
                dominios_unicos.append(dominio)
        for dominio in dominios_unicos:
            dominios_unicos_aceptados_count[dominio]=dominios.count(dominio)
        for dominio, cantidad in dominios_unicos_aceptados_count.items():
            if dominio not in urls.cache_urls_denegadas and cantidad >= CANTIDAD_PARA_IMPORTAR:
                self.dominios_permitidos_a_agregar.append(dominio)
    
    def showDominiosAceptados(self):
        return self.dominios_permitidos_a_agregar
    
    def persitirDominiosAceptados(self):
        pass
        
    def getListasGrises(self):
        pass
        
analizador=Analizador()
analizador.relevarDominiosAceptados()
print analizador.showDominiosAceptados()
    
