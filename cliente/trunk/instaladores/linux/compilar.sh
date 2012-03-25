#!/bin/bash
echo "   - Limpiando directorios..."
[ -d ../cliente/build ] && rm -r ../cliente/build
[ -d ../cliente/dist ] && rm -r ../cliente/dist
[ -d ../sincronizadorCliente/build ] && rm -r ../sincronizadorCliente/build
[ -d ../sincronizadorCliente/dist ] && rm -r ../sincronizadorCliente/dist

echo "   - configurando pyinstaller..."
python pyinstaller-1.5.1/Configure.py 2> /dev/null 1> /dev/null
echo "   - compilando cliente..."
python pyinstaller-1.5.1/Build.py -y ./cliente/cliente.spec > /dev/null
echo "   - compilando sincronizador..."
python pyinstaller-1.5.1/Build.py -y ./sincronizadorCliente/sincronizadorCliente.spec > /dev/null
echo "   - Generando archivo payload..."
cd cliente/dist/
tar cvfz ../../payload/cliente.tar.gz cliente > /dev/null
cd ../../
cd sincronizadorCliente/dist/
tar cvfz ../../payload/sincronizador.tar.gz sincronizadorCliente > /dev/null
cd ../../
