import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

cursor = mydb.cursor()

cursor.execute("USE laplateforme")

cursor.execute("SELECT capacite FROM salle")

total = 0
for x in cursor.fetchall():
    total += x[0]

print(f"La capacité de toutes les salles est de : {total}")