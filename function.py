import sqlite3
import config
import re
import hashlib
from pathlib import Path
import os
from uuid import uuid4
import json
import shutil


def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            print(f)
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


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
                    "FULLNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL)"
            conn = get_connection()
            conn.cursor().execute(query)
            query = "CREATE TABLE IF NOT EXISTS FileShare " \
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    "DIR TEXT NOT NULL, FILENAME TEXT NOT NULL UNIQUE, " \
                    "SHARE TEXT NOT NULL)"
            conn.cursor().execute(query)
            query = "CREATE TABLE IF NOT EXISTS Crypto " \
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    "DIR TEXT NOT NULL, FILENAME TEXT NOT NULL UNIQUE, " \
                    "KEY TEXT NOT NULL, NONCE TEXT NOT NULL)"
            conn.cursor().execute(query)
            query = "CREATE TABLE IF NOT EXISTS Stats " \
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
                    "DIR TEXT NOT NULL, FILENAME TEXT NOT NULL UNIQUE, " \
                    "TIMES TEXT NOT NULL)"
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


def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_with_salt(password):
    return hashlib.md5((password + config.MD5_SALT).encode()).hexdigest()

def gen_file_name(name, username, pdir):
    parent_dir = os.path.join(config.UPLOAD_DIR, md5_hash(username))
    parent_dir = os.path.join(parent_dir, pdir)
    init_directory(parent_dir)
    new1_name = make_unique(name)
    directory = md5_hash(username)
    new_name = (pdir + "/" if pdir != "" else "") + new1_name
    return os.path.join(parent_dir, new1_name), directory, new_name


def make_file_path(parent_dir):
    return os.path.join(config.UPLOAD_DIR, parent_dir)


def list_file_in_directory(path, username, parent_dir):
    try:
        files = os.listdir(path)
        paths = []
        for f in files:
            fullpath = os.path.join(os.path.join(os.getcwd(), path), f)
            if os.path.isfile(fullpath):
                filetype = "f"
                download = gen_link(username, f, parent_dir, filetype, "download")
                size = os.path.getsize(fullpath)
            else:
                filetype = "d"
                download = gen_link(username, f, parent_dir, filetype, "download")
                size = ""
            delete = gen_link(username, f, parent_dir, filetype, "delete")
            rename = gen_link(username, f, parent_dir, filetype, "rename")
            share = gen_link(username, f, parent_dir, filetype, "share")
            revoke = gen_link(username, f, parent_dir, filetype, "revoke")
            list_share = gen_link(username, f, parent_dir, filetype, "list_share")
            f = {"file_name": f, "download": download, "delete": delete, "rename": rename,
                 "share": share, "revoke": revoke, "list_share": list_share,
                 "modified": os.path.getmtime(os.path.join(path, f)), "file_type": filetype, "size": size}
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
    elif linktype == "delete":
        param = "action=delete&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name
    elif linktype == "rename":
        param = "action=rename&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name + "&new_name="
    elif linktype == "share":
        param = "action=share&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name + "&username_list="
    elif linktype == "revoke":
        param = "action=revoke&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name + "&username_list="
    elif linktype == "list_share":
        param = "action=list_share&dir=" + username + "&file_name=" + \
                (parent_dir + "/" if parent_dir != "" else "") + file_name
    return param


def delete_file(parent_dir, file_name):
    path = os.path.join(make_file_path(parent_dir), file_name)
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def rename_file(parent_dir, old_name, new_name):
    old_path = os.path.join(make_file_path(parent_dir), old_name)
    new_path = os.path.join(make_file_path(parent_dir), new_name)
    os.rename(old_path, new_path)
