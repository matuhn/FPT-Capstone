import user
import fcrypto
import function
import json
import os


def add_permission(parent_dir, filename, share):
    try:
        query = "INSERT INTO FileShare(DIR, FILENAME, SHARE, SIGN) " \
                "VALUES (:dir, :filename, :share, :sign)"
        conn = function.get_connection()
        message = (parent_dir + filename + share).encode('utf-8')
        sign = fcrypto.ecc_sign(message)
        conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename, 'share': share, 'sign': sign})
        conn.commit()
    except Exception as ex:
        print(ex)


def check_permission(parent_dir, filename):
    try:
        query = "SELECT SHARE FROM FileShare WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename})
        for row in c:
            if row is not None:
                print(row[0])
                return row[0]
        return 0
    except Exception as ex:
        print(ex)


def update_permission(parent_dir, filename, share):
    try:
        query = "UPDATE FileShare SET SHARE = :share WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename, 'share': share})
        conn.commit()
    except Exception as ex:
        print(ex)


def get_file_by_username(username):
    try:
        query = "SELECT DIR, FILENAME FROM FileShare WHERE SHARE LIKE '%" + username + "%'"
        conn = function.get_connection()
        c = conn.cursor().execute(query)
        return c
    except Exception as ex:
        print(ex)


def add_permission_of_list_username(username, parent_dir, filename):
    try:
        user_list = username.replace(" ", "").split("|")
        share = check_permission(parent_dir, filename)
        for u_name in user_list:
            if ("|" + u_name + "|") not in share:
                if user.select_user(u_name) != 0:
                    share += (u_name + "|")
        update_permission(parent_dir, filename, share)
        return {"code": 200, "result": "Shared"}
    except Exception as ex:
        print(ex)


def edit_file_name(parent_dir, filename, new_name, is_dir, old_name):
    try:
        if is_dir:
            query = "UPDATE FileShare SET FILENAME = REPLACE(FILENAME, :old_name, :new_name) " \
                    "WHERE DIR = :dir AND FILENAME LIKE '%" + old_name + "%'"
            conn = function.get_connection()
            conn.cursor().execute(query, {'new_name': new_name.split("/")[-1], 'dir': parent_dir, 'old_name': old_name})
        else:
            query = "UPDATE FileShare SET FILENAME = :new_name WHERE DIR = :dir AND FILENAME = :filename"
            conn = function.get_connection()
            conn.cursor().execute(query, {'new_name': new_name, 'filename': filename, 'dir': parent_dir})
        conn.commit()
    except Exception as ex:
        print(ex)


def delete_file(parent_dir, filename):
    try:
        query = "DELETE FROM FileShare WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'filename': filename, 'dir': parent_dir})
        conn.commit()
    except Exception as ex:
        print(ex)


def revoke_permission_of_list_username(username, parent_dir, filename):
    try:
        user_list = username.replace(" ", "").split("|")
        share = check_permission(parent_dir, filename)
        for u_name in user_list:
            if ("|" + u_name + "|") in share:
                if user.select_user(u_name) != 0:
                    u_name = "|" + u_name + "|"
                    share = share.replace(u_name, "|")
        update_permission(parent_dir, filename, share)
        return {"code": 200, "result": "Revoked"}
    except Exception as ex:
        print(ex)


def get_shared_file_by_username(username):
    c = get_file_by_username(username)
    print(username)
    try:
        result = []
        for row in c:
            path = os.path.join(function.make_file_path(row[0]), row[1])
            full_path = os.path.join(os.getcwd(), path)
            size = os.path.getsize(full_path)
            modified = os.path.getmtime(path)
            owner = find_owner(row[0])
            download = function.gen_link(row[0], row[1], "", "f", "download")
            f = {"file_name": row[1], "size": size, "modified": modified, "owner": owner, "download": download}
            result.append(f)
    except Exception as ex:
        print(ex)
    return json.dumps(result)


def find_owner(parent_dir):
    try:
        query = "SELECT USERNAME FROM Users "
        conn = function.get_connection()
        c = conn.cursor().execute(query)
        for row in c:
            if function.md5_hash(row[0]) == parent_dir:
                return row
    except Exception as ex:
        print(ex)
