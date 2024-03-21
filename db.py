from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, jsonify, request
from flask import Flask, render_template, request, redirect, url_for, session

import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib


def create_db(app, mysql):
    # Create database if not exists
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS `officeapp` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cur.execute("USE `officeapp`;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS `users` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `name` varchar(50) NOT NULL,
                `password` varchar(255) NOT NULL,
                `email` varchar(100) NOT NULL,
                PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
        """)
        mysql.connection.commit()
        cur.close()

def register(app, mysql):
    
    msg = 'Internal server error'
    status_code = 500

    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            status_code = 400

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            status_code = 400

        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers!'
            status_code = 400

        elif not name or not password or not email:
            msg = 'Please fill out the form!'
            status_code = 400

        else:
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (name, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            status_code = 200

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        status_code = 400

    return {'msg': msg, 'status_code': status_code}

def login(app, mysql):
    msg = 'Internal server error'
    status_code = 500
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = %s AND password = %s', (name, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            # Redirect to home page
            msg = 'Logged in successfully!'
            status_code = 200
        else:
            msg = 'Incorrect name/password!'
            status_code = 401
    return {'msg': msg, 'status_code': status_code}

def logout():
    msg = 'Internal server error'
    status_code = 500
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        msg = 'Logout successfully!'
        status_code = 200

        return {'msg': msg, 'status_code': status_code}
    else:
        msg = 'Logout faild!'
        status_code = 200
        return {'msg': msg, 'status_code': status_code}
    
def user(mysql):
    msg = 'Internal server error'
    status_code = 500
    if request.method == 'GET':
        if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT name, email FROM users WHERE id = %s', (session['id'],))
            user = cursor.fetchone()
            status_code = 200
        else:
            status_code = 404
    return {'user': user, 'status_code': status_code}