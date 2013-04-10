#!/bin/bash
VERSION="1.1"
echo "----------------------------------------------------"
echo "Regenerando el instalador de kerberus, version ${VERSION} para GNU/Linux"
echo "----------------------------------------------------"
echo ""

nombre_inst="kerberus-installer-${VERSION}.sh"

grep "ENTORNO_DE_DESARROLLO = True" ../../conf/config.py > /dev/null
if [ ${?} -eq 0 ]; then 
  echo "- Cambiando a modo produccion";
  sed -i 's/ENTORNO_DE_DESARROLLO\ =\ True/ENTORNO_DE_DESARROLLO\ =\ False/g' ../../conf/config.py
fi
echo "- Compilando ${nombre_inst}..."
sh compilar.sh

echo "- Generando archivo payload..."
cd cliente/dist/
tar cvfz ../../payload/cliente.tar.gz cliente > /dev/null
cd ../../
cd sincronizadorCliente/dist/
tar cvfz ../../payload/sincronizador.tar.gz sincronizadorCliente > /dev/null
cd ../../
cd desinstalador/dist/
tar cvfz ../../payload/desinstalador.tar.gz desinstalador > /dev/null
cd ../../


#echo "- Copiando DB del instalador de windows..."
#if [ -f payload/kerberus.db ]; then
#  rm payload/kerberus.db
#fi
#cp ../windows/ArchivosDefault/kerberus.db payload/kerberus.db
echo "- Regenerando la DB a partir del archivo cliente.sql..."
if [ -f payload/kerberus.db ]; then
  rm payload/kerberus.db
fi
sqlite3  payload/kerberus.db < ../../cliente.sql

#if [ -f payload/licencia.txt ]; then
#  rm payload/licencia.txt
#fi
#cp ../windows/ArchivosDefault/licencia.txt payload/licencia.txt

echo "- Copiando templates..."
cp ../../templates/* payload/templates/

echo "- Armando el archivo self-extracting..."
cd payload
tar cf ../payload.tar ./*
cd ..

if [ -e "payload.tar" ]; then
    gzip -f payload.tar

    if [ -e "payload.tar.gz" ]; then
        cat decompress payload.tar.gz > ${nombre_inst}
	rm payload.tar.gz
    else
        echo "payload.tar.gz does not exist"
        exit 1
    fi
else
    echo "payload.tar does not exist"
    exit 1
fi

echo "Listo."
exit 0
