#import sqlite3
import logging
import logging.handlers
import sys

sys.path.append('../conf')

#import config


def logSetup(logfile, loglevel=5, logsize=1, cant_rotaciones=1,
                cabecera_log=""):
    logger = logging.getLogger(cabecera_log)
    logger.setLevel(loglevel * 10)
    handler = logging.handlers.RotatingFileHandler(logfile,
                maxBytes=(logsize * (1 << 20)), backupCount=cant_rotaciones)
    fmt = logging.Formatter(
                                "[%(asctime)-12s.%(msecs)03d] "
                                "%(levelname)-4s {%(name)s %(threadName)s}"
                                " %(message)s",
                                "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


# Logging
#logger = logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB,
#config.LOG_CANT_ROTACIONES,"Modulo Servidores")
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
