import mysql.connector
import json

# Optimize this import statement, maybe put db in its own file???
with open('credentials.json', 'r') as file:
    credentials = json.load(file)

db = mysql.connector.connect(
        host=credentials['database']['host'],
        user=credentials['database']['user'],
        passwd=credentials['database']['password'],
        database=credentials['database']['database']
    )

