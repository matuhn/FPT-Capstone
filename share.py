import config
import function


def add_permission(path, date, share):
    try:
        query = "INSERT INTO FileShare(PATH, DATE, SHARE) " \
                "VALUES (:path, :date, :share)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'path': path, 'date': date, 'share': share})
        conn.commit()
    except Exception as ex:
        print(ex)


def get_permission(path):
    try:
        query = "SELECT SHARE FROM FileShare " \
                "WHERE PATH = :path"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'path': path})
        for row in c:
            if row is not None:
                return row
        return "Not existed"
    except Exception as ex:
        print(ex)


def check_permission(path, username):
    try:
        query = "SELECT SHARE, DATE FROM FileShare WHERE PATH = :path AND SHARE like '%"+username+"%'"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'path': path})
        for row in c:
            if row is not None:
                return row
        return "Not existed"
    except Exception as ex:
        print(ex)


