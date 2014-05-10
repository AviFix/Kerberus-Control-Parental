#!/bin/bash

# Variables
VERSION="1.1"
PATH_COMMON="./deb/usr/share/kerberus/"
echo "----------------------------------------------------"
echo "Regenerando el paquete DEB de kerberus, version ${VERSION}"
echo "----------------------------------------------------"
echo ""

grep "ENTORNO_DE_DESARROLLO = True" ../../conf/config.py > /dev/null
if [ ${?} -eq 0 ]; then 
  echo "- Cambiando a modo produccion";
  sed -i 's/ENTORNO_DE_DESARROLLO\ =\ True/ENTORNO_DE_DESARROLLO\ =\ False/g' ../../conf/config.py
fi
echo "- Regenerando la DB a partir del archivo cliente.sql..."
if [ -f ${PATH_COMMON}/kerberus.db ]; then
  rm ${PATH_COMMON}/kerberus.db
fi
sqlite3  ${PATH_COMMON}/kerberus.db < ../../cliente.sql

if [ -f ${PATH_COMMON}/licencia.txt ]; then
  rm ${PATH_COMMON}/licencia.txt
fi
cp ../windows/ArchivosDefault/licencia.txt ${PATH_COMMON}/licencia.txt

echo "- Copiando templates..."
cp ../../templates/* ${PATH_COMMON}/templates/


echo "Listo."
exit 0
