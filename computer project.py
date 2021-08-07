import mysql.connector
from mysql.connector import errorcode
import datetime
from time import sleep
import threading
import getpass

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

def login():    
    user = input('Username :')
    passw = getpass.getpass("Password: ")
    cnx, cursor = make_connection()
    query = 'SELECT password from economy_data where username = %s'
    cursor.execute(query,(user,))
    realpass = cursor.fetchone()
    if realpass == None:
        print("Wrong username/password")
        cnx.close()
        return False , user , passw
    elif realpass[0] == passw:
        print('Login Successful!')
        cnx.close()
        return True , user , passw
    else:
        print("Wrong username/password")
        cnx.close()
        return False , user , passw


#this function is for first time use
def add_account(username,password):
    cnx, cursor = make_connection()
    try: 
        cursor.execute('INSERT INTO economy_data(username , password) VALUES (%s , %s)' , (username , password))
        cnx.commit()
        cnx.close()
        print('Account has been succesfully created!')
    except mysql.connector.IntegrityError:
        print("Account already exists")

#this function is for displaying the current and previous exchange rates
def show_exchange_rate():    
    cnx, cursor = make_connection()
    cursor.execute('SELECT current_exchange_rate , prev_exchange_rate FROM exchange_rate')
    results = cursor.fetchone()
    print('The current exchange rate is',results[0],'$ per crypto')
    print('The previous exchange rate was',results[1],'$ per crypto')

#this function is for showing the balance in your account
def balance(username):
    cnx, cursor = make_connection()
    query = "SELECT crypto, money FROM economy_data WHERE username = %s" 
    cursor.execute(query,(username,))
    results = cursor.fetchone()
    print('You have',results[0],'cryptos in your account')
    print('You have',results[1],'$ in your account')

#this function is for obtaining the current exchange rate for buying and selling
def exchange_rate():
    cnx, cursor = make_connection()
    cursor.execute('SELECT current_exchange_rate FROM exchange_rate')
    return cursor.fetchone()[0]

#this function is for buying crypto
def buy_crypto(num , username): #here num is the number of cryptos being requested to buy
    cnx, cursor = make_connection()
    exch = exchange_rate()
    cost = num * exch
    query = "SELECT crypto, money FROM economy_data WHERE username = %s" 
    cursor.execute(query,(username,)) 
    values = cursor.fetchone()
    available_crypto = values[0]
    available_money = values[1]
    if cost <= available_money:
        new_balance = available_money - cost
        new_crypto_balance = available_crypto + num
        command = "UPDATE economy_data SET crypto = %s , money = %s WHERE username = %s"
        values =  (new_crypto_balance , new_balance , username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        print('Transaction was completely successful')
        print(num,'cryptos have been added to your account')
    else:
        print('Sorry transaction was unsuccessful due to limited funds')

#this function is for buying crypto
def sell_crypto(num , username): #here num is the number of cryptos being sold
    cnx, cursor = make_connection()
    exch = exchange_rate()
    sale = num * exch
    query = "SELECT crypto, money FROM economy_data WHERE username = %s" 
    cursor.execute(query,(username,)) 
    values = cursor.fetchone()
    available_crypto = values[0]
    available_money = values[1]
    if num <= available_crypto:
        new_balance = available_money + sale
        new_crypto_balance = available_crypto - num
        command = "UPDATE economy_data SET crypto = %s , money = %s WHERE username = %s"
        values =  (new_crypto_balance , new_balance , username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        print('Transaction was completely successful')
        print(sale,'$ have been added to your account')
    else:
        print('Sorry transaction was unsuccessful due to limited funds')

def exch_r8_refresh():
    cnx, cursor = make_connection()
    query1 = "SELECT current_exchange_rate , prev_exchange_rate FROM exchange_rate" 
    cursor.execute(query1)
    curr_exch_r8 = cursor.fetchone()[0]

    query2 = "SELECT crypto FROM economy_data" 
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
    prev_exch_r8 = curr_exch_r8
    return new_exch_r8 , prev_exch_r8

def exch_r8_loop():
    cnx, cursor = make_connection()
    while True:
        cnx, cursor = make_connection()
        cursor.execute("select next_reset from exchange_rate")
        results = cursor.fetchone()
        dt = datetime.datetime.strptime(results[0], '%Y-%m-%d %H:%M:%S')
        if datetime.datetime.now() >= dt:
            query = "update exchange_rate SET current_exchange_rate = %s , prev_exchange_rate = %s , next_reset = %s"
            value = dt + datetime.timedelta(minutes = 30)
            curr_exch_r8,prev_exch_r8 = exch_r8_refresh()
            cursor.execute(query,(curr_exch_r8,prev_exch_r8,value.strftime('%Y-%m-%d %H:%M:%S'),))
            cnx.commit()
            cnx.close()
            sleep(5)
exch_r8_loop = threading.Thread(target=exch_r8_loop,daemon=True)
exch_r8_loop.start()


a,username,password = login()
if a == False:
    print('bruh')
else:
    while True:
        print('''
        1. balance
        2.
        ''')
        break


