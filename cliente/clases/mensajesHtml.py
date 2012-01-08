# -*- coding: utf-8 -*-

"""Modulo encargado de renderizar un template html, y mostrar un mensaje determinado"""

#Modulos externos
from string import Template

#Modulos propios
import config
import logging
import funciones

#Excepciones
class MensajesHtmlError(Exception): pass
#class nombre(ConsultorError): pass

# Logging
logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"Modulo Consultor")

# Clase
class MensajesHtml:
    def __init__(self,path_templates):
        self.path_templates=path_templates
        self.template_pedir_password=path_templates+'/pedirPassword.html'
        self.template_sitio_denegado=path_templates+'/sitioDenegado.html'

    def renderizarMensaje(self,template_path,diccionario):
        archivo_template=open(template_path,'r').read()
        template = Template(archivo_template)
        mensaje_renderizado=template.substitute(diccionario)
        return mensaje_renderizado

    def pedirPassword(self,mensaje=''):
        diccionario=dict(
            titulo='Deshabilitar filtrado temporalmente',
            subtitulo='(El filtrado estara inactivo por el resto de la sesión)',
            mensaje='Ingrese la password del administrador de kerberus',
            mensaje_error=mensaje
            )
        mensaje=self.renderizarMensaje(self.template_pedir_password,diccionario)
        return mensaje

    def denegarSitio(self,sitio=''):
        diccionario=dict(
            sitio=sitio,
            path_templates=self.path_templates
            )
        mensaje=self.renderizarMensaje(self.template_sitio_denegado,diccionario)
        return mensaje
