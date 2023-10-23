import json
import mysql.connector
import model

# Etape 1: Etablir une connexion vers la base de données

db_config = { 'host': 'localhost', 'user': 'root', 'password': '', 'database': 'fouille_données' }
conn = mysql.connector.connect(**db_config)

cursor = conn.cursor()




cursor.execute("SELECT Utilisateur, Date, Heure, Titre, Delai, RefTran, Commentaire FROM transition")

# Récupération des données et création d'instances de la classe Action
actions = []
for row in cursor.fetchall():
    user, date, heure, titre, delai, reftran, commentaire = row
    actionDetails = {'Delai': delai, 'RefTran': reftran, 'Commentaire': commentaire}
    action = model.Action(user, date, titre, actionDetails)
    actions.append(action)


conn.close()

#print pour le test
for action in actions:
    print(f"User: {action.user}, Date: {action.date}, ActionType: {action.actionType}")
    print("ActionDetails:", action.actionDetails)
    print()


'''
obj = cursor.fetchall()

# Etape 2 :convertir les données en json
dict_obj = { 'key': obj }
json_obj = json.dumps(dict_obj,indent=4, sort_keys=True, default=str)

'''
