import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

cursor = mydb.cursor()

cursor.execute("USE laplateforme")

cursor.execute("SELECT superficie FROM etage")

total = 0
for x in cursor.fetchall():
    total += x[0]

print(f"La superficie de La Plateforme est de {total} m²")