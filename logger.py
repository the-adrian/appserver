# -*- coding: utf-8 -*-
__author__ = 'aramirez'

import logging
import logging.handlers
import os
import sys
import threading
import time


__PATH__ = "/var/log/appserver"

__FORMAT__ = '%(asctime)s| %(lineno)4s| %(message)-s'
__DATE_FMT__ = '%y-%m-%d %H:%M:%S'

LOGFILESIZE = 31457280
MAXLOGFILES = 2



def error(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/appserver/error.log')
        logger.setLevel(logging.ERROR)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/appserver/error.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathError = '/var/log/appserver/error.log'
	try:
            hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args= (pathError, ) )
            hilo.start()
	except:
	    pass


def warning(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/appserver/warning.log')
        logger.setLevel(logging.WARNING)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/appserver/warning.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathWarning = '/var/log/appserver/warning.log'
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args= ( pathWarning, ) )
        hilo.start()


def debug(msg):
    if validatePath(__PATH__):
        logger = logging.getLogger('/var/log/appserver/debug.log')
	
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(filename='/var/log/appserver/debug.log', mode='a', maxBytes=LOGFILESIZE,
                                                       backupCount=MAXLOGFILES)
        formatter = logging.Formatter(__FORMAT__, __DATE_FMT__)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(msg)
	pathDebug = "/var/log/appserver/debug.log"
        hilo = threading.Thread(target=limpiarLog, name="Hilo_limpiar_log", args= (pathDebug, ) )
        hilo.start()


def limpiarLog(ruta):
    try:
	cursor = open(ruta,'r')
    	listaLog = cursor.readlines()
    	cursor.close()
    except:
	pass # Error al leer el archivo 
    try:
    	cursor = open(ruta, "w")
    	linea1 = ""
        for linea in listaLog:
            if linea1 != linea:
                cursor.write(linea)
            linea1 = linea
        cursor.close()
    except:
	pass # Error al escribir en el archivo


def validatePath(strpath):
    try:
        if not os.path.isdir(strpath):
            # Tratara de crearla
            os.makedirs(strpath)
        return True
    except OSError, err:
        if err.errno == 13:
            print >> sys.stderr, \
                "No se puede crear el directorio  \"%s\", revisar permisos" % (strpath)

