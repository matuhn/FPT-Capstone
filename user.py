import config
import function


def get_all_user():
    try:
        users = []
        query = "SELECT USERNAME FROM Users"
        conn = function.get_connection()
        c = conn.cursor().execute(query)
        for row in c:
            if row is not None:
                users.append(row[0])
        print(users)
        return users
    except Exception as ex:
        print(ex)


def check_username_duplicate(username):
    try:
        query = "SELECT USERNAME FROM Users WHERE USERNAME = :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username': username})
        for row in c:
            if row is not None:
                return "Duplicate"
        return "None"
    except Exception as ex:
        print(ex)


def check_email_duplicate(email, username):
    try:
        query = "SELECT EMAIL FROM Users WHERE EMAIL = :email AND USERNAME != :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'email': email, 'username': username})
        for row in c:
            if row is not None:
                return "Duplicate"
        return "None"
    except Exception as ex:
        print(ex)


def insert_user(username, email, fullname, password):
    try:
        query = "INSERT INTO Users(USERNAME, EMAIL, FULLNAME, PASSWORD) " \
                "VALUES (:username, :email, :fullname, :password)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'username': username, 'email': email, 'fullname': fullname, 'password': password})
        conn.commit()
    except Exception as ex:
        print(ex)


def select_user(username_or_email):
    try:
        query = "SELECT ID, USERNAME, EMAIL, PASSWORD, FULLNAME FROM Users " \
                "WHERE EMAIL = :username_or_email OR USERNAME = :username_or_email"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username_or_email': username_or_email})
        for row in c:
            if row is not None:
                return row
        return "Not existed"
    except Exception as ex:
        print(ex)


def update_user(username, email, fullname, password):
    try:
        query = "UPDATE Users SET EMAIL = :email, FULLNAME = :fullname, PASSWORD = :password WHERE USERNAME = :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username': username, 'email': email, 'fullname': fullname, 'password': password})
        conn.commit()
        return "Updated"
    except Exception as ex:
        print(ex)


def register(username, email, fullname, password):
    try:
        if function.parameter_policy(username, config.USERNAME_POLICY) == "Match":
            if (function.parameter_policy(email, config.EMAIL_POLICY)) == "Match":
                if check_username_duplicate(username) != "Duplicate":
                    if check_email_duplicate(email, username) != "Duplicate":
                        insert_user(username, email, fullname, function.hash_with_salt(password))
                        function.init_directory(function.make_file_path(function.md5_hash(username)))
                        result = {"code": 200, "result": "Created user"}
                    else:
                        result = {"code": 500, "result": "Email Duplicate"}
                else:
                    result = {"code": 500, "result": "Username Duplicate"}
            else:
                result = {"code": 500, "result": "Invalidate Email"}
        else:
            result = {"code": 500, "result": "Invalidate Username"}
    except Exception as ex:
        print(ex)
        result = {"code": 500, "result": "Server Error"}
    return result


def login(username_or_email, password):
    try:
        result = select_user(username_or_email)[3]
        if function.hash_with_salt(password) == result:
            result = {"code": 200, "result": "Login successfully"}
        else:
            result = {"code": 500, "result": "Check your account and login again"}
        return result
    except Exception as ex:
        print(ex)
        result = {"code": 500, "result": "Server Error"}
    return result


def edit(username, email, fullname, password):
    try:
        if (function.parameter_policy(email, config.EMAIL_POLICY)) == "Match":
            if check_email_duplicate(email, username) != "Duplicate":
                if password != "":
                    update_user(username, email, fullname, function.md5_hash(password))
                    result = {"code": 200, "result": "Updated user"}
                else:
                    result = {"code": 500, "result": "Password is not null"}
            else:
                result = {"code": 500, "result": "Email Duplicate"}
        else:
            result = {"code": 500, "result": "Invalidate Email"}
    except Exception as ex:
        print(ex)
        result = {"code": 500, "result": "Server Error"}
    return result
