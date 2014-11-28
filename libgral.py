import datetime


def getDay():
    day = datetime.datetime.now()
    day = day.strftime("%d")
    day = str(day)
    return day


def getDate():
    date = str(datetime.date.today())
    return date


def getTime():
    time = str(datetime.datetime.now())
    time = time.split(' ') 
    time = time[1]  
    time = time.split('.')
    time = time[0]
    return time


def getAllDate():
    fecha_hora = str(datetime.datetime.today())
    fecha_hora = fecha_hora.split('.')  # Separa las decimas de segundos
    fecha_hora = fecha_hora[0]  
    return fecha_hora


def separeteAmount(amount):
    total = 0
    totalamount = amount.split(';')
    coins = totalamount[0].split(',')
    bills = totalamount[1].split(',')
    totalcoins = int(coins[1])
    totalbills = int(bills[1])
    total = totalcoins + totalbills
    total = total / 100
    return total


def getNameOfDay():
    day = datetime.datetime.now()
    day = day.strftime("%A")
    if day == "Monday":
        return "Lunes"
    elif day == "Tuesday":
        return "Martes"
    elif day == "Wednesday":
        return "Miercoles"
    elif day == "Thursday":
        return "Jueves"
    elif day == "Friday":
        return "Viernes"
    elif day == "Saturday":
        return "Sabado"
    elif day == "Sunday":
        return "Domingo"


def getNumbreOfDay():
    dia = datetime.datetime.now()
    dia = dia.strftime("%d")
    dia = str(dia)
    return dia


def ObtenerFecha():
    fecha = str(datetime.date.today())
    return fecha


def getHour():
    hour = str(datetime.datetime.now())
    hour = hour.split(' ') 
    hour = hour[1]  
    hour = hour.split('.')
    hour = hour[0]
    return hour


def getAllDate():
    date = str(datetime.datetime.today())
    date = date.split('.')  # Separa las decimas de segundos
    date = date[0]  
    return date
