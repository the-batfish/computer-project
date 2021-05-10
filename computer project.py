import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database='computerscienceprojectdb' 
    )
    print('yeet')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

#this function is for first time use
def add_account(user_id,username,password):
    cursor = cnx.cursor().execute('INSERT INTO economy_data(user_id , username , password , crypto , money) VALUES (%s , %s , %s , 0 , 0)' , (user_id , username , password))
    cnx.commit()
    cnx.close()

#my name yeet

