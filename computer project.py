import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(
    host="sql6.freemysqlhosting.net",
    user="sql6409553",
    password="kn7MhCQugW",
    database='sql6409553' 
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


cursor = cnx.cursor().execute('insert into user_data(username, crypto , money) values ("yeet", 0 , 0)')
cnx.commit()
cnx.close()