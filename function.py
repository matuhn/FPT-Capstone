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
            query = "CREATE TABLE IF NOT EXISTS Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT NOT NULL UNIQUE, EMAIL TEXT NOT NULL UNIQUE, FULLNAME TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL)"
            conn = get_connection()
            conn.cursor().execute(query)
            conn.commit()
    except Exception as ex:
        print(ex)


def parameter_policy(parameter, regex):
    try:
        if re.match(regex, parameter) is not None:
            return "Match"
        else:
            return "Not match"
    except Exception as ex:
        print(ex)


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()



