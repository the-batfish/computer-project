import mysql.connector
from mysql.connector import errorcode

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

#this function is for first time use
def add_account(user_id,username,password):
    cursor.execute('INSERT INTO economy_data(user_id , username , password , crypto , money) VALUES (%s , %s , %s , 0 , 0)' , (user_id , username , password))
    cnx.commit()
    cnx.close()
    print('Account has been succesfully created!')

#this function is for displaying the current and previous exchange rates
def show_exchange_rate():    
    cursor.execute('SELECT current_exchange_rate , prev_exchange_rate FROM exchange_rate')
    results = cursor.fetchone()
    print('The current exchange rate is',results[0],'$ per crypto')
    print('The previous exchange rate was',results[1],'$ per crypto')

#this function is for obtaining the current exchange rate for buying and selling
def exchange_rate():
    cursor.execute('SELECT current_exchange_rate FROM exchange_rate')
    return cursor.fetchone()[0]

#this function is for buying crypto
def buy_crypto(num , username): #here num is the number of cryptos being requested to buy
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
        print(num,' cryptos have been added to your account')
    else:
        print('Sorry transaction was unsuccessful due to limited funds')

#this function is for buying crypto
def sell_crypto(num , username): #here num is the number of cryptos being sold
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
