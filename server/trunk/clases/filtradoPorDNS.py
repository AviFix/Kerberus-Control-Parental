# -*- coding: utf-8 -*-

"""Modulo encargado de verificar un dominio contra opendns"""

'''
@copyright: GPL v.3
@author: ehooo
@contact: &lt;ehooo|at|rollanwar|dot|net&gt;
'''
import dns.resolver
import dns.reversename
import logging

modulo_logger = logging.getLogger('Kerberus')


class DnsFilter():
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = ['208.67.222.222', '208.67.220.220']

    def testDominio(self, dominio):
        """Verifica contra opendns si el dominio esta permitido"""
        try:
            respuesta = self.resolver.query(dominio, 'A')
            ip = respuesta[0].address
            if ip == "67.215.65.130":
                modulo_logger.log(logging.INFO,
                    "Dominio Denegado por DNS: %s" % dominio)
                return False
            else:
                modulo_logger.log(logging.INFO,
                    "Dominio Permitido por DNS: %s" % dominio)
                return True
        except dns.resolver.NoAnswer:
            modulo_logger.log(logging.ERROR,
                "ERROR: No se pudo determinar si el dominio %s es valido. " \
                % dominio)
            return True
