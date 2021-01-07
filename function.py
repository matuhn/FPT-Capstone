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
    try:
        if (check_file_exist(config.DATABASE)):
            query = "CREATE TABLE IF NOT EXISTS Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT NOT NULL UNIQUE, EMAIL TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL UNIQUE)"
            conn = get_connection()
            conn.cursor().execute(query)
            conn.commit()
    except:
        print("Bug when init db")


def check_username_duplicate(username):
    try:
        query = "SELECT USERNAME FROM Users WHERE USERNAME = :username"
        conn = get_connection()
        c = conn.cursor().execute(query, {'username': username})
        for row in c:
            if (row is not None):
                return "Duplicate"
        return "None"
    except:
        print("Bug when check_username_dup")


def check_email_duplicate(email):
    try:
        query = "SELECT EMAIL FROM Users WHERE EMAIL = :email"
        conn = get_connection()
        c = conn.cursor().execute(query, {'email': email})
        for row in c:
            if (row is not None):
                return "Duplicate"
        return "None"
    except:
        print("Bug when check email")


def parameter_policy(parameter, regex):
    try:
        if (re.match(regex,parameter) is not None):
            return "Match"
        else:
            return "Not match"
    except:
        print("Bug in policy regex")


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def insert_user(username, email, password):
    try:
        query = "INSERT INTO Users(USERNAME, EMAIL, PASSWORD) VALUES (:username, :email, :password)"
        conn = get_connection()
        conn.cursor().execute(query, {'username': username, 'email': email, 'password': password})
        conn.commit()
    except:
        print("insert buggy")


def select_user(username_or_email):
    try:
        query = "SELECT ID,USERNAME,EMAIL,PASSWORD FROM Users WHERE EMAIL = :username_or_email OR USERNAME = :username_or_email"
        conn = get_connection()
        c = conn.cursor().execute(query, {'username_or_email': username_or_email})
        for row in c:
            if (row is not None):
                return row
        return "Not existed"
    except:
        print("Select never bug")


def register(username, email, password):
    try:
        if (parameter_policy(username, config.USERNAME_POLICY) == "Match"):
            if (parameter_policy(email, config.EMAIL_POLICY)) == "Match":
                if (check_username_duplicate(username) != "Duplicate"):
                    if (check_email_duplicate(email) != "Duplicate"):
                        insert_user(username, email, hash_password(password))
                        result = {"code": 200, "result": "Created user"}
                    else:
                        result = {"code": 500, "result": "Email Duplicate"}
                else:
                    result = {"code": 500, "result": "Username Duplicate"}
            else:
                result = {"code": 500, "result": "Invalidate Email"}
        else:
            result = {"code": 500, "result": "Invalidate Username"}
    except:
        result = {"code": 500, "result": "Server Error"}
    return result


def login(username_or_email, password):
    try:
        result = select_user(username_or_email)[3]
        if (hash_password(password) == result):
            result = {"code": 200, "result": "Login successfully"}
        else:
            result = {"code": 500, "result": "Check your account and login again"}
        return result
    except:
        result = {"code": 500, "result": "Server Error"}
    return result
