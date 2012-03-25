#!/bin/sh
ACCION=$1
PROXY_HOST=$2
PROXY_PORT=$3

gnome_proxy() {
	case "$1" in
	set)
	  	existe_aplicacion gsettings2
	  	if [ ${?} ];
		then
			gsettings set org.gnome.system.proxy.http host '${PROXY_HOST}'
			gsettings set org.gnome.system.proxy.https host '${PROXY_HOST}'
			gsettings set org.gnome.system.proxy.http port ${PROXY_PORT}
			gsettings set org.gnome.system.proxy.https port ${PROXY_PORT}
			gsettings set org.gnome.system.proxy use-same-proxy false
			gsettings set org.gnome.system.proxy mode 'manual'
		else
		  	echo "No esta instalado gsettings, por lo que no se setea el proxy para Gnome."
		fi
	;;
	unset)
	        gsettings set org.gnome.system.proxy.http host ''
        	gsettings set org.gnome.system.proxy.https host ''
	        gsettings set org.gnome.system.proxy.http port 0 
	        gsettings set org.gnome.system.proxy.https port 0
        	gsettings set org.gnome.system.proxy use-same-proxy true
	        gsettings set org.gnome.system.proxy mode 'none'
        	gsettings reset-recursively org.gnome.system.proxy
	;;
	*)
                echo "Opcion invalida. Deber ser 'set' o 'unset'"
                exit 1
esac 
}

kde_proxy() {
  case "$1" in
    	set)
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key AuthMode 0
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key Proxy\ Config ''
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key ReversedException false
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key ftpProxy ''
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key ProxyType 1
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key httpProxy "http://${PROXY_HOST}:${PROXY_PORT}"
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key httpsProxy "http://${PROXY_HOST}:${PROXY_PORT}"
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key NoProxyFor	"localhost, 127.0.0.1"
	;;
      	unset)
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key AuthMode 0
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key Proxy\ Config ''
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key ReversedException false
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key ftpProxy ''
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key ProxyType 0
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key httpProxy ''
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key httpsProxy ''
		kwriteconfig --file kioslaverc --group Proxy\ Settings --key NoProxyFor	''
	;;
      	*)
	  	echo "Opcion invalida. Deber ser 'set' o 'unset'"
		exit 1
esac
}


case "$1" in
set)
	if [ -n "$PROXY_HOST" ]
	then
	    	echo "Setting proxy configuration : $PROXY_HOST:$PROXY_PORT"
		gnome_proxy set
		kde_proxy set
	fi
;;
unset)
	gnome_proxy unset
	kde_proxy unset
;;
*)
	echo "setProxy.sh <accion> <proxy_host> <proxy_port>"
	exit 1
esac

