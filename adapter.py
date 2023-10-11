import json
import mysql.connector


# Etape 1: Etablir une connexion vers la base de données

db_config = { 'host': 'localhost', 'user': 'root', 'password': '', 'database': 'fouille_données' }
conn = mysql.connector.connect(**db_config)

cursor = conn.cursor()
cursor.execute('SELECT * FROM  TABLE')
obj = cursor.fetchall()

# Etape 2 :convertir les données en json
dict_obj = { 'key': obj }
json_obj = json.dumps(dict_obj)

print(json_obj)