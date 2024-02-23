import sqlite3

conn = sqlite3.connect("database.db")

"""
    mot de passe pour les testes :
    1)maxime : hehe
    2)alux : hihi
    3)methaphore : muumoo
"""

def menu_principal():
    print("ajouter un utilisateur(1) \nse connecter(2)")
    try:
        choix = int(input())
        if choix == 1:
            ajouter_utilisateur()
        elif choix == 2:
            afficher_users()
            print("quel utilisateur? (id)")
            try:
                utilisateurID = int(input())
                loging(utilisateurID)
                return menu_utilisateur(utilisateurID)
            except ValueError:
                print("rentrez l'id de l'utilisateur")
                return menu_principal()
        else:
            print("entrez 1 ou 2")
            return menu_principal()
    except ValueError:
        print("rentrez 1 ou 2")
        return menu_principal()


def ajouter_utilisateur():
    curr = conn.cursor()
    print("nom de l'utilisateur :")
    nom = str(input())
    print("mot de passe de l'utilisateur :")
    mdp = str(input())
    if mdp =="":
        curr.execute(f"INSERT INTO Users (UserName) VALUES ('{nom}')")
    else:
        curr.execute(f"INSERT INTO Users (UserName, UserPassword) VALUES ('{nom}', '{mdp}')")
    conn.commit()
    print(f"utilisateur {nom} ajouté")
    curr.close
    return menu_principal()


def afficher_users():
    cur = conn.cursor()
    cur.execute("SELECT UserID, UserName FROM Users")
    liste = cur.fetchall()
    for i in liste:
        print(i)
    cur.close()


def loging(utilisateurId):
    cur = conn.cursor()
    cur.execute(f"SELECT UserPassword FROM Users WHERE UserID = {utilisateurId}")
    password = cur.fetchall()[0][0]
    if password == None:
        print("pas de mot de passe")
        cur.close
        return None
    wordinput = str(input("mot de passe? ('retour' pour changer d'utilisateur)\n"))
    if wordinput == "retour":
        cur.close()
        menu_principal()
    elif wordinput == password:
        cur.close()
        return None
    else:
        print("mauvais mot de passe")
        cur.close()
        loging(utilisateurId)



def menu_utilisateur(utilisateurID):
    
    print(
        "que voulez vous faire ? \n1)déconnecter \n2)ajouter \n3)consulter \n4)supprimer \n5)changer mdp"
    )
    try:
        ordre = int(input())
    except ValueError:
        print("option inexistente")
        return menu_utilisateur(utilisateurID)
    
    if ordre == 1:
        print("déconnection")
        return menu_principal()
    
    elif ordre == 2:
        table = selection_table(utilisateurID)
        ajouter_elements(table, utilisateurID)
        return menu_utilisateur(utilisateurID)
    
    elif ordre == 3:
        table = selection_table(utilisateurID)
        afficher_attributs(table, utilisateurID)
        return menu_utilisateur(utilisateurID)
    
    elif ordre == 4:
        table = selection_table(utilisateurID)
        supprimer_elements(table, utilisateurID)
        return menu_utilisateur(utilisateurID)
    
    elif ordre == 5:
        changer_mpd_user(utilisateurID)
        return menu_utilisateur(utilisateurID)

    else:
        print("option inexistente")
        return menu_utilisateur(utilisateurID)
        
        

def selection_table(utilisateurId):
    print("liste des catégories :")
    tablesdispo = "-Abonnement\n-Administratif\n-MDP"
    print(tablesdispo)
    print("avec quelle table interagire ? (retour pour changer d'action)")
    table = str(input())
    
    if table == "retour":
        return menu_utilisateur(utilisateurId)
    
    if table not in tablesdispo:
        print("catégorie inexistente")
        selection_table()
        
    else :
        return table
    
    

def afficher_attributs(table, utilisateurID):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cur.fetchall()][1:]
    print(columns)
    columns_str = ", ".join([f"{table}.{column}" for column in columns])
    cur.execute(
        f"SELECT {columns_str} FROM {table} JOIN Users ON Users.UserID = {table}.UserID WHERE Users.UserID = {utilisateurID};"
    )
    liste = cur.fetchall()
    for i in liste:
        print(i)
    cur.close()

def changer_mpd_user(utilisateurID):
    curr = conn.cursor()
    mdp_actuelle = curr.execute(
        f"SELECT UserPassword FROM Users WHERE UserID ={utilisateurID}"
    )
    mdp_actuelle = curr.fetchall()
    print("le mot de passe actuelle est", mdp_actuelle[0][0])
    print("entrer de nouveau mot de passe")
    nouveau_mdp = input()
    curr.execute(
        f"UPDATE Users SET UserPassword = '{nouveau_mdp}' WHERE UserID = {utilisateurID}"
    )
    conn.commit()
    print("mot de passe mis a jour pour", nouveau_mdp)
    curr.close()



def ajouter_elements(table, utilisateurID):
    cur = conn.cursor()
    
    cur.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cur.fetchall()][1:]  
 
    valeurs_element = {}

    for colonne in columns:
        valeur = input(f"Entrez la valeur pour {colonne}: ")
        valeurs_element[colonne] = valeur
    valeurs_element['UserID'] = utilisateurID

    colonnes_str = ", ".join(valeurs_element.keys())
    valeurs_str = ", ".join([f"'{valeur}'" for valeur in valeurs_element.values()])
    
    
    cur.execute(f"INSERT INTO {table} ({colonnes_str}) VALUES ({valeurs_str})")
    conn.commit()
    print("Élément ajouté avec succès.")
    cur.close()



def supprimer_elements(table, utilisateurID):
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cur.fetchall()][1:]
    afficher_attributs(table, utilisateurID)
    for i in range(len(columns)):
        print(f"{i+1}. {columns[i]}")
    
    choix_colonne = input("a partir de quelle collone supprimer ")
    try:
        choix_colonne = int(choix_colonne)
        
        if choix_colonne < 1 or choix_colonne > len(columns):
            raise ValueError("Numéro de colonne invalide.")
        colonne = columns[choix_colonne - 1]
        
        
    except (ValueError, IndexError):
        print("Numéro de colonne invalide.")
        return supprimer_elements(table, utilisateurID)
    
    valeur = input(f"que chercher dans la colonne '{colonne}' ('annuler' pour annuler) ")
    if valeur == " annuler" :
        print("annulation")
        return
    
    try:
        cur.execute(f"DELETE FROM {table} WHERE {colonne} = '{valeur}'")
    except :
        print(f"l'élément {valeur} n'existe pas dans la colonne {colonne}.")
        return supprimer_elements(table, utilisateurID)
    conn.commit()
    print(f"les lignes contenant l'element {valeur} dans la colonne {colonne} ont été supprimé.")
    
    cur.close()


menu_principal()