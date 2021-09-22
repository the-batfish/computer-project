import codecs
import json
import pickle
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import errorcode
import datetime

currencies = ["botcoin", "esterium", "binguscoin", "floppacoin"]

with open("data.dat", "rb") as f:
    data = pickle.load(f).replace("'", '"')
    dbconfig = json.loads(codecs.decode(data, "rot13", "strict"))

def make_connection():
    try:
        cnx = mysql.connector.connect(
            pool_name="mypool",
            pool_size=2,
            **dbconfig
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
        query = "SELECT password from economy_data where username = %s"
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
                "INSERT INTO economy_data(username , password) VALUES (%s , %s)",
                (username, password),
            )
            cnx.commit()
            cnx.close()
            return True, username
        except mysql.connector.IntegrityError:
            return False, username


def del_account(username, password):
    cnx, cursor = make_connection()
    query = "SELECT password from economy_data where username = %s"
    cursor.execute(query, (username,))
    truepass = cursor.fetchone()[0]
    if password == truepass:
        query2 = "DELETE FROM economy_data WHERE username = %s"
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
    cursor.execute(
        f"SELECT {currency} , dates FROM {currency} ORDER BY dates DESC LIMIT 10"
    )

    results = cursor.fetchall()[::-1]
    xvalues1 = []
    xvalues = []
    yvalues = []
    for j in range(0, len(results)):
        xvalues1.append(results[j][1])

    for b in range(len(xvalues1) - 10, len(xvalues1)):
        xvalues.append(xvalues1[b][5:16])

    for k in range(0, len(results)):
        yvalues.append(results[k][0])

    plt.xticks(rotation=45)
    plt.plot(xvalues, yvalues)
    plt.legend((currency,))
    plt.xlabel("DATE")
    plt.ylabel("EXCHANGE RATE")
    cnx.close()
    plt.show()


# this function is for showing the balance in your account


def balance(username):
    cnx, cursor = make_connection()
    query = "SELECT money , botcoin , esterium , binguscoin , floppacoin , beans FROM economy_data WHERE username = %s"
    cursor.execute(query, (username,))
    results = cursor.fetchone()
    cnx.close()
    return results


# this function is for obtaining the current exchange rate for buying and selling


def exchange_rate(currency):
    cnx, cursor = make_connection()
    cursor.execute(f"SELECT {currency} FROM {currency} ORDER BY dates DESC LIMIT 1")
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
        command = (
            f"UPDATE economy_data SET {currency} = %s , money = %s WHERE username = %s"
        )
        values = (new_crypto_balance, new_balance, username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        return True
    else:
        cnx.close()
        return False


# this function is for buying crypto


def sell_crypto(
    num, username, currency
):  # here num is the number of cryptos being sold
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
        command = (
            f"UPDATE economy_data SET {currency} = %s , money = %s WHERE username = %s"
        )
        values = (new_crypto_balance, new_balance, username)
        cursor.execute(command, values)
        cnx.commit()
        cnx.close()
        return True
    else:
        cnx.close()
        return False

#for showing the next reset timer
def exch_time(currency):
    cnx, cursor = make_connection()
    cursor.execute(f"SELECT dates FROM {currency} ORDER BY dates DESC LIMIT 1")
    result = cursor.fetchone()[0] + datetime.timedelta(minutes = 10) + datetime.timedelta(seconds = 3)
    cnx.close()
    return result

def main():
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    a, username = login_register(username, password, "Log In")
    if a == True:
        while True:
            print(
                """
        1. Balance
        2. Show Exchange Rate
        3. Buy Crypto
        4. Sell Crypto
        5. Delete account
        0. Exit
        """
            )
            choice = int(input("Enter your choice: "))
            if choice == 0:
                break
            elif choice == 1:
                balance(username)
            elif choice == 2:
                show_exchange_rate("botcoin")
            elif choice == 3:
                while True:
                    cryptochoice1 = int(
                        input(
                            """
                    1. botcoin
                    2. esterium
                    3. binguscoin
                    4. floppacoin
                    enter your choice of cryptocurrency here: 
                    """
                        )
                    )
                    if cryptochoice1 == 1:
                        crypto1 = "botcoin"
                        break
                    elif cryptochoice1 == 2:
                        crypto1 = "esterium"
                        break
                    elif cryptochoice1 == 3:
                        crypto1 = "binguscoin"
                        break
                    elif cryptochoice1 == 4:
                        crypto1 = "floppacoin"
                        break
                    else:
                        print("Enter a valid option!")

                buy_amount = int(input("Enter the number of cryptos you want to buy: "))
                if buy_amount > 0:
                    buy_crypto(buy_amount, username, crypto1)
                else:
                    print("Enter a proper value!")
            elif choice == 4:
                while True:
                    cryptochoice2 = int(
                        input(
                            """
                    1. botcoin
                    2. esterium
                    3. binguscoin
                    4. floppacoin
                    enter your choice of cryptocurrency here: """
                        )
                    )
                    if cryptochoice2 == 1:
                        crypto2 = "botcoin"
                        break
                    elif cryptochoice2 == 2:
                        crypto2 = "esterium"
                        break
                    elif cryptochoice2 == 3:
                        crypto2 = "binguscoin"
                        break
                    elif cryptochoice2 == 4:
                        crypto2 = "floppacoin"
                        break
                    else:
                        print("Enter a valid option!")

                sell_amount = int(
                    input("Enter the number of cryptos you want to sell: ")
                )

                if sell_amount > 0:
                    sell_crypto(sell_amount, username, crypto2)
                else:
                    print("Enter a proper value!")
            elif choice == 5:
                if del_account(username) == True:
                    break


if __name__ == "__main__":
    main()
