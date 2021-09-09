import codecs
import json
import pickle
import datetime
import threading
from time import sleep
import matplotlib.pyplot as plt
import mplfinance as mpl
import mysql.connector
from mysql.connector import errorcode

currencies = ['botcoin', 'esterium', 'binguscoin', 'floppacoin']

with open('data.dat','rb') as f:
    dat = pickle.load(f).replace("'",'"')
    data =  json.loads(codecs.decode(dat, "rot13", "strict"))

def make_connection():
    try:
        cnx = mysql.connector.connect(
            host = data['host'],
            user=data['user'],
            password=data['password'],
            database=data['database']
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return cnx, cnx.cursor()


def login_register(username, password, choice="Register"):
    if choice == "Log In":
        cnx, cursor = make_connection()
        query = 'SELECT password from economy_data where username = %s'
        cursor.execute(query, (username,))
        realpass = cursor.fetchone()
        if realpass == None:
            cnx.close()
            return False, username
        elif realpass[0] == password:
            cnx.close()
            return True, username
        else:
            cnx.close()
            return False, username
    elif choice == "Register":
        cnx, cursor = make_connection()
        try:
            cursor.execute(
                'INSERT INTO economy_data(username , password) VALUES (%s , %s)', (username, password))
            cnx.commit()
            cnx.close()
            return True, username
        except mysql.connector.IntegrityError:
            return False, username


def del_account(username, password):
    cnx, cursor = make_connection()
    query = 'SELECT password from economy_data where username = %s'
    cursor.execute(query, (username,))
    truepass = cursor.fetchone()[0]
    if password == truepass:
        query2 = 'DELETE FROM economy_data WHERE username = %s'
        cursor.execute(query2, (username,))
        cnx.commit()
        cnx.close()
        return True
    else:
        cnx.close()
        return False

# this function is for displaying the current and previous exchange rates


def show_exchange_rate(currency):

    cnx, cursor = make_connection()
    cursor.execute(f'SELECT {currency} , date FROM {currency} ORDER BY date ASC')
    results = cursor.fetchall()
    ohlc = []
    xvalues = []
    yvalues = []
    for j in range(0, len(results)):
        xvalues.append(results[j][1])
    for k in range(0, len(results)):
        yvalues.append(results[k][0])

    plt.plot(label=currency)
    bruh = []
    for i in range(1, len(xvalues)+1):
        bruh.append(i)
    plt.xticks(bruh,xvalues)
    plt.legend(currencies)
    plt.xlabel('DATE')
    plt.ylabel('EXCHANGE RATE')
    cnx.close()



    for i in range(1,len(yvalues)):
 
        plt.vlines(x = i, ymin = yvalues[i-1], ymax = yvalues[i], color = 'black', linewidth = 0)
        
        if yvalues[i-1] < yvalues[i]:
            plt.vlines(x = i, ymin = yvalues[i - 1], ymax = yvalues[i], color = 'green', linewidth = 4)
        
        elif yvalues[i-1] > yvalues[i]:
            plt.vlines(x = i, ymin = yvalues[i - 1], ymax = yvalues[i], color = 'red', linewidth = 4)  
            
        if yvalues[i-1] == yvalues[i]:
            plt.vlines(x = i, ymin = yvalues[i -1], ymax = yvalues[i] + 0.1, color = 'black', linewidth = 10)  
          
    plt.show()

# this function is for showing the balance in your account


def balance(username):
    cnx, cursor = make_connection()
    query = "SELECT money , botcoin , esterium , binguscoin , floppacoin FROM economy_data WHERE username = %s"
    cursor.execute(query, (username,))
    results = cursor.fetchone()
    cnx.close()
    return results

# this function is for obtaining the current exchange rate for buying and selling


def exchange_rate(currency):
    cnx, cursor = make_connection()
    cursor.execute(
        f'SELECT {currency} FROM {currency} ORDER BY date DESC LIMIT 1')
    result = cursor.fetchone()[0]
    cnx.close()
    return result

# this function is for buying crypto


# here num is the number of cryptos being requested to buy
def buy_crypto(num, username, currency):
    cnx, cursor = make_connection()
    exch = exchange_rate(currency)
    cost = num * exch
    query = f"SELECT {currency} , money FROM economy_data WHERE username = %s"
    cursor.execute(query, (username,))
    values = cursor.fetchone()
    available_crypto = values[0]
    available_money = values[1]
    if cost <= available_money:
        new_balance = available_money - cost
        new_crypto_balance = available_crypto + num
        command = f"UPDATE economy_data SET {currency} = %s , money = %s WHERE username = %s"
        values = (new_crypto_balance, new_balance, username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        return True
    else:
        return False

# this function is for buying crypto


def sell_crypto(num, username, currency):  # here num is the number of cryptos being sold
    cnx, cursor = make_connection()
    exch = exchange_rate(currency)
    sale = num * exch
    query = f"SELECT {currency}, money FROM economy_data WHERE username = %s"
    cursor.execute(query, (username,))
    values = cursor.fetchone()
    available_crypto = values[0]
    available_money = values[1]
    if num <= available_crypto:
        new_balance = available_money + sale
        new_crypto_balance = available_crypto - num
        command = f"UPDATE economy_data SET {currency} = %s , money = %s WHERE username = %s"
        values = (new_crypto_balance, new_balance, username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        return True
    else:
        cnx.close()
        return False


def exch_r8_refresh(currency):
    cnx, cursor = make_connection()
    query1 = f"SELECT {currency} , ratio FROM {currency} ORDER BY date DESC LIMIT 1"
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
            cursor.execute(f"SELECT date FROM {i} ORDER BY date DESC LIMIT 1")
            results = cursor.fetchone()[0]
            dt = datetime.datetime.strptime(results, '%Y-%m-%d')
            if datetime.datetime.now() >= (dt + datetime.timedelta(days=1)):
                curr_exch_r8, ratio = exch_r8_refresh(i)
                query = f"INSERT INTO {i}(date, {i} , ratio) VALUES(%s,%s,%s)"
                cursor.execute(query, (datetime.datetime.now().strftime(
                    '%Y-%m-%d'), curr_exch_r8, ratio))
                cnx.commit()
                sleep(5)
            cnx.close()


exch_r8_loop = threading.Thread(target=exch_r8_loop, daemon=True)
exch_r8_loop.start()

def main():
    username = input('Enter the username: ')
    password = input('Enter the password: ')
    a, username = login_register(username,password,"Log In")
    if a == True:
        while True:
            print('''
        1. Balance
        2. Show Exchange Rate
        3. Buy Crypto
        4. Sell Crypto
        5. Delete account
        0. Exit
        ''')
            choice = int(input('Enter your choice: '))
            if choice == 0:
                break
            elif choice == 1:
                balance(username)
            elif choice == 2:
                show_exchange_rate('botcoin')
            elif choice == 3:
                while True:
                    cryptochoice1 = int(input('''
                    1. botcoin
                    2. esterium
                    3. binguscoin
                    4. floppacoin
                    enter your choice of cryptocurrency here: 
                    '''))
                    if cryptochoice1 == 1:
                        crypto1 = 'botcoin'
                        break
                    elif cryptochoice1 == 2:
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

                buy_amount = int(
                    input('Enter the number of cryptos you want to buy: '))
                if buy_amount > 0:
                    buy_crypto(buy_amount, username, crypto1)
                else:
                    print('Enter a proper value!')
            elif choice == 4:
                while True:
                    cryptochoice2 = int(input('''
                    1. botcoin
                    2. esterium
                    3. binguscoin
                    4. floppacoin
                    enter your choice of cryptocurrency here: '''
                                            ))
                    if cryptochoice2 == 1:
                        crypto2 = 'botcoin'
                        break
                    elif cryptochoice2 == 2:
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

                sell_amount = int(
                    input('Enter the number of cryptos you want to sell: '))

                if sell_amount > 0:
                    sell_crypto(sell_amount, username, crypto2)
                else:
                    print('Enter a proper value!')
            elif choice == 5:
                if del_account(username) == True:
                    break

if __name__ == "__main__":
    main()