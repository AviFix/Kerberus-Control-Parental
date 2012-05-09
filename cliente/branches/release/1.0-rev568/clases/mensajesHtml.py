# -*- coding: utf-8 -*-

"""Modulo encargado de renderizar un template html, y mostrar un mensaje determinado"""

#Modulos externos
from string import Template

#Modulos propios
import config
import logging

modulo_logger = logging.getLogger('kerberus.'+__name__)

#Excepciones
class MensajesHtmlError(Exception): pass
#class nombre(ConsultorError): pass


# Clase
class MensajesHtml:
    def __init__(self,path_templates):
        self.path_templates=path_templates
        self.template_pedir_password=path_templates+'/pedirPassword.html'
        self.template_sitio_denegado=path_templates+'/sitioDenegado.html'
        self.template_cambiar_password=path_templates+'/cambiarPassword.html'
        self.template_mensaje=path_templates+'/mensaje.html'

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

    def cambiarPassword(self,mensaje='',focus_en=''):
        diccionario=dict(
            titulo='Cambiar password',
            subtitulo='(Cambio de la password del administrador de kerberus)',
            mensaje_error=mensaje,
            focus=focus_en
            )
        mensaje=self.renderizarMensaje(self.template_cambiar_password,diccionario)
        return mensaje

    def passwordCambiadaCorrectamente(self,mensaje=''):
        diccionario=dict(
            titulo='Cambiar password',
            mensaje=mensaje
            )
        mensaje=self.renderizarMensaje(self.template_mensaje,diccionario)
        return mensaje

    def recordarPassword(self,mensaje=''):
        diccionario=dict(
            titulo='Recordar password',
            mensaje=mensaje
            )
        mensaje=self.renderizarMensaje(self.template_mensaje,diccionario)
        return mensaje

    def denegarSitio(self,sitio=''):
        diccionario=dict(
            sitio=sitio,
            path_templates=self.path_templates
            )
        mensaje=self.renderizarMensaje(self.template_sitio_denegado,diccionario)
        return mensaje
