import user
import function
import json


def add_permission(parent_dir, filename, share):
    try:
        query = "INSERT INTO FileShare(DIR, FILENAME, SHARE) " \
                "VALUES (:dir, :filename, :share)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename, 'share': share})
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
        return "Not existed"
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
                if user.select_user(u_name) != "Not existed":
                    share += (u_name + "|")
        update_permission(parent_dir, filename, share)
        return {"code": 200, "result": "Shared"}
    except Exception as ex:
        print(ex)


def edit_file_name(parent_dir, filename, new_name):
    try:
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
                if user.select_user(u_name) != "Not existed":
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
            print(row)
            f = {"file_name": row[1], "dir": row[0]}
            result.append(f)
    except Exception as ex:
        print(ex)
    return json.dumps(result)