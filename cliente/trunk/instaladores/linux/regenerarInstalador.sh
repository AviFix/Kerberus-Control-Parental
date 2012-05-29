#!/bin/bash
VERSION="1.0"
echo "----------------------------------------------------"
echo "Regenerando el instalador de kerberus, version ${VERSION} para GNU/Linux"
echo "----------------------------------------------------"
echo ""

nombre_inst="kerberus-installer-${VERSION}.sh"
echo "- Compilando ${nombre_inst}..."
sh compilar.sh
echo "- Copiando DB del instalador de windows..."
if [ -f payload/kerberus.db ]; then
  rm payload/kerberus.db
fi
cp ../windows/ArchivosDefault/kerberus.db payload/kerberus.db
if [ -f payload/licencia.txt ]; then
  rm payload/licencia.txt
fi
cp ../windows/ArchivosDefault/licencia.txt payload/licencia.txt

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
