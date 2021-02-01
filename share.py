import user
import function


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


def add_permission_of_list_username(username, parent_dir, filename):
    try:
        user_list = username.replace(" ", "").split("|")
        share = check_permission(parent_dir, filename)
        print(share)
        for uName in user_list:
            if (uName + "|") not in share:
                if (uName + "|") not in check_permission(parent_dir, filename):
                    if user.select_user(uName) != "Not existed":
                        share += (uName + "|")
        update_permission(parent_dir, filename, share)
        return {"code": 200, "result": "Shared"}
    except Exception as ex:
        print(ex)