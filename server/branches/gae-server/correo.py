# -*- coding: utf-8 -*-

"""Modulo encargado de renderizar un template html, y mostrar un mensaje
determinado"""

#Modulos externos
from google.appengine.api import mail
import os
import jinja2

PATH_TEMPLATES = "%s/emailTemplate" % os.path.dirname(__file__)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(PATH_TEMPLATES),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# Clase
class Correo:

    def __init__(self):
        pass

    def enviar(self, destinatario, asunto, mensaje_html="",
                FROM='Kerberus Control Parental <registro@kerberus.com.ar>'):
        if mail.is_email_valid(destinatario):
            message = mail.EmailMessage(sender=FROM, subject=asunto)
            message.reply_to = 'consultas@kerberus.com.ar'
            message.to = destinatario
            message.html = mensaje_html.encode('utf-8')
            if destinatario == 'nuevosusuarios@kerberus.com.ar' or destinatario == 'bajausuarios@kerberus.com.ar':
                mail.send_mail_to_admins('maximiliano@kerberus.com.ar', asunto, body='',html=message.html)
            else:            
                message.send()
        else:
            print "Dirección de email invalida!: %s" % destinatario

    def enviarCorreoBienvenida(self, destinatario, usuario, password, idioma="es"):
        if idioma == "en":
            asunto = u'Your Kerberus\'s administrator password'
        else:
            asunto = u'Su contraseña de Kerberus'
        mensaje = Mensaje(idioma=idioma)
        self.enviar(destinatario, asunto, mensaje.bienvenida(usuario, password))

    def notificarNuevoUsuario(self, cant_users_reg, email, nombre, password, 
            idioma, pais, region, ciudad, latitud_longitud, ip):
        asunto = u'Nuevo usuario Kerberus'
        mensaje = Mensaje()
        mensaje_html = mensaje.nuevoUsuario(
            cant_users_reg, 
            email, 
            nombre, 
            password, 
            idioma, 
            pais, 
            region, 
            ciudad, 
            latitud_longitud,
            ip
            )
        self.enviar(u'nuevosusuarios@kerberus.com.ar',
                    asunto,
                    mensaje_html
                    )

    def notificarBajaUsuario(
        self, cant_users_reg, nombre, email, pais, region, ciudad, latitud_longitud
        ):
        asunto = u'Baja de usuario Kerberus'
        mensaje = Mensaje()
        mensaje_html = mensaje.bajaUsuario(
            cant_users_reg, nombre, email, pais, region, ciudad, latitud_longitud
            )
        self.enviar(u'bajausuarios@kerberus.com.ar',
                    asunto,
                    mensaje_html
                    )

    def enviarCorreoRecordarPassword(self, email, password, nombre, idioma="es"):
        if idioma == "en":
            asunto = u'Kerberus\'s password reminder'
        else:
            asunto = u'Recordatorio de contraseña de Kerberus Control Parental'
        mensaje = Mensaje(idioma=idioma)
        mensaje_html = mensaje.recordarPassword(nombre, password)
        self.enviar(email,
                    asunto,
                    mensaje_html
                    )

    def enviarCorreoNuevaPassword(self, email, password, nombre, idioma="es"):
        mensaje = Mensaje(idioma=idioma)
        if idioma == "en":
            asunto = u'Kerberus\'s administrator password has been changed successfuly'
        else:
            asunto = u'Cambio de contraseña de kerberus'
        mensaje_html = mensaje.nuevaPassword(nombre, password)
        self.enviar(email, asunto, mensaje_html)

class Mensaje:
    def __init__(self, idioma="es"):
        self.idioma=idioma

    def renderizarMensaje(self, template, diccionario):
        temp = JINJA_ENVIRONMENT.get_template(template)
        mensaje_renderizado = temp.render(diccionario)
        return mensaje_renderizado

    def bienvenida(self, usuario, password):
        diccionario = { 'usuario': usuario.encode('utf-8'),
                        'password': password.encode('utf-8')
                        }
        if self.idioma == "en":
            mensaje_html = self.renderizarMensaje('welcome.html', diccionario)
        else:
            mensaje_html = self.renderizarMensaje('bienvenida.html', diccionario)
        return mensaje_html

    def nuevaPassword(self, usuario, password):
        diccionario = { 'usuario': usuario.encode('utf-8'),
                        'password': password.encode('utf-8')
                        }
        if self.idioma == "en":
            mensaje_html = self.renderizarMensaje('passwordChange.html', diccionario)
        else:
            mensaje_html = self.renderizarMensaje('cambioDePassword.html', diccionario)
        return mensaje_html

    def nuevoUsuario(self, cant_users_reg, email, nombre, password, idioma, pais, region, 
        ciudad, latitud_longitud, ip):

        diccionario = { 'cant_users_reg': cant_users_reg,
                        'nombre': nombre.encode('utf-8'),
                        'email': email.encode('utf-8'),
                        'country': pais,
                        'region': region,
                        'ciudad': ciudad,
                        'latitud_longitud': latitud_longitud,
                        'ip': ip
                        }
        mensaje_html = self.renderizarMensaje('nuevoUsuario.html', diccionario)
        return mensaje_html

    def bajaUsuario(
        self, cant_users_reg, nombre, email, pais, region, ciudad, latitud_longitud
        ):
        diccionario = { 
            'cant_users_reg': cant_users_reg,
            'nombre': nombre, 
            'email': email,
            'pais': pais,
            'region': region,
            'ciudad': ciudad,
            'latitud_longitud': latitud_longitud
        }
        mensaje = self.renderizarMensaje('bajaUsuario.html', diccionario)
        return mensaje

    def recordarPassword(self, nombre, password):
        diccionario = { 'usuario': nombre.encode('utf-8'),
                        'password': password.encode('utf-8')
                        }
        if self.idioma == "en":
            mensaje_html = self.renderizarMensaje('rememberPassword.html', diccionario)
        else:
            mensaje_html = self.renderizarMensaje('recordarPassword.html', diccionario)
        return mensaje_html