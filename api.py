import db as db
from flask import Flask, jsonify, request

def registerUser(app, mysql):
    try:
        return db.register(app, mysql)

    except Exception as e:
        return e
    
def loginUser(app, mysql):
    try:
        return db.login(app, mysql)

    except Exception as e:
        return e
    
def logoutUser():
    try:
        return db.logout()

    except Exception as e:
        return e
    
def user(mysql):
    try:
        return db.user(mysql)

    except Exception as e:
        return e
    