import mysql.connector
from mysql.connector import errorcode
import datetime

try:
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database='computerscienceprojectdb' 
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
	value = datetime.datetime(2021,5,17,19,45,0).strftime('%Y-%m-%d %H:%M:%S')
	print(value)
	cursor.execute(query,(str(value),))
	cnx.commit()
	cnx.close()
something()