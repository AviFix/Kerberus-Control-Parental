import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

from sincronizadorCliente import *

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "Kerberus-daemon"
    _svc_display_name_ = "Kerberus daemon service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
       # Inicio
        logger = logSetup ()

        if  platform.uname()[0] == 'Linux':
            PATH_DB='/var/cache/kerberus/kerberus.db'
            LOG_FILENAME='/var/log/kerberus-cliente.log'
            logger.log(logging.DEBUG,"Plataforma detectada: GNU/Linux")
        else:
            logger.log(logging.DEBUG,"Plataforma detectada: Microsoft Windows")
            import  _winreg
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
            PATH_DB=_winreg.QueryValueEx(key,'kerberus-common')[0]+'\kerberus.db'
            LOG_FILENAME=_winreg.QueryValueEx(key,'kerberus-common')[0]+'\kerberus-sync.log'

        while True:
            #obtiene el tiempo en minutos
            periodo_expiracion=getPeriodoDeActualizacion()
            logger.log(logging.INFO, "Iniciando el demonio de sincronización")
            if not periodo_expiracion:
                periodo_expiracion=1
            logger.log(logging.DEBUG, "Periodo de actualizacion: %s minuto/s" % periodo_expiracion)
            # paso de minutos a segundos el periodo de expiracion
            periodo_expiracion=int(periodo_expiracion)*60
            conexion_db = sqlite3.connect(PATH_DB)
            cursor=conexion_db.cursor()
            ultima_actualizacion=cursor.execute('select ultima_actualizacion from sincronizador').fetchone()[0]
            tiempo_actual=time.time()
            tiempo_transcurrido=tiempo_actual - ultima_actualizacion
            if (tiempo_transcurrido > periodo_expiracion)  :
                logger.log(logging.DEBUG,"Sincronizando dominios permitidos/dengados con servidor...")
                sincronizarDominiosConServer(tiempo_actual)
                #borrarUrlsViejasCache(tiempo_actual, periodo_expiracion)
            else:
                tiempo_restante=ultima_actualizacion + periodo_expiracion - tiempo_actual
                logger.log(logging.DEBUG, "Faltan %s minutos para que se vuelva a sincronizar" % (tiempo_restante/60))
                time.sleep(tiempo_restante)
            conexion_db.close()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
