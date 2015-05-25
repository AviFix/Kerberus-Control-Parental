# -*- coding: utf-8 -*-

"""Modulo encargado de renderizar un template html, y mostrar un mensaje
determinado"""

#Modulos externos
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

#Modulos propios
import config
import pygeoip
modulo_logger = logging.getLogger('kerberus.' + __name__)
GEOIP = pygeoip.Database('/usr/share/GeoIP/GeoIP.dat')

# Clase
class Correo:

    def __init__(self):
        pass

    def enviar(self, destinatario, asunto, mensaje,
                FROM='Kerberus Control Parental <registro@kerberus.com.ar>'):
        # FIXME: Deberia enviarlos a un server local, el que deberia hacer de
        # relay de google

        msg = MIMEMultipart('alternative')
        msg['subject'] = asunto
        msg['To'] = destinatario
        msg['From'] = FROM
        HTML_BODY = MIMEText(mensaje, 'html')
        msg.attach(HTML_BODY)

        gmail_user = 'registro@kerberus.com.ar'
        gmail_pwd = 'p3r1c0cr1pt0man0'
        sender = 'consultas@kerberus.com.ar'
        modulo_logger.log(logging.DEBUG,
            "Enviando correo a: %s, subject: %s, mensaje: %s " %
            (destinatario, asunto, mensaje.decode('utf-8')))
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail(sender, destinatario, msg.as_string())
            smtpserver.close()
        except smtplib.SMTPException, e:
            modulo_logger.log(logging.ERROR,
                "Error al enviar un email a %s. ERROR: %s" % (destinatario, e))

    def enviarCorreoBienvenida(self, destinatario, usuario, password, idioma="es"):
        if idioma == "en":
            asunto = u'Your Kerberus\'s administrator password'
        else:
            asunto = u'Su contraseña de Kerberus'
        mensaje = MensajeHtml(idioma=idioma)
        self.enviar(destinatario, asunto, mensaje.bienvenida(usuario, password))

    def notificarNuevoUsuario(self, cant_users_reg, nombre, email, ip):
        asunto = u'Nuevo usuario Kerberus'
        mensaje = MensajeHtml()
        self.enviar(u'nuevosusuarios@kerberus.com.ar',
                    asunto,
                    mensaje.nuevoUsuario(cant_users_reg, nombre, email, ip)
                    )

    def notificarBajaUsuario(self, cant_users_reg):
        asunto = u'Baja de usuario Kerberus'
        mensaje = MensajeHtml()
        self.enviar(u'bajausuarios@kerberus.com.ar',
                    asunto,
                    mensaje.bajaUsuario(cant_users_reg)
                    )

    def enviarCorreoRecordarPassword(self, email, password, nombre, idioma="es"):
        if idioma == "en":
            asunto = u'Kerberus\'s password reminder'
        else:
            asunto = u'Recordatorio de contraseña de Kerberus Control Parental'
        mensaje = MensajeHtml(idioma=idioma)
        self.enviar(email,
                    asunto,
                    mensaje.recordarPassword(nombre, password)
                    )

    def enviarCorreoNuevaPassword(self, email, password, nombre, idioma="es"):
        mensaje = MensajeHtml(idioma=idioma)
        if idioma == "en":
            asunto = u'Kerberus\'s administrator password has been changed successfuly'
        else:
            asunto = u'Cambio de contraseña de kerberus'
        self.enviar(email, asunto, mensaje.nuevaPassword(nombre, password))

class MensajeHtml:
    def __init__(self, path_templates='emailTemplate/', idioma="es"):
        self.path_templates = path_templates
        self.idioma=idioma

    def renderizarMensaje(self, template, diccionario):
        archivo_template = open(self.path_templates+template, 'r').read()
        template = Template(archivo_template)
        mensaje_renderizado = template.substitute(diccionario)
        return mensaje_renderizado

    def bienvenida(self, usuario, password):
        diccionario = { 'usuario': usuario.encode('utf-8'),
                        'password': password.encode('utf-8')
                        }
        if self.idioma == "en":
            mensaje = self.renderizarMensaje('welcome.html', diccionario)
        else:
            mensaje = self.renderizarMensaje('bienvenida.html', diccionario)
        return mensaje

    def nuevaPassword(self, usuario, password):
        diccionario = { 'usuario': usuario.encode('utf-8'),
                        'password': password.encode('utf-8')
                        }
        if self.idioma == "en":
            mensaje = self.renderizarMensaje('passwordChange.html', diccionario)
        else:
            mensaje = self.renderizarMensaje('cambioDePassword.html', diccionario)
        return mensaje

    def nuevoUsuario(self, cant_users_reg, nombre, email, ip):
        try:
            country = GEOIP.lookup(ip).country
        except:
            country = ''

        diccionario = { 'cant_users_reg': cant_users_reg,
                        'nombre': nombre.encode('utf-8'),
                        'email': email.encode('utf-8'),
                        'ip': ip.encode('utf-8'),
                        'country': country.encode('utf-8')
                        }
        mensaje = self.renderizarMensaje('nuevoUsuario.html', diccionario)
        return mensaje

    def bajaUsuario(self, cant_users_reg):
        diccionario = { 'cant_users_reg': cant_users_reg }
        mensaje = self.renderizarMensaje('bajaUsuario.html', diccionario)
        return mensaje

    def recordarPassword(self, nombre, password):
        diccionario = { 'usuario': nombre.encode('utf-8'),
                        'password': password.encode('utf-8')
                        }
        if self.idioma == "en":
            mensaje = self.renderizarMensaje('rememberPassword.html', diccionario)
        else:
            mensaje = self.renderizarMensaje('recordarPassword.html', diccionario)
        return mensaje