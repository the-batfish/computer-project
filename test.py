import mysql.connector
from mysql.connector import errorcode
import datetime
import time

try:
    cnx = mysql.connector.connect(
    host="blsuvxgq3bvwh8qw4ah7-mysql.services.clever-cloud.com",
    user="uf7gxtzihchkojup",
    password="K1bhziQq9KnSPAVSnFdH",
    database='blsuvxgq3bvwh8qw4ah7' 
    )



except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor = cnx.cursor()

def something():
	query = "INSERT INTO exchange_rate(next_reset) VALUES('%s') "
	value = datetime.datetime(2021,5,18,8,15,30).strftime('%Y-%m-%d %H:%M:%S')
	print(value)
	cursor.execute("update exchange_rate SET next_reset = %s",(value,))
	cnx.commit()
	cnx.close()
something()

while True:
    cursor.execute("select next_reset from exchange_rate")
    dt = datetime.datetime.strptime(cursor.fetchone()[0], '%Y-%m-%d %H:%M:%S')
    if datetime.datetime.now() >= dt:
        print('yeet')
        query = "update exchange_rate SET next_reset = %s"
        value = dt + datetime.timedelta(seconds=30)
        cursor.execute(query,(value.strftime('%Y-%m-%d %H:%M:%S'),))
        cnx.commit()
        cnx.close()
        time.sleep(10)
    else:
        pass
