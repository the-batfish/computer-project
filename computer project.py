import mysql.connector
from mysql.connector import errorcode
import datetime
from time import sleep
import getpass
import matplotlib.pyplot as plt

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

def login_register():    
    print('''
        Enter your choice:
        1. login
        2. register
        ''')
    choice = int(input('Enter your choice here: '))
    if choice == 1:
        user = input('Username :')
        passw = getpass.getpass("Password: ")
        cnx, cursor = make_connection()
        query = 'SELECT password from economy_data where username = %s'
        cursor.execute(query,(user,))
        realpass = cursor.fetchone()
        if realpass == None:
            print("Wrong username/password")
            cnx.close()
            return False , user
        elif realpass[0] == passw:
            print('Login Successful!')
            cnx.close()
            return True , user
        else:
            print("Wrong username/password")
            cnx.close()
            return False , user
    elif choice == 2:
        cnx, cursor = make_connection()
        try: 
            while True:
                user = input('Username :')
                passw1 = getpass.getpass("Password: ")
                passw2 = getpass.getpass("Confirm Password: ")
                if passw1 == passw2:
                    break
                else:
                    print('Wrong password. Try again!')
            cursor.execute('INSERT INTO economy_data(username , password) VALUES (%s , %s)' , (user , passw1))
            cnx.commit()
            cnx.close()
            print('Account has been succesfully created!')
            return True, user
        except mysql.connector.IntegrityError:
            print("Account already exists")
            return False, user

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
    for i in currencies:
        cnx, cursor = make_connection()
        cursor.execute(f'SELECT {i} , date FROM {i} ORDER BY date ASC')
        results = cursor.fetchall()
        xvalues = []
        yvalues = []
        for j in range(0,len(results)):
            xvalues.append(results[j][1])
        for k in range(0,len(results)):
            yvalues.append(results[k][0])
        plt.plot(xvalues,yvalues, label = i)
        plt.legend(currencies)
        plt.ylabel('EXCHANGE RATE')
        plt.xlabel('DATE')
        cnx.close()
    plt.show()

#this function is for showing the balance in your account
def balance(username):
    cnx, cursor = make_connection()
    query = "SELECT money , botcoin , esterium , binguscoin , floppacoin FROM economy_data WHERE username = %s" 
    cursor.execute(query,(username,))
    results = cursor.fetchone()
    print('You have',results[0],'$ in your account')
    print('You have',results[1],'botcoins in your account')
    print('You have',results[2],'esterium in your account')
    print('You have',results[3],'binguscoin in your account')
    print('You have',results[4],'floppacoin in your account')
    cnx.close()

#this function is for obtaining the current exchange rate for buying and selling
def exchange_rate(currency):
    cnx, cursor = make_connection()
    cursor.execute(f'SELECT {currency} FROM {currency} ORDER BY date DESC LIMIT 1')
    result = cursor.fetchone()[0]
    cnx.close()
    return result

#this function is for buying crypto
def buy_crypto(num , username , currency): #here num is the number of cryptos being requested to buy
    cnx, cursor = make_connection()
    exch = exchange_rate(currency)
    cost = num * exch
    query = f"SELECT {currency} , money FROM economy_data WHERE username = %s" 
    cursor.execute(query,(username,)) 
    values = cursor.fetchone()
    available_crypto = values[0]
    available_money = values[1]
    if cost <= available_money:
        new_balance = available_money - cost
        new_crypto_balance = available_crypto + num
        command = f"UPDATE economy_data SET {currency} = %s , money = %s WHERE username = %s"
        values =  (new_crypto_balance , new_balance , username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        print('Transaction was completely successful')
        print(f'{num} {currency}s have been added to your account')
    else:
        cnx.close()
        print('Sorry transaction was unsuccessful due to limited funds')

#this function is for buying crypto
def sell_crypto(num , username , currency): #here num is the number of cryptos being sold
    cnx, cursor = make_connection()
    exch = exchange_rate()
    sale = num * exch
    query = f"SELECT {currency}, money FROM economy_data WHERE username = %s" 
    cursor.execute(query,(username,)) 
    values = cursor.fetchone()
    available_crypto = values[0]
    available_money = values[1]
    if num <= available_crypto:
        new_balance = available_money + sale
        new_crypto_balance = available_crypto - num
        command = f"UPDATE economy_data SET {currency} = %s , money = %s WHERE username = %s"
        values =  (new_crypto_balance , new_balance , username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        print('Transaction was completely successful')
        print(sale,'$ have been added to your account')
    else:
        cnx.close()
        print('Sorry transaction was unsuccessful due to limited funds')

a,username = login_register()
if a == False:
    print('bruh')
else:
    while True:
        print('''
       1. Balance
       2. Show Exchange Rate
       3. Buy Crypto
       4. Sell Crypto
       0. Exit
    ''')
        choice = int(input('Enter your choice :'))
        if choice == 0:
            break
        elif choice == 1:
            balance(username)
        elif choice == 2:
            show_exchange_rate()
        elif choice == 3:
            while True:
                cryptochoice1 = int(input('''
                enter your choice of crypto currency:
                1. botcoin
                2. esterium
                3. binguscoin
                4. floppacoin
                '''))
                if cryptochoice1 == 1:
                    crypto1 = 'botcoin'
                    break
                elif cryptochoice1 ==2:
                    crypto1 = 'esterium'
                    break
                elif cryptochoice1 == 3:
                    crypto1 = 'binguscoin'
                    break
                elif cryptochoice1 == 4:
                    crypto1 = 'floppacoin'
                    break
                else:
                    print('Enter a valid option!')

            buy_amount = int(input('Enter the number of cryptos you want to buy: '))
            if buy_amount > 0:
                buy_crypto(buy_amount,username, crypto1)
            else:
                print('Enter a proper value!')
        elif choice == 4:
            while True:
                cryptochoice2 = int(input('''
                enter your choice of crypto currency:
                1. botcoin
                2. esterium
                3. binguscoin
                4. floppacoin
                '''))
                if cryptochoice2 == 1:
                    crypto2 = 'botcoin'
                    break
                elif cryptochoice2 ==2:
                    crypto2 = 'esterium'
                    break
                elif cryptochoice2 == 3:
                    crypto2 = 'binguscoin'
                    break
                elif cryptochoice2 == 4:
                    crypto2 = 'floppacoin'
                    break
                else:
                    print('Enter a valid option!')

            sell_amount = int(input('Enter the number of cryptos you want to buy: '))

            if sell_amount > 0:
                sell_crypto(sell_amount,username. crypto2)
            else:
                print('Enter a proper value!')  