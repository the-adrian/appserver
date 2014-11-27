#-*- coding:utf-8 -*-
import MySQLdb
import libgral


DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'root'
DB_NAME = 'kernotek'


def run_query(query):
	datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
	conn = MySQLdb.connect(*datos)
	cursor = conn.cursor()
	cursor.execute(query)

	if query.upper().startswith("SELECT"):
		data = cursor.fetchall()
	else:
		conn.commit()
		data = None

	cursor.close()
	conn.close()
	return data


def getActualShift():
	query = "SELECT MAX(shiftno) FROM panelshifthead;"
	data = run_query(query)
	return data


def getRate():
	query = "SELECT rate FROM config;"
	data = run_query(query)
	return data


def changeRate(rate):
	query = "UPDATE config SET rate = '"+rate+"';"
	run_query(query)


def getOpenTime():
	query = "SELECT t_apertura FROM config;"
	data = run_query(query)
	return data


def changeOpenTime(time):
	query = "UPDATE config SET t_apertura = '"+time+"';"
	run_query(query)


def getTicket():
	query = "SELECT no_venta_act FROM cnfig;"
	data = run_query(query)
	return data


def recordSale(query):
	run_query(query)


def existCutShift():
	query = "SELECT hacer_corte_turno FROM config;"
	data = run_query(query)
	return data


def deactivateCutShift():
	query = "UPDATE config SET hacer_corte_turno = '0';"
	run_query(query)


def getTypeCutShift():
	query = "SELECT tipo_corte FROM config;"
	data = run_query(query)
	return data


def getTypeOfTime():
	query = "SELECT corte_automatico FROM config;"
	data = run_query(query)
	return data


def getTimeAutomaCut():
	query = "SELECT tiempo_corte FROM config;"
	data = run_query(query)
	return data


def startShift(numShift, startDate, amount):
	query = "INSERT INTO panelshifthead(shiftno, datestart, amountini) "\
			"VALUES("+str(numShift)+", "+str(startDate)+", "+str(amount)+");"
	run_query(query)


def cutShift(amount):
	activeshift = getActualShift()
	dateendcute = libgral.getAllDate()
	newshift = int(activeshift) + 1
	query = "UPDATE panelshifthead SET dateend = '"+str(deteendcut)+"', "\
			"amountend = "+str(amount)+" WHERE shiftno = "+str(activeshift)+";"
	run_query(query)
	startShift(newshift, dateendshift,amount)
	query = "UPDATE config SET shift_no_act = "+str(newshift)+""
	run_query(query)


