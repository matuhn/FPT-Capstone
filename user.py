import config
import function


def check_username_duplicate(username):
    try:
        query = "SELECT USERNAME FROM Users WHERE USERNAME = :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username': username})
        for row in c:
            if row is not None:
                return "Duplicate"
        return "None"
    except:
        print("Bug when check_username_dup")


def check_email_duplicate(email):
    try:
        query = "SELECT EMAIL FROM Users WHERE EMAIL = :email"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'email': email})
        for row in c:
            if row is not None:
                return "Duplicate"
        return "None"
    except:
        print("Bug when check email")


def insert_user(username, email, password):
    try:
        query = "INSERT INTO Users(USERNAME, EMAIL, PASSWORD) VALUES (:username, :email, :password)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'username': username, 'email': email, 'password': password})
        conn.commit()
    except Exception as ex:
        print(ex)


def select_user(username_or_email):
    try:
        query = "SELECT ID, USERNAME, EMAIL, PASSWORD FROM Users WHERE EMAIL = :username_or_email OR USERNAME = :username_or_email"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username_or_email': username_or_email})
        for row in c:
            if row is not None:
                return row
        return "Not existed"
    except:
        print("Select never bug")


def register(username, email, password):
    try:
        if function.parameter_policy(username, config.USERNAME_POLICY) == "Match":
            if (function.parameter_policy(email, config.EMAIL_POLICY)) == "Match":
                if check_username_duplicate(username) != "Duplicate":
                    if check_email_duplicate(email) != "Duplicate":
                        insert_user(username, email, function.hash_password(password))
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
        if function.hash_password(password) == result:
            result = {"code": 200, "result": "Login successfully"}
        else:
            result = {"code": 500, "result": "Check your account and login again"}
        return result
    except:
        result = {"code": 500, "result": "Server Error"}
    return result
