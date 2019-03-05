
from datetime import datetime
from dateutil import relativedelta
import time, json
import requests
import smtplib, ssl

class Stock:
	symbol = ''
	cost = 0
	purDate = ''
	portfolio = ''

def getStocks():
	stocks = []

	#PEP,106.25,10/05/2018,Tre Motif Roth
	with open("StockGains.txt", "r") as filestream:
		for line in filestream:
			currentline = line.split(",")
			stock = Stock()
			stock.symbol = currentline[0].rstrip()
			stock.cost = float(currentline[1].rstrip())
			stock.purDate = currentline[2].rstrip()
			stock.portfolio = currentline[3].rstrip()
			stocks.append(stock)
	return stocks

def calcMonthsFromPurchase(aStock):
	splitDate = aStock.purDate.split("/")
	purchaseDate = datetime(int(splitDate[2]),int(splitDate[0]),int(splitDate[1]))
	todaysDate = datetime(datetime.now().year,datetime.now().month, datetime.now().day)
	difference = relativedelta.relativedelta(todaysDate, purchaseDate)
	years = difference.years
	months = difference.months
	days = difference.days

	return (years*12)+months+(days/30)

def getStockPrice(aStock):
	URL = "https://api.iextrading.com/1.0/stock/"+aStock.symbol+"/price"
	print(URL)
	r = requests.get(url = URL)
	data = r.json()
	return float(data)	

def calcPerChange(aPurPrice, aCurPrice):
	print("Purchase Price ["+str(aPurPrice)+"]")
	print("Current Price ["+str(aCurPrice)+"]")
	return ((aCurPrice-aPurPrice)/aPurPrice)*100


def sendEmailAlert(aMsg):
	port = 587  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = "sellarit9@gmail.com"
	receiver_email = "sellarit9@gmail.com"
	password = "9Longbombs9$"
	message = """\
	Subject: %s

	%s.""" % (aMsg,aMsg)

	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
	    server.ehlo()  # Can be omitted
	    server.starttls(context=context)
	    server.ehlo()  # Can be omitted
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, message)


def main():

	for stock in getStocks():
		print("******"+stock.symbol+"*******")
		months = calcMonthsFromPurchase(stock)
		perChange = calcPerChange(stock.cost,getStockPrice(stock))

		if(months < 12):
			if perChange >= 12:
				sendEmailAlert("STOCK ["+stock.symbol+"] ALERT for PORTFOLIO ["+stock.portfolio+"] PRICE is GREAT THAN 12%")

		if(months >= 12):
			if perChange >= (months+1):
				sendEmailAlert("STOCK ["+stock.symbol+"] ALERT for PORTFOLIO ["+stock.portfolio+"] PRICE CHANGE IS [" +str(perChange)+"%]")

main()