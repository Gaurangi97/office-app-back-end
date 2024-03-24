from MySQLdb import MySQLError
from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

import MySQLdb.cursors
import db as db
import api as api


app = Flask(__name__)
mysql = MySQL(app)
CORS(app)

app.secret_key = 'qawsxedrdr'
app.config['MYSQL_HOST'] = '127.0.0.1'  # Change this to your MySQL server host
app.config['MYSQL_USER'] = 'root'  # Change this to your MySQL name
app.config['MYSQL_PASSWORD'] = ''  # Change this to your MySQL password
app.config['MYSQL_DB'] = 'officeapp'

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/api/user', methods=['GET'])
def get_user():
    return api.user(mysql)

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    return api.loginUser(app, mysql)

@app.route('/api/register', methods=['GET', 'POST'])
def register_user():
    return api.registerUser(app, mysql)

@app.route('/api/logout')
def logout():
    return api.logoutUser()
   

def createDataBase():
    try:
        db.create_db(app, mysql)
        print('DataBase created successfully')
    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':
    createDataBase()
    app.run(debug=True, host="0.0.0.0")
