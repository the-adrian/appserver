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
