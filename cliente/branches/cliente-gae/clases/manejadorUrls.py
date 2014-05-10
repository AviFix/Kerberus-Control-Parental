# -*- coding: utf-8 -*-

"""Modulo encargado de la modificacion de urls (safeSearch por ejemplo)"""
#Modulos externos
import re


#Excepciones
class manejadorUrlsError(Exception):

    def __init__(self):
        super(manejadorUrlsError, self).__init__()
        pass
#class nombre(manejadorUrlsError): pass


class ManejadorUrls:
    def __init__(self):
        self.buscadores = ['Google', 'Yahoo', 'Bing', 'Youtube']

    def esDominio(self, url):
        a = url.split('/')
        if len(a) < 5:
            if len(a) == 4:
                if a[3] == "":
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def agregarSafeSearch(self, url):
        """Reescribe la url para que soporte safeSearch"""
        buscador = self.identificarBuscador(url)
        if buscador == "Google":
            agregado = "&safe=active"
            if agregado not in url:
                url = url + agregado
            return url
        elif buscador == "Yahoo":
            agregado = "&vm=r"
            if agregado not in url:
                url = url + agregado
            return url
        elif buscador == "Bing":
            agregado = "&adlt=strict"
            if agregado not in url:
                url = url + agregado
            return url
        elif buscador == "Youtube":
            agregado = "&safe=active"
            if agregado not in url:
                url = url + agregado
            return url
        else:
            return url

    def soportaSafeSearch(self, url):
        """Verifica si la url es de un buscador que soporte safesearch"""
        pagina = self.identificarBuscador(url)
        return pagina in self.buscadores

    def identificarBuscador(self, url):
        """Identifica que navegador de los que soportan safeSearch es"""
        if re.match(
            "(?!^http:\/\/suggestqueries.).*google\..*/(custom|search|"
            "images)\?", url):
            return "Google"
        elif re.match(".*\.yahoo\..*/search", url):
            return "Yahoo"
        elif re.match(".*\.bing\..*/search", url):
            return "Bing"
        elif re.match("^http:\/\/www.youtube.com\/results\?", url):
            return "Youtube"
        else:
            return ""


def main():
    pass

# Importante: los módulos no deberían ejecutar
# código al ser importados
if __name__ == '__main__':
    main()