import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user ='root',
    passwd = '1234'
)

#prepare a cursor object
cursorObject = dataBase.cursor()

#create a database
cursorObject.execute("CREATE DATABASE crmDB")

print("All done!")