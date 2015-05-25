#!/bin/bash
sudo rm -r kerberus
sudo svn export http://www.kerberus.com.ar/proyecto_control_parental/server/trunk kerberus
echo -n "Ingrese el server_id que se le asignara a este nodo:"
read id
sed -i -e s/"server_id =.*.$"/"server_id = ${id}"/g kerberus/server.conf
sudo /etc/init.d/kerberus-server restart
sudo /etc/init.d/kerberus-sincronizadorNodos restart
echo "Listo!."

