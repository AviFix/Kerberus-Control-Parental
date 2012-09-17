#!/bin/bash
PATH_CLIENTE=/var/cache/kerberus
BASE_CLIENTE=${PATH_CLIENTE}/kerberus.db
SQL_CLIENTE=./cliente.sql
SINCRONIZADOR=./sincronizadorCliente.py

if [ -f ${BASE_CLIENTE} ] ; then
	echo "Regenerando base cliente..."
	rm ${BASE_CLIENTE}
else
  	echo "Generando base cliente..."
	if [ ! -d ${PATH_CLIENTE} ]; then
	  echo "Creando directorio"
	  mkdir -p ${PATH_CLIENTE}
	fi
fi

cat ${SQL_CLIENTE}|sqlite3 ${BASE_CLIENTE}

echo "Recargando sincronizador..."
/etc/init.d/kerberus-sincronizador restart

echo "Recargando cliente..."
/etc/init.d/kerberus-cliente restart
