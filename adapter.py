import json
import mysql.connector
import model

# Etape 1: Etablir une connexion vers la base de données

db_config = { 'host': 'localhost', 'user': 'root', 'password': '', 'database': 'fouille_données' }
conn = mysql.connector.connect(**db_config)

cursor = conn.cursor()




cursor.execute("SELECT Utilisateur, Date, Heure, Titre, Attribut FROM transition")

# Récupération des données et création d'instances de la classe Action
actions = []
for row in cursor.fetchall():
    user, date, heure, titre, attribut = row
    actionDetails = {}
    if(attribut != ""):
        attributs = attribut.split(",")
        for detail in attributs:
            details = detail.split("=")
            if(len(details) == 1):
                actionDetails[details[0]] = ""
            else:
                actionDetails[details[0]] = details[1]
    action = model.Action(user, date,heure , titre, actionDetails)
    actions.append(action)


conn.close()

'''
#print pour le test
for action in actions:
    print(f"User: {action.user}, Date: {action.date}, ActionType: {action.actionType}")
    print("ActionDetails:", action.actionDetails)
    print()
'''

# Etape 2: sauvegarder les actions dans un fichier json
with open('actions.json', 'w') as f:
    for action in actions:
        action.date = str(action.date)
        action.heure = str(action.heure)
    json.dump(actions, f, default=lambda o: o.__dict__, indent=4)