import os
import json
from flask import Flask, request, render_template
import pymysql


Connection = pymysql.connect(host='localhost', user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_USER_PASSWORD'].strip(), 
             db='history',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor )


app = Flask(__name__)
app.debug =True




@app.route('/')
def home():
	return render_template('index.html')


@app.route('/api', methods=['GET', 'POST'])
def api():
	if request.method == 'POST':
		month = int(request.values.get('month'))
		day = int(request.values.get('day'))
		year = int(request.values.get('year'))
		sql = "SELECT * from entries where day=" + str(day) + " AND month=" + str(month)+ " AND year="+str(year)
		print(sql)
		with Connection.cursor() as cursor:
			#print(heading+ desc)
			cursor.execute(sql)
			result = cursor.fetchall()
			for row in result:
				row['heading'] = row['heading'].replace("\\n","\n").replace("\\r","\n").replace("\\","")
				row['description'] = row['description'].replace("\\n","\n").replace("\\r","\n").replace("\\","")
			return json.dumps(result)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)