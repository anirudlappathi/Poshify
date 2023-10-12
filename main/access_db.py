# To get password from user
from getpass import getpass
# To connect our Python script to the MySQL DB
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="root",
        password=input("Enter root password: "),
    ) as connection:
        print(connection)
except Error as e:
    print(e)