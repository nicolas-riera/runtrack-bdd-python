import mysql.connector
from time import sleep

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

cursor = mydb.cursor()

cursor.execute("USE zoo")

def clear():
    print("\n"*50)

def afficher_tableau(titres, donnees):
    largeurs = []
    for i in range(len(titres)):
        max_col = len(str(titres[i]))
        for ligne in donnees:
            max_col = max(max_col, len(str(ligne[i])))
        largeurs.append(max_col + 2)  

    def ligne_sep():
        print("┌" + "┬".join("─" * l for l in largeurs) + "┐")

    def ligne_sep_milieu():
        print("├" + "┼".join("─" * l for l in largeurs) + "┤")

    def ligne_sep_bas():
        print("└" + "┴".join("─" * l for l in largeurs) + "┘")

    ligne_sep()

    print("│" + "│".join(str(titres[i]).center(largeurs[i]) for i in range(len(titres))) + "│")

    ligne_sep_milieu()

    for ligne in donnees:
        print("│" + "│".join(str(ligne[i]).center(largeurs[i]) for i in range(len(ligne))) + "│")

    ligne_sep_bas()

while True:

    clear()

    print("Zoo :\n")
    print("1. Gérer les animaux\n2. Gérer les cages\n0. Quitter")

    usr_choice = input()

    match usr_choice:

        # Animaux
        case "1":
            clear()
            print("Animaux :\n")
            print("1. Afficher les animaux\n2. Ajouter un animal\n3. Modifier un animal\n4. Supprimer un animal\n0. Retour")

            usr_choice = input()

            match usr_choice:
                case "1":
                    clear()
                    cursor.execute("SELECT * from animal")
                    afficher_tableau(["ID", "Nom", "Race", "ID_Cage", "Date de naissance", "Pays d'origine"], cursor.fetchall())
                    input("\nAppuyez sur Entrée pour revenir en arrière.")
                case "2":
                    clear()
                    name = input("Entrez le nom : ")
                    race = input("Entrez la race : ")
                    is_in_cage = input("Est ce que l'animal est dans une cage (1 pour Oui, 0 pour non) :")
                    if is_in_cage == "1":
                        id_cage = input("Entrez l'ID de la cage : ")
                    date_naissance = input("Entrez la date de naissance (YYYY-MM-DD) : ")
                    pays_origine = input("Entrez le pays d'origine : ")

                    donnees_valides = True

                    if not name or not race or is_in_cage not in ("0", "1") or not pays_origine:
                        donnees_valides = False

                    if is_in_cage == "1":
                        if not id_cage.isdigit():
                            donnees_valides = False

                    parts = date_naissance.split("-")
                    if len(parts) != 3 or not all(p.isdigit() for p in parts):
                        donnees_valides = False
                    else:
                        year, month, day = map(int, parts)
                        if not (1 <= month <= 12 and 1 <= day <= 31):
                            donnees_valides = False

                    if not donnees_valides:
                        print("Les données ne sont pas valides...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    clear()
                    print("Ajout en cours...")
                    if is_in_cage == "1":
                        cursor.execute("INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine) VALUES (%s, %s, %s, %s, %s);", (name, race, id_cage, date_naissance, pays_origine))
                    else :
                        cursor.execute("INSERT INTO animal (nom, race, date_naissance, pays_origine) VALUES (%s, %s, %s, %s);", (name, race, date_naissance, pays_origine))
                    mydb.commit()
                    
                    clear()
                    print("Ajout effectué !")
                    sleep(0.5)
                    input("\nAppuyez sur Entrée pour continuer.")
                    continue
                case "3":
                    
                    clear()

                    cursor.execute("SELECT * from animal")
                    values = cursor.fetchall()
                    afficher_tableau(["ID", "Nom", "Race", "ID_Cage", "Date de naissance", "Pays d'origine"], values)

                    usr_id = input("\nEntrez l'ID de l'animal : ")

                    clear()

                    try:
                        usr_id = int(usr_id)
                    except:
                        print("ID non valide...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    found = False
                    for e in values:
                        if e[0] == usr_id:
                            found = True
                    
                    if not found:
                        print("ID introuvable...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    cursor.execute(f"SELECT * FROM animal WHERE id = {usr_id};")

                    afficher_tableau(["ID", "Nom", "Race", "ID_Cage", "Date de naissance", "Pays d'origine"], cursor.fetchall())

                    print("\n1. Changer le nom\n2. Changer la race\n3. Changer de cage\n4. Changer la date de naissance\n5. Changer le pays d'origine\n0. Retour")

                    usr_choice = input()

                    clear()

                    match usr_choice:
                        case "1":
                            name = input("Entrez le nouveau nom : ")

                            if name:
                                clear()
                                print("Modification en cours...")
                                
                                cursor.execute("UPDATE animal SET nom = %s WHERE id = %s", (name, usr_id))
                                mydb.commit()
                                
                                clear()
                                print("Modification effectuée !")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                            else:
                                print("Entrée vide...")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue

                        case "2":
                            race = input("Entrez la nouvelle race : ")

                            if race:
                                clear()
                                print("Modification en cours...")
                                
                                cursor.execute("UPDATE animal SET race = %s WHERE id = %s", (race, usr_id))
                                mydb.commit()
                                
                                clear()
                                print("Modification effectuée !")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                            else:
                                print("Entrée vide...")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                        case "3":
                            skip_menu = False
                            for e in values:
                                if e[0] == usr_id:
                                    if e[3] == None:
                                        skip_menu = True
                                        break
                            
                            if not skip_menu:
                                print("1. Changer de cage\n2. Sortir d'une cage")

                                usr_choice = input()
                            else:
                                usr_choice = "1"

                            clear()
                            
                            match usr_choice:
                                case "1":

                                    cursor.execute("SELECT * FROM cage")
                                    values_cages_base = cursor.fetchall()
                                    values_cages = []
                                    for line in values_cages_base:
                                        animal_list = []
                                        for animal in values:
                                            if animal[3] == line[0]:
                                                animal_list.append(animal[1])
                                        line = list(line)
                                        if animal_list:
                                            line.append(", ".join(animal_list))
                                        else:
                                            line.append("-")
                                        values_cages.append(line)
                                                                  
                                    afficher_tableau(["ID","Superficie", "Capacité", "Animaux présents"], values_cages)
                            
                                    usr_cage = input("\nEntrez l'ID d'une cage : ")

                                    try :
                                        usr_cage = int(usr_cage)
                                    except:
                                        print("ID non valide...")
                                        sleep(0.5)
                                        input("\nAppuyez sur Entrée pour continuer.")
                                        continue

                                    found = False
                                    full = False
                                    for e in values_cages:
                                        if e[0] == usr_cage:
                                            found = True
                                            nb_in_cage = 0
                                            for i in values:
                                                if i[3] == usr_cage:
                                                    nb_in_cage += 1
                                            if nb_in_cage >= e[2]:
                                                clear()
                                                print("Cage pleine..")
                                                sleep(0.5)
                                                input("\nAppuyez sur Entrée pour continuer.")
                                                full = True
                                                break

                                    if found and not full:
                                        
                                        print("Modification en cours...")
                                        
                                        cursor.execute("UPDATE animal SET id_cage = %s WHERE id = %s", (usr_cage, usr_id))
                                        mydb.commit()
                                        
                                        clear()
                                        print("Modification effectuée !")
                                        sleep(0.5)
                                        input("\nAppuyez sur Entrée pour continuer.")
                                        continue
  
                                    elif not full:
                                        print("ID introuvable...")
                                        sleep(0.5)
                                        input("\nAppuyez sur Entrée pour continuer.")
                                        continue

                                case "2":
                                    print("Modification en cours...")
                                        
                                    cursor.execute("UPDATE animal SET id_cage = %s WHERE id = %s", (None, usr_id))
                                    mydb.commit()
                                    
                                    clear()
                                    print("Modification effectuée !")
                                    sleep(0.5)
                                    input("\nAppuyez sur Entrée pour continuer.")
                                    continue
                                case _:
                                    continue
                            
                        case "4":

                            date_naissance = input("Entrez la nouvelle date de naissance (YYYY-MM-DD) : ")

                            donnees_valides = True
                            parts = date_naissance.split("-")
                            if len(parts) != 3 or not all(p.isdigit() for p in parts):
                                donnees_valides = False
                            else:
                                year, month, day = map(int, parts)
                                if not (1 <= month <= 12 and 1 <= day <= 31):
                                    donnees_valides = False

                            if donnees_valides :
                                clear()
                                print("Modification en cours...")
                                
                                cursor.execute("UPDATE animal SET date_naissance = %s WHERE id = %s", (date_naissance, usr_id))
                                mydb.commit()
                                
                                clear()
                                print("Modification effectuée !")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                            else:
                                print("Entrée vide ou invalide...")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue

                        case "5":
                            text = input("Entrez le nouveau pays d'origine: ")

                            if text:
                                clear()
                                print("Modification en cours...")
                                
                                cursor.execute("UPDATE animal SET pays_origine = %s WHERE id = %s", (text, usr_id))
                                mydb.commit()
                                
                                clear()
                                print("Modification effectuée !")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                            else:
                                print("Entrée vide...")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                        case _:
                            continue
                    

                case "4":

                    cursor.execute("SELECT * from animal")
                    values = cursor.fetchall()
                    afficher_tableau(["ID", "Nom", "Race", "ID_Cage", "Date de naissance", "Pays d'origine"], values)

                    usr_id = input("\nEntrez l'ID de l'animal : ")

                    clear()

                    try:
                        usr_id = int(usr_id)
                    except:
                        print("ID non valide...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    found = False
                    for e in values:
                        if e[0] == usr_id:
                            found = True
                    
                    if not found:
                        print("ID introuvable...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    clear()
                    print("Suppression en cours...")
                    
                    cursor.execute(f"DELETE FROM animal WHERE id = {usr_id}")
                    mydb.commit()
                    
                    clear()
                    print("Suppression effectuée !")
                    sleep(0.5)
                    input("\nAppuyez sur Entrée pour continuer.")
                    continue
                case _:
                    continue

        # Cages      
        case "2":
            clear()
            print("Cages :\n")
            print("1. Afficher les cages\n2. Ajouter une cage\n3. Modifier une cages\n4. Supprimer une cage\n0. Retour")

            usr_choice = input()

            match usr_choice:
                case "1":
                    clear()
                    cursor.execute("SELECT * FROM animal")
                    values = cursor.fetchall()
                    cursor.execute("SELECT * FROM cage")
                    values_cages_base = cursor.fetchall()
                    values_cages = []
                    for line in values_cages_base:
                        animal_list = []
                        for animal in values:
                            if animal[3] == line[0]:
                                animal_list.append(animal[1])
                        line = list(line)
                        if animal_list:
                            line.append(", ".join(animal_list))
                        else:
                            line.append("-")
                        values_cages.append(line)
                                                    
                    afficher_tableau(["ID","Superficie", "Capacité", "Animaux présents"], values_cages)

                    superficie_total = 0
                    for e in values_cages:
                        superficie_total += e[2]

                    print(f"Superficie totale : {superficie_total} m²")
            
                    input("\nAppuyez sur Entrée pour revenir en arrière.")
                case "2":
                    clear()
                    superficie = input("Entrez la superficie : ")
                    capacite = input("Entrez la capicité : ")

                    donnees_valides = True

                    if not superficie or not capacite:
                        donnees_valides = False

                    if not donnees_valides:
                        print("Les données ne sont pas valides...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    clear()
                    print("Ajout en cours...")
                    cursor.execute("INSERT INTO cage (superficie, capacite) VALUES (%s, %s);", (superficie, capacite))
                    mydb.commit()
                    
                    clear()
                    print("Ajout effectué !")
                    sleep(0.5)
                    input("\nAppuyez sur Entrée pour continuer.")
                    continue

                case "3":
                    
                    clear()
                    cursor.execute("SELECT * FROM animal")
                    values = cursor.fetchall()
                    cursor.execute("SELECT * FROM cage")
                    values_cages_base = cursor.fetchall()
                    values_cages = []
                    for line in values_cages_base:
                        animal_list = []
                        for animal in values:
                            if animal[3] == line[0]:
                                animal_list.append(animal[1])
                        line = list(line)
                        if animal_list:
                            line.append(", ".join(animal_list))
                        else:
                            line.append("-")
                        values_cages.append(line)
                                                    
                    afficher_tableau(["ID","Superficie", "Capacité", "Animaux présents"], values_cages)

                    usr_id = input("\nEntrez l'ID de la cage : ")

                    clear()

                    try:
                        usr_id = int(usr_id)
                    except:
                        print("ID non valide...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    found = False
                    for e in values_cages:
                        if e[0] == usr_id:
                            found = True
                    
                    if not found:
                        print("ID introuvable...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    cursor.execute(f"SELECT * FROM cage WHERE id = {usr_id};")

                    values_cage_base = cursor.fetchall()
                    values_cage = []

                    for line in values_cage_base:
                        animal_list = []
                        for animal in values:
                            if animal[3] == line[0]:
                                animal_list.append(animal[1])
                        line = list(line)
                        if animal_list:
                            line.append(", ".join(animal_list))
                        else:
                            line.append("-")
                        values_cage.append(line)

                    afficher_tableau(["ID","Superficie", "Capacité", "Animaux présents"], values_cage)

                    print("\n1. Changer la superficie\n2. Changer la capacité\n3. Vider la cage\n0. Retour")

                    usr_choice = input()

                    clear()

                    match usr_choice:
                        case "1":
                            superficie = input("Entrez la nouvelle superficie : ")

                            if superficie:
                                clear()
                                print("Modification en cours...")
                                
                                cursor.execute("UPDATE cage SET superficie = %s WHERE id = %s", (superficie, usr_id))
                                mydb.commit()
                                
                                clear()
                                print("Modification effectuée !")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                            else:
                                print("Entrée vide...")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue

                        case "2":
                            capacite = input("Entrez la nouvelle capacitée : ")

                            if capacite:
                                clear()
                                print("Modification en cours...")
                                
                                cursor.execute("UPDATE animal SET race = %s WHERE id = %s", (capacite, usr_id))
                                mydb.commit()
                                
                                clear()
                                print("Modification effectuée !")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue
                            else:
                                print("Entrée vide...")
                                sleep(0.5)
                                input("\nAppuyez sur Entrée pour continuer.")
                                continue

                        case "3":
                            clear()
                            print("Modification en cours...")
                            
                            cursor.execute("SELECT * FROM animal")
                            values = cursor.fetchall()
                            for e in values:
                                if e[3] == usr_id:
                                    cursor.execute("UPDATE animal SET id_cage=%s WHERE id=%s", (None, e[0]))
                                
                            mydb.commit()
                                
                            clear()
                            print("Modification effectuée !")
                            sleep(0.5)
                            input("\nAppuyez sur Entrée pour continuer.")
                            continue

                        case _:
                            continue
                    

                case "4":

                    clear()
                    cursor.execute("SELECT * FROM animal")
                    values = cursor.fetchall()
                    cursor.execute("SELECT * FROM cage")
                    values_cages_base = cursor.fetchall()
                    values_cages = []
                    for line in values_cages_base:
                        animal_list = []
                        for animal in values:
                            if animal[3] == line[0]:
                                animal_list.append(animal[1])
                        line = list(line)
                        if animal_list:
                            line.append(", ".join(animal_list))
                        else:
                            line.append("-")
                        values_cages.append(line)
                                                    
                    afficher_tableau(["ID","Superficie", "Capacité", "Animaux présents"], values_cages)

                    usr_id = input("\nEntrez l'ID de la cage : ")

                    clear()

                    try:
                        usr_id = int(usr_id)
                    except:
                        print("ID non valide...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    found = False
                    for e in values_cage:
                        if e[0] == usr_id:
                            found = True
                    
                    if not found:
                        print("ID introuvable...")
                        sleep(0.5)
                        input("\nAppuyez sur Entrée pour continuer.")
                        continue

                    clear()
                    print("Suppression en cours...")
                    
                    cursor.execute(f"DELETE FROM cage WHERE id = {usr_id}")

                    cursor.execute("SELECT * FROM animal")
                    values = cursor.fetchall()
                    for e in values:
                        if e[3] == usr_id:
                            cursor.execute("UPDATE animal SET id_cage=%s WHERE id=%s", (None, e[0]))

                    mydb.commit()
                    
                    clear()
                    print("Suppression effectuée !")
                    sleep(0.5)
                    input("\nAppuyez sur Entrée pour continuer.")
                    continue
                case _:
                    continue
                
        case "0":
            clear()
            print("Au revoir !")
            mydb.commit()
            sleep(2)
            exit() 
        case _:
            continue   

    mydb.commit()