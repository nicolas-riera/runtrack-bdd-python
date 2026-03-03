import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

cursor = mydb.cursor()

cursor.execute("USE laplateforme")

cursor.execute("SELECT nom, capacite FROM salle ")

for x in cursor.fetchall():
    print(x)