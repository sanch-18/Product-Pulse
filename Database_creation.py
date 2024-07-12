# Install Mysql on your computer
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python 

import mysql.connector as sql

dataBase = sql.connect(host = 'localhost', user = 'root', passwd = 'sancho7039')

# # prepare a cursor object
# cursorObject = dataBase.cursor()

# # Create a database
# cursorObject.execute("CREATE DATABASE E-Commerce")

# print("All Done!")