import sqlite3
import config
import re
import hashlib
from pathlib import Path
import os
from uuid import uuid4
import json


def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"


def check_file_exist(file):
    try:
        open(file)
    except IOError:
        open(config.DATABASE, 'a').close()
        return 1
    finally:
        return 1


def get_connection():
    connection = sqlite3.connect(config.DATABASE)
    return connection


def init_directory(name):
    Path(name).mkdir(parents=True, exist_ok=True)


def init_database():
    try:
        if check_file_exist(config.DATABASE):
            query = "CREATE TABLE IF NOT EXISTS Users " \
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    "USERNAME TEXT NOT NULL UNIQUE, EMAIL TEXT NOT NULL UNIQUE, " \
                    "FULLNAME TEXT NOT NULL UNIQUE, PASSWORD TEXT NOT NULL)"
            conn = get_connection()
            conn.cursor().execute(query)
            query = "CREATE TABLE IF NOT EXISTS FileShare " \
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    "PATH TEXT NOT NULL UNIQUE, DATE TEXT NOT NULL UNIQUE, " \
                    "SHARE TEXT NOT NULL UNIQUE)"
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


def gen_file_name(name, username):
    parent_dir = os.path.join(config.UPLOAD_DIR, hash_password(username))
    init_directory(parent_dir)
    new_name = make_unique(name)
    directory = hash_password(username)
    return os.path.join(parent_dir, new_name), directory, new_name


def make_file_path(parent_dir):
    return os.path.join(config.UPLOAD_DIR, parent_dir)


def list_file_in_directory(path, username, parent_dir):
    try:
        files = os.listdir(path)
        paths = []
        for f in files:
            if os.path.isfile(os.path.join(os.path.join(os.getcwd(), path), f)):
                filetype = "f"
                download = gen_link(username, f, parent_dir, filetype, "download")
            else:
                filetype = "d"
                download = gen_link(username, f, parent_dir, filetype, "download")
            delete = gen_link(username, f, parent_dir, filetype, "delete")
            rename = gen_link(username, f, parent_dir, filetype, "rename")
            f = {"file_name": f, "download": download, "delete": delete, "rename": rename,
                 "modified": os.path.getmtime(os.path.join(path, f)), "file_type": filetype}
            paths.append(f)
    except:
        paths = "Error Not Found"
    return json.dumps(paths)


def gen_link(username, file_name, parent_dir, filetype, linktype):
    if linktype == "download":
        if filetype == "f":
            param = "dir=" + username + "&file_name=" + (parent_dir + "/" if parent_dir != "" else "") + file_name
        if filetype == "d":
            param = "dir=" + (parent_dir + "/" if parent_dir != "" else "") + file_name
    if linktype == "delete":
        param = "action=delete&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name
    if linktype == "rename":
        param = "action=delete&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name + "&new_name="
    return param


def delete_file(parent_dir, file_name):
    path = os.path.join(make_file_path(parent_dir), file_name)
    try:
        os.remove(path)
    except Exception as e:
        print(e)
        os.rmdir(path)


def rename_file(parent_dir, old_name, new_name):
    old_path = os.path.join(make_file_path(parent_dir), old_name)
    new_path = os.path.join(make_file_path(parent_dir), new_name)
    os.rename(old_path, new_path)
