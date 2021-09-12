import mysql.connector
from mysql.connector import errorcode
from time import sleep
import datetime

currencies = ['botcoin', 'esterium', 'binguscoin', 'floppacoin','beans']

def make_connection():
    try:
        cnx = mysql.connector.connect(
            host ='blsuvxgq3bvwh8qw4ah7-mysql.services.clever-cloud.com',
            user='uf7gxtzihchkojup',
            password='K1bhziQq9KnSPAVSnFdH',
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
    query1 = f"SELECT {currency} , ratio FROM {currency} ORDER BY dates DESC LIMIT 1"
    cursor.execute(query1)
    results = cursor.fetchone()
    curr_exch_r8 = results[0]
    curr_ratio = results[1]

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

    ratio = round(avg_crypto/avg_money, 2)
    if ratio == curr_ratio:
        new_exch_r8 = curr_exch_r8
    elif round(curr_exch_r8*ratio) <= 1:
        new_exch_r8 = 1
    else:
        new_exch_r8 = round(curr_exch_r8*ratio)
    cnx.close()
    return new_exch_r8, ratio


def exch_r8_loop():
    while True:
        for i in currencies:
            cnx, cursor = make_connection()
            cursor.execute(f"SELECT dates FROM {i} ORDER BY dates DESC LIMIT 1")
            results = cursor.fetchone()[0]
            dt = datetime.datetime.strptime(results, '%Y-%m-%d %H:%M:%S')
            if datetime.datetime.now() >= (dt + datetime.timedelta(minutes=10)):
                curr_exch_r8, ratio = exch_r8_refresh(i)
                query = f"INSERT INTO {i}(dates, {i} , ratio) VALUES(%s,%s,%s)"
                cursor.execute(query, (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), curr_exch_r8, ratio))
                cnx.commit()
                sleep(5)
            cnx.close()
exch_r8_loop()