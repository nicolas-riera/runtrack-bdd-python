import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

cursor = mydb.cursor()

cursor.execute("USE laplateforme")

cursor.execute("SELECT * FROM employe E JOIN service S ON E.id_service = S.id")

for x in cursor.fetchall():
    print(x)

class Employe:
    @staticmethod
    def create_employe(nom, prenom, salaire, id_service):
        cursor.execute("INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s);", (nom, prenom, salaire, id_service))

    @staticmethod
    def read_employe(id):
        cursor.execute(f"SELECT * FROM employe WHERE id = {id};")
        for x in cursor.fetchall():
            print(x)

    @staticmethod
    def update_employe(id, nom=None, prenom=None, salaire=None, id_service=None):
        if nom:
            cursor.execute("UPDATE employe SET nom=%s WHERE id=%s;", (nom, id))
        if prenom:
            cursor.execute("UPDATE employe SET prenom=%s WHERE id=%s;", (prenom, id))
        if salaire:
            cursor.execute("UPDATE employe SET salaire=%s WHERE id=%s;", (salaire, id))
        if id_service:
            cursor.execute("UPDATE employe SET id_service=%s WHERE id=%s;", (id_service, id))

    def delete_employe(id):
        cursor.execute(f"DELETE FROM employe WHERE id = {id}")

# Employe.create_employe("Dupont", "Jean", 1400, 1)

Employe.read_employe(1)

Employe.update_employe(11, nom="Ducon")
Employe.update_employe(11, prenom="Rick")
Employe.update_employe(11, salaire=2800.2)
Employe.update_employe(11, id_service=2)

# Employe.delete_employe(10)

mydb.commit()