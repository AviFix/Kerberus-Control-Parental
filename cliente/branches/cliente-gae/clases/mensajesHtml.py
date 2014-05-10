# -*- coding: utf-8 -*-

"""Modulo encargado de renderizar un template html, y mostrar un mensaje
determinado"""

#Modulos externos
from string import Template
import sys
sys.path.append('../')

#Modulos propios
import logging
import language

modulo_logger = logging.getLogger('kerberus.' + __name__)


#Excepciones
class MensajesHtmlError(Exception):

    def __init__(self):
        super(MensajesHtmlError, self).__init__()
        pass

#class nombre(ConsultorError): pass


# Clase
class MensajesHtml:
    def __init__(self, path_templates):
        self.path_templates = path_templates
        self.template_pedir_password = path_templates + '/pedirPassword.html'
        self.template_sitio_denegado = path_templates + '/sitioDenegado.html'
        self.template_cambiar_password = path_templates + \
                                        '/cambiarPassword.html'
        self.template_mensaje = path_templates + '/mensaje.html'

    def renderizarMensaje(self, template_path, diccionario):
        archivo_template = open(template_path, 'r').read()
        template = Template(archivo_template)
        mensaje_renderizado = template.substitute(diccionario)
        return mensaje_renderizado

    def pedirPassword(self, mensaje=''):
        titulo=_('Temporarily Disable filter')
        diccionario = {
            'titulo': titulo,
            'subtitulo': u'(El filtrado estará inactivo hasta que reinicie la PC)'.encode('utf-8'),
            'mensaje': u'Ingrese la contraseña del administrador de Kerberus'.encode('utf-8'),
            'mensaje_error': mensaje.encode('utf-8')
            }
        mensaje = self.renderizarMensaje(self.template_pedir_password,
                                        diccionario)
        return mensaje

    def cambiarPassword(self, mensaje='', focus_en=''):
        diccionario = {
            'titulo': u'Cambiar contraseña'.encode('utf-8'),
            'subtitulo': u'(Cambio de la contraseña del administrador de Kerberus)'.encode('utf-8'),
            'mensaje_error': mensaje.encode('utf-8'),
            'focus': focus_en.encode('utf-8')
            }
        mensaje = self.renderizarMensaje(self.template_cambiar_password,
                                            diccionario)
        return mensaje

    def passwordCambiadaCorrectamente(self, mensaje=''):
        diccionario = {
            'titulo': u'Cambiar contraseña'.encode('utf-8'),
            'mensaje': mensaje.encode('utf-8')
            }
        mensaje = self.renderizarMensaje(self.template_mensaje, diccionario)
        return mensaje

    def recordarPassword(self, mensaje=''):
        diccionario = {
            'titulo': u'Recordar contraseña'.encode('utf-8'),
            'mensaje': mensaje.encode('utf-8')
            }
        mensaje = self.renderizarMensaje(self.template_mensaje, diccionario)
        return mensaje

    def denegarSitio(self, sitio=''):
        diccionario = {
            'sitio': sitio.encode('utf-8'),
            'path_templates': self.path_templates
            }
        mensaje = self.renderizarMensaje(self.template_sitio_denegado,
                                            diccionario)
        return mensaje


def main():
    pass

# Importante: los módulos no deberían ejecutar
# código al ser importados
if __name__ == '__main__':
    main()