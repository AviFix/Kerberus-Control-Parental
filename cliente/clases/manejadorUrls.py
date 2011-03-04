import re

class ManejadorUrls:
    def __init__(self):
        self.buscadores=['Google', 'Yahoo', 'Bing', 'Youtube']
        
    def agregarSafeSearch(self, url):
            buscador=self.identificarBuscador(url)
            if buscador == "Google":
                agregado="&safe=active"
                if agregado not in url:                
                    url=url+agregado
                return url
            elif buscador == "Yahoo":
                agregado="&vm=r"
                if agregado not in url:
                    url=url+agregado
                return url
            elif buscador == "Bing":
                agregado="&adlt=strict"
                if agregado not in url:
                    url=url+agregado
                return url                
            elif buscador == "Youtube":
                agregado="&safe=active"
                if agregado not in url:
                    url=url+agregado
                return url                      
            else:                
                return url

    def soportaSafeSearch(self, url):
        pagina=self.identificarBuscador(url)
        return pagina in self.buscadores
        
    def identificarBuscador(self, url):
        if re.match("(?!^http:\/\/suggestqueries.).*google\..*/(custom|search|images)\?", url):
            return "Google"
        elif re.match(".*\.yahoo\..*/search", url):
            return "Yahoo"
        elif re.match(".*\.bing\..*/search", url):
            return "Bing"
        elif re.match("^http:\/\/www.youtube.com\/results\?", url):
            return "Youtube"            
        else:
            return ""
