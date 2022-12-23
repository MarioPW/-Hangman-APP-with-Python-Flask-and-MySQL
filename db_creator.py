"""import mysql.connector

mt = mysql.connector.connect(
    host='localhost',
    user='root',
)

mt_cursor = mt.cursor()
mt_cursor.execute("CREATE DATABASE hangman_users")

mt_cursor.execute("SHOW DATABASE")

for i in mt_cursor:
    print(i)"""

# Comand to make it work
"""
\>>> from db_qsl.py import app, db
\>>> app.app_context().push()
\>>> db.create_all()
\>>> exit()
"""
##### Comand to make it work 2 (in git)  ####
"""
Error: Could not locate a Flask application. Use the 'flask --app' option, 'FLASK_APP' environment variable, or a 'wsgi.py' or 'app.py' file in the current directory.

Usage: flask [OPTIONS] COMMAND [ARGS]...
Try 'flask --help' for help.

Error: No such command 'db'."""

# Solution
'(venv) ...with activated virtual enviroment'
"""
$ export FLASK_ENV=development
$ export FLASK_APP=db_sql.py"""

"then you can type 'flask run' or 'flask migrate', etc."
import random

animals = ["ANTELOPE", "BABOON", "BEAR", "BISON", "BUFFALO", "CAPUCHIN", "CHEETAH", "CHIMPANZEE", "COUGAR", "DEER", "EAGLE", "ELEPHANT", "Echidna", "FALCON", "GAZELLE", "GIRAFFE", "GIBBON", "GORILLA", "HAWK", "HYENA", "JAGUAR", "KANGAROO", "LEMUR", "LEOPARD", "LION", "MACAQUE", "MANDRILL", "MARMOSET", "MOOSE", "OWL", "ORANGUTAN", "PELICAN", "PLATYPUS", "PENGUIN", "RHINOCEROS", "TIGER", "VULTURE", "WALLABY", "WATER BUFFALO", "WOLF", "WOODPECKER", "YAK", "ZEBRA"]

random_animal = random.choice(animals)
print(random_animal)