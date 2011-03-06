"""Test de unidad para el modulo consultor.py"""

# Modulos externos
import sys,  unittest

# Modulos propios
sys.path.append('../clases')
import consultor

class Urls(unittest.TestCase):
    extensiones_exceptuadas=("gif","jpeg","jpg","png","js","css","swf","ico","json","mp3","wav","rss","rar","zip","pdf","xml")      
    extensiones_no_exceptuadas=("html","htm","txt")  
    consult=consultor.Consultor()
    
    def verificarExtensionesExceptuadas(self):
        """Verificar que se exceptuen las extensiones no analizables por dansguardian"""
        for extension in self.extensiones_exceptuadas:
            self.assertTrue(consult.extensionValida(url))
             
    def verificarExtensionesNoExceptuadas(self):
        """Verificar que NO se exceptuen las extensiones analizables por dansguardian"""
        for extension in self.extensiones_no_exceptuadas:
            self.assertFalse(consultor.Consultor.extensionValida(url))

if __name__ == '__main__':
    unittest.main()
