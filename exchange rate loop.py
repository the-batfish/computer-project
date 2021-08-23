import datetime
import mysql.connector
from mysql.connector import errorcode
from time import sleep

currencies = ['botcoin','esterium','binguscoin','floppacoin']
def make_connection():
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
    return cnx, cnx.cursor()

def exch_r8_refresh(currency):
    cnx, cursor = make_connection()
    query1 = f"SELECT {currency} FROM {currency} ORDER BY date DESC LIMIT 1" 
    cursor.execute(query1)
    curr_exch_r8 = cursor.fetchone()[0]

    query2 = f"SELECT {currency} FROM economy_data" 
    cursor.execute(query2)
    n1 = 0
    tot_crypto = 0
    for i in cursor.fetchall():
        tot_crypto += i[0]
        n1 += 1
    avg_crypto = tot_crypto/n1

    query3 = "SELECT money FROM economy_data" 
    cursor.execute(query3)
    n2 = 0
    tot_money = 0
    for i in cursor.fetchall():
        tot_money += i[0]
        n2 += 1
    avg_money = tot_money/n2
    if avg_money == 0:
        avg_money = 1
    
    ratio = avg_crypto/avg_money
    if round(curr_exch_r8*ratio) <= 1: 
        new_exch_r8 = 1
    elif round(curr_exch_r8*ratio) >= 100:
        new_exch_r8 = 100
    else:
        new_exch_r8 = round(curr_exch_r8*ratio)
    cnx.close()
    return new_exch_r8

def exch_r8_loop():
    while True:
        for i in currencies:
            cnx, cursor = make_connection()
            cursor.execute(f"SELECT date FROM {i} ORDER BY date DESC LIMIT 1")
            results = cursor.fetchone()[0]
            dt = datetime.datetime.strptime(results, '%Y-%m-%d')
            if datetime.datetime.now() >= (dt + datetime.timedelta(days=1)):
                curr_exch_r8 = exch_r8_refresh(i)
                query = f"INSERT INTO {i}(date, {i}) VALUES(%s,%s)"
                cursor.execute(query,(datetime.datetime.now().strftime('%Y-%m-%d'),curr_exch_r8))
                cnx.commit()
                sleep(5)
            cnx.close()
exch_r8_loop()