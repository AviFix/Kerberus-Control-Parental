#import os
#import grp
import signal
import daemon
#import lockfile
import sys

sys.path.append('conf')

import config

daemonConf = config.serverConfig()

from server import  (
    setup_inicial,
    lanzar_server,
    detener_server,
#    reload_server,
    )

if daemonConf.log_daemon:
    stderr_file = open(daemonConf.daemon_stderr_file, 'w+')
    stdout_file = open(daemonConf.daemon_stdout_file, 'w+')
else:
    stderr_file = None
    stdout_file = None

context = daemon.DaemonContext(
   working_directory='/srv/kerberus/',
    umask=002,
#    pidfile=lockfile.FileLock('/tmp/kerberus.pid'),
    stderr=stderr_file,
    stdout=stdout_file,
    files_preserve=[stderr_file, stdout_file]
    )

context.signal_map = {
    signal.SIGTERM: detener_server,
#    signal.SIGHUP: reload_server,
    }


setup_inicial()

with context:
    lanzar_server()
