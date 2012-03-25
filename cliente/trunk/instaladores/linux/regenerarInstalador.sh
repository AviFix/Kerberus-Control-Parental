#!/bin/bash
echo "----------------------------------------------------"
echo "Regenerando el instalador de kerberus para GNU/Linux"
echo "----------------------------------------------------"
echo ""
nombre_inst="kerberus-installer.sh"
echo "- Compilando ${nombre_inst}..."
sh compilar.sh 
echo "- Generando DB..."
if [ -f payload/kerberus.db ]; then
  rm payload/kerberus.db
fi
cat ../../cliente/cliente.sql |sqlite3 payload/kerberus.db

echo "- Copiando templates..."
cp ../../cliente/templates/* payload/templates/

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
