import os
import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql.converters import escape_string

dayPostfixVar = {
	0: "th",
	1: "st",
	2: "nd",
	3: "rd"
}
monthVar = {
	1: "january",
	2: "february",
	3: "march",
	4: "april",
	5: "may",
	6: "june",
	7: "july",
	8: "august",
	9: "september",
	10: "october",
	11: "november",
	12: "december"
}
monthDays = {
	1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}
def dayPostfix(day):
	if(day == 12 or day == 13):
		return "th"
	if(day % 10) > 3:
		return "th"
	return dayPostfixVar[day % 10]
	
def monthToStr(month):
	return monthVar[month]
def formatDate(day, month):
	return monthToStr(month) + str(day) + dayPostfix(day)

Connection = pymysql.connect(host='localhost', user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_USER_PASSWORD'].strip(), 
             db='history',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor )


url = ''


baseUrl = "http://thepeoplehistory.com/"


for i in range(1, 13):
	for j in range(1, monthDays[i]+1):
		url = baseUrl+formatDate(j, i) + ".html"
		print("Currently Processing: " + url)
		print()
		response = requests.get(url)
		soup = BeautifulSoup(response.content, "lxml").findAll('div', { "class":"newhighlight" })

		try:
			for block in soup:
				if(block.strong):
					year = int(block.strong.text)
					heading = str(block.find('span', { "class": "c9"}).text).strip()

					desc = ""
					for text in block.findAll(text=True):
						if( not (text.parent.name == "strong" or text.parent.name == "span")):
							desc += str(text).strip()
				
					with Connection.cursor() as cursor:
						sql = "INSERT INTO entries(`day`, `month`, `year`, `heading`, `description`) VALUES(%s, %s, %s, %s, %s)" 
						#print(heading+ desc)
						cursor.execute(sql, (j, i, year, escape_string(heading), escape_string(desc)))
					Connection.commit()
		except:
			pass
		finally:
			pass
Connection.close()
#		    	sql = "INSERT INTO entries (`day`,`month`,`year`,`heading`,`description`) VALUES (%s, %s, %s, %s, %s)"
