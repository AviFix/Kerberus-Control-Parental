# -*- coding: utf-8 -*-

"""Benchmark, utilizando el listado de sitios mas visitados segun alexa.com"""

# Modulos externos
import sys,  time,  sqlite3,  csv,  datetime,  logging,  random

# Modulos propios
sys.path.append('../clases')
import consultor

class benchmark1():
#    verificador=consultor.Consultor()
    username='test_user'
    password='test'
    
    def cargarListaDeDominios(self):   
        self.ranking = csv.reader(open('top-1m.csv', 'rb'), delimiter=',')

    def correrBenchmark(self):
        """Realiza la verificacion de los dominios, leyendo el ranking de alexa"""
        verificador=consultor.Consultor()       
        verificador.setLogger(logging)
        conexion = sqlite3.connect('benchmarks.db')
        cursor=conexion.cursor()   
        cursor.execute('insert into benchmark_ejecucion(fecha,id_benchmark ) values (?,?)',(str(datetime.datetime.now()),1))
        id_ejecucion=cursor.execute('select last_insert_rowid();').fetchone()[0]
        conexion.commit()
        cant_sitios=1000.0
        i = 1
        for id_url, url in self.ranking:
            url="http://"+url
#            inicio=time.time()
            respuesta, mensaje=verificador.validarUrl(self.username, self.password, url)
#            fin=time.time()
#            tiempo=fin-inicio
#            # ahora con cache en el server
#            inicio_con_cache=time.time()
#            respuesta, mensaje=verificador.validarUrl(self.username, self.password, url)
#            fin_con_cache=time.time()
#            tiempo_con_cache=fin_con_cache-inicio_con_cache            
#            print "Dominio: %s - tiempo: %s - tiempo cacheado: %s" % (url, tiempo, tiempo_con_cache)
#            cursor.execute('insert into benchmark_result(id_ejecucion,id_url,url,tiempo,tiempo_con_cache,apto) values (?,?,?,?,?,?)',(id_ejecucion, id_url, url, tiempo, tiempo_con_cache, respuesta )) 
#            conexion.commit()   
            if i >= cant_sitios:
                break
            if i/cant_sitios:
                print "Sitio: %s, Progreso %s%%" % (str(i), str(i/cant_sitios*100))           
            i=i+1;
            ########### sacar esto!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if i > 150:
                time.sleep(random.randrange(1, 5))
            ########### sacar esto!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                
        conexion.close()
            
if __name__ == '__main__':
    bench=benchmark1()
    bench.cargarListaDeDominios()
    bench.correrBenchmark()
