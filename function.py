import sqlite3
import config
import re
import hashlib


def check_file_exist(File):
    try:
        f = open(File)
    except IOError:
        open(config.DATABASE, 'a').close()
        return 1
    finally:
        return 1


def get_connection():
    connection = sqlite3.connect(config.DATABASE)
    return connection


def init_database():
    if (check_file_exist(config.DATABASE)):
        query = "CREATE TABLE IF NOT EXISTS Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT NOT NULL UNIQUE, EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL UNIQUE)"
        conn = get_connection()
        conn.cursor().execute(query)
        conn.commit()


def check_username_duplicate(username):
    query = "SELECT USERNAME FROM Users WHERE USERNAME = :username"
    conn = get_connection()
    c = conn.cursor().execute(query, {'username': username})
    for row in c:
        if (row is not None):
            return "Duplicate"
    return "None"


def check_email_duplicate(email):
    query = "SELECT EMAIL FROM Users WHERE EMAIL = :email"
    conn = get_connection()
    c = conn.cursor().execute(query, {'email': email})
    for row in c:
        if (row is not None):
            return "Duplicate"
    return "None"


def parameter_policy(parameter, regex):
    if (re.match(regex,parameter) is not None):
        return "Match"
    else:
        return "Not match"


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def insert_user(username, email, password):
    query = "INSERT INTO Users(USERNAME, EMAIL, PASSWORD) VALUES (:username, :email, :password)"
    conn = get_connection()
    conn.cursor().execute(query, {'username': username, 'email': email, 'password': password})
    conn.commit()


def select_user(username_or_email):
    query = "SELECT * FROM Users WHERE EMAIL = :username_or_email OR USERNAME = :username_or_email"
    conn = get_connection()
    c = conn.cursor().execute(query, {'username_or_email': username_or_email})
    for row in c:
        if (row is not None):
            return row[3]
    return "Not existed"


def register(username, email, password, confirm_password):
    if (parameter_policy(username, config.USERNAME_POLICY) == "Match"):
        if (parameter_policy(email, config.EMAIL_POLICY)) == "Match":
            if (check_username_duplicate(username) != "Duplicate"):
                if (check_email_duplicate(email) != "Duplicate"):
                    if (hash_password(password) == hash_password(confirm_password)):
                        insert_user(username, email, hash_password(password))
                        result = {"code": 200, "result": "Created user"}
                    else:
                        result = {"code": 500, "result": "2 password not the same"}
                else:
                    result = {"code": 500, "result": "Email Duplicate"}
            else:
                result = {"code": 500, "result": "Username Duplicate"}
        else:
            result = {"code": 500, "result": "Invalidate Email"}
    else:
        result = {"code": 500, "result": "Invalidate Username"}
    return result


def login(username_or_email, password):
    result = select_user(username_or_email)
    if (hash_password(password) == result):
        result = {"code": 200, "result": "Login successfully"}
    else:
        result = {"code": 500, "result": "Check your account and login again"}
    return result
