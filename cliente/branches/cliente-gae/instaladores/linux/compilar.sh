#!/bin/bash

echo "   - Limpiando directorios..."
[ -d ../cliente/build ] && rm -r ../cliente/build
[ -d ../cliente/dist ] && rm -r ../cliente/dist
[ -d ../sincronizadorCliente/build ] && rm -r ../sincronizadorCliente/build
[ -d ../sincronizadorCliente/dist ] && rm -r ../sincronizadorCliente/dist
[ -d ../desinstalador/build ] && rm -r ../desinstalador/build
[ -d ../desinstalador/dist ] && rm -r ../desinstalador/dist
[ -d ../systemtray/build ] && rm -r ../systemtray/build
[ -d ../systemtray/dist ] && rm -r ../systemtray/dist

grep ENTORNO_DE_DESARROLLO=True ../../conf/config.py > /dev/null
if [ ${?} -eq 0 ];then
	echo "   - Seteando entorno en produccion..."
	sed -i s/ENTORNO_DE_DESARROLLO=True/ENTORNO_DE_DESARROLLO=False/g ../../conf/config.py
	SETEADO_ENTORNO=true 
fi
echo "   - compilando cliente..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./cliente/cliente.spec
echo "   - compilando sincronizador..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./sincronizadorCliente/sincronizadorCliente.spec
echo "   - compilando desinstalador..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./desinstalador/desinstalador.spec
echo "   - compilando systemtray..."
python ../common/pyinstaller-2.0/pyinstaller.py -y --log-level=ERROR ./systemtray/systemtray.spec

if [ ${SETEADO_ENTORNO} ]; then
          echo "   - Volviendo al entorno de desarrollo..."
          sed -i s/ENTORNO_DE_DESARROLLO=False/ENTORNO_DE_DESARROLLO=True/g  ../../conf/config.py
fi
