"""Test de unidad para el modulo manejadorUrls.py"""

# Modulos externos
import sys,  unittest

# Modulos propios
sys.path.append('../clases')
import consultor

class verificadorUrls(unittest.TestCase):
    extensiones_exceptuadas=(".gif",".jpeg",".jpg",".png",".js",".css",".swf",".ico",".json",".mp3",".wav",".rss",".rar",".zip",".pdf",".xml")
    extensiones_no_exceptuadas=(".html",".htm",".txt")
    verificador=consultor.Consultor()
    
    def testVerificarExtensionesExceptuadas(self):
        """Verificar que se exceptuen las extensiones no analizables por dansguardian"""
        for extension in self.extensiones_exceptuadas:
            self.assertTrue(self.verificador.extensionValida(extension))
           
    def testVerificarExtensionesNoExceptuadas(self):
        """Verificar que NO se exceptuen las extensiones analizables por dansguardian"""
        for extension in self.extensiones_no_exceptuadas:
            self.assertFalse(self.verificador.extensionValida(extension))
        

            
if __name__ == '__main__':
    unittest.main()
