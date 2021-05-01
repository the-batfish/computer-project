import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(
    host="sql6.freemysqlhosting.net",
    user="sql6409553",
    password="kn7MhCQugW",
    )
    print('yeet')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
