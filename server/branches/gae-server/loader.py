# Comando para hacer la carga de datos:
#./bulkload_client.py --filename=/home/mboscovich/server/gae-server/dominios.csv 
#                     --kind=Dominio 
#                     --url=http://localhost:8080/load
# Poner en false threadsafe y descomentar la linea del handler de load en app.yaml


from google.appengine.ext import bulkload, ndb
from datetime import datetime

def utf8string(s):
    return unicode(s, 'utf-8')
    
def fecha(s):
	return datetime.strptime(s,'%Y-%m-%d %H:%M:%S')

class DominioLoader(bulkload.Loader):
    def __init__(self):
        fields = [
            ("estado", utf8string),
            ("url", utf8string),
            ("ultima_revision", fecha),
            ("verificador", utf8string)
            ]
       
        bulkload.Loader.__init__(self, 'Dominio', fields)

if __name__ == "__main__":
    bulkload.main(DominioLoader())

