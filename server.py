#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
import sys
import logger
import recordsale
import threading
import select
import os
import classdb
import inhibirmdb
from liberror import registroError
from datetime import datetime
import libgral		

FLAG_CUT = True
COUNT_CUT = 0
IP_UDP = "127.0.0.1"
PORT_UDP = 8000

ACTUAL_RATE = 0
ACTUAL_OPEN_TIME = 0
ACTUAL_SHIFT = 0

MAX_FAIL_POLLS = 8
TIME_POLL = 0.01
MODE_DEBUG = True

SERVICE_VALIDATOR = "service validator manual"

# ------ PETICIONES DEL SOCKET DE C ------	
__POOL__     = "P|x"
__SHIFT__    = "T|x"
__ERROR__    = "E|"
__AMOUNT__   = "M|"
__RATE__     = "R|x"
__OPENTIME__ = "O|x"
__TICKET__   = "K|x"
# __CANALES__  = "C|x"
__VENTA__    = " \x02"

__PETITION_AMOUNT__   = "M|x"

def activateValidator():
	try:
		os.system(SERVICE_VALIDATOR)
	except:
		if MODE_DEBUG:
			print "file not found : validator.c"
		logger.error('validtor.c no fue encontrado')


def startThreadValidator():
	if MODE_DEBUG:
		print "starting validator"
	try:
		validator = threading.Thread(target=activateValidator, name="thread validator")
		validator.start()
	except:
		if MODE_DEBUG:
			print "unable to start service validator"


# ------------ FUNTIONS ----------------------

def setSale(sale):
	recordsale.main(sale)


def setActualShift():
	shift = classdb.getActualShift()
	global ACTUAL_SHIFT
	ACTUAL_SHIFT = shift
	shift = "T|" + str(shift)
	if MODE_DEBUG:
		print "TX: %s" % (shift)
	return shift


def setRate():
	rate = classdb.getRate()
	rate = rate * 100
	rate = int(rate)
	global ACTUAL_RATE
	ACTUAL_RATE = rate
	rate = "R|" + str(rate)
	if MODE_DEBUG:
		print "Tx: %s" % (rate)
	return rate


def setOpenTime():
	opentime = str(classdb.getOpenTime())
	global ACTUAL_OPEN_TIME
	ACTUAL_OPEN_TIME = opentime
	opentime = "O|"+opentime
	if MODE_DEBUG:
		print "TX: %s" % opentime
	return opentime


def setTicket():
	ticket = int(classdb.getTicket()) + 1
	ticket = "K|"+str(ticket)
	return ticket


def existChangeRate():
	newrate = classdb.getRate()
	newrate = int(newrate * 100)
	if newrate != ACTUAL_RATE:
		return True
	return False


def existChangeOpenTime():
	newtime = classdb.getOpenTime()
	if str(newtime) != str(ACTUAL_OPEN_TIME):
		return True
	return False


def getStatusCutShift():
	data = classdb.existCutShift()
	if data == '1':
		return True
	return False


def __main__():
	existchangerate = False
	existchangeopentime = False
	count = 0
	existcutshift = False
	if MODE_DEBUG:
		print "Connecting to %s port: %i" % (IP_UDP,PORT_UDP)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((IP_UDP, PORT_UDP))
	sock.setblocking(0)

	try:
		if MODE_DEBUG:
			print "Connecting..."
		sock.sendto("starting socket udp", (IP_UDP,PORT_UDP))
		if MODE_DEBUG:
			print "successful Connection"
	except:
		if MODE_DEBUG:
			print "connection failed"
		logger.error("no se puede iniciar el socket")
		sys.exit(0)

	while True:
		automaticcut = classdb.getTypeCutShift()
		if automaticcut:
			pass # Agregar la parte del corte automatico
		time.sleep(TIME_POLL)
		msgsock = select.select([sock], [], [], 0.5)
		existchangerate = existChangeRate()
		existchangeopentime = existChangeOpenTime()
		existcutshift = getStatusCutShift()
		if msgsock[0]:
			count = 0
			rx = ""
			pollfailed = 0
			# attempts to activate validator
			attemptsactivate = 0 
			rx, address = sock.recvfrom(1024)
			if MODE_DEBUG:
				if rx != "P|x":
					print "rx: ", rx

			if existchangerate:
				sock.sendto(setRate(), address)
				logger.debug("cambio de tarifa a "+str(ACTUAL_RATE)+"")

			if existchangeopentime:
				sock.sendto(setOpenTime(), address)
				logger.debug("cambio del tiempo de apertura a "+str(ACTUAL_OPEN_TIME)+" seg.")

			if existcutshift:
				sock.sendto(__PETITION_AMOUNT__, address)
				classdb.deactivateCutShift()

			if len(rx) > 2:
				if rx == __RATE__:
					sock.sendto(setRate(), address)
				elif rx == __OPENTIME__:
					sock.sendto(setOpenTime(), address)
				elif rx == __TICKET__:
					sock.sendto(setTicket(), address)
				elif rx == __SHIFT__:
					sock.sendto(setActualShift(), address)
				elif rx.startswith(__ERROR__):
					registroError(rx)
				elif rx.startswith(__AMOUNT__):
					amount = libgral.separeteAmount(rx)
					classdb.cutShift(amount)
					sock.sendto(activeShift(), address)
					if MODE_DEBUG:
						print "CUT SHIFT"
				elif len(rx) > 70:
					if MODE_DEBUG:
						print "Sale :%s" % (rx)  
					try:
						threadsale = threading.Thread(target=setSale, args=(rx, ), name="thread record sale")
						threadsale.start()
					except:
						logger.error("no se pude registrar la venta posibles problemas con las consultas")
						if MODE_DEBUG:
							print "can't record sale, possible error of query  sql"
		# failed poll
		else:
			pollfailed += 1
			if MODE_DEBUG:
				print "Lost connection !!"
			if pollfailed == MAX_FAIL_POLLS:
				while attemptsactivate < 3:
					if MODE_DEBUG:
						print "attempt for activate validator"
					time.sleep(0.5)
					try:
						inhibirmdb.main()
						time.sleep(0.3)
						startThreadValidator()
						logger.warning("reinicio automático de validator")
						break
					except:
						attemptsactivate += 1



if __name__=='__main__':
		__main__()



					







