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
\>>> from models.py import app, db
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
$ export FLASK_DEBUG=True
$ export FLASK_APP=models.py"""

"then you can type 'flask run' or 'flask migrate', etc."