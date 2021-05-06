import config
import function
import datetime
import fcrypto


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


def insert_user(username, email, fullname, password, confirm):
    try:
        query = "INSERT INTO Users(USERNAME, EMAIL, FULLNAME, PASSWORD, CONFIRM) " \
                "VALUES (:username, :email, :fullname, :password, :confirm)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'username': username, 'email': email, 'fullname': fullname, 'password': password,
                                      'confirm': confirm})
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


def get_confirm(username_or_email):
    try:
        query = "SELECT CONFIRM FROM Users " \
                "WHERE EMAIL = :username_or_email OR USERNAME = :username_or_email"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username_or_email': username_or_email})
        for row in c:
            if row is not None:
                return row
        return "Not existed"
    except Exception as ex:
        print(ex)


def update_confirm(username, confirm):
    try:
        query = "UPDATE Users SET CONFIRM = :confirm WHERE USERNAME = :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'confirm': confirm, 'username': username})
        conn.commit()
        return "Updated"
    except Exception as ex:
        print(ex)


def update_user(username, email, fullname):
    try:
        query = "UPDATE Users SET EMAIL = :email, FULLNAME = :fullname, WHERE USERNAME = :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'username': username, 'email': email, 'fullname': fullname})
        conn.commit()
        return "Updated"
    except Exception as ex:
        print(ex)


def update_pw(username, new):
    try:
        query = "UPDATE Users SET PASSWORD = :new WHERE USERNAME = :username"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'new': new, 'username': username})
        conn.commit()
        return "Updated"
    except Exception as ex:
        print(ex)


def register(username, email, fullname, password, confirm):
    try:
        if function.parameter_policy(username, config.USERNAME_POLICY) == "Match":
            if (function.parameter_policy(email, config.EMAIL_POLICY)) == "Match":
                if check_username_duplicate(username) != "Duplicate":
                    if check_email_duplicate(email, username) != "Duplicate":
                        insert_user(username, email, fullname, function.hash_with_salt(password), confirm)
                        function.init_directory(function.make_file_path(function.md5_hash(username)))
                        result = {"code": 200, "result": "Created user. Check mail to confirm"}
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
        try:
            if int(get_confirm(username_or_email)[0]) == 1:
                if function.hash_with_salt(password) == result:
                    result = {"code": 200, "result": "Login successfully"}
                else:
                    result = {"code": 500, "result": "Check your account and login again"}
            else:
                result = {"code": 500, "result": "Not yet confirm"}
        except Exception as ex:
            result = {"code": 500, "result": "Check your account and login again"}
        return result
    except Exception as ex:
        print(ex)
        result = {"code": 500, "result": "Server Error"}
    return result


def edit(username, email, fullname):
    try:
        if (function.parameter_policy(email, config.EMAIL_POLICY)) == "Match":
            if check_email_duplicate(email, username) != "Duplicate":
                update_user(username, email, fullname)
                result = {"code": 200, "result": "Updated user"}
            else:
                result = {"code": 500, "result": "Email Duplicate"}
        else:
            result = {"code": 500, "result": "Invalidate Email"}
    except Exception as ex:
        print(ex)
        result = {"code": 500, "result": "Server Error"}
    return result


def change_pass(username, old, new):
    try:
        if select_user(username)[3] == old:
            update_pw(username, new)
            result = {"code": 200, "result": "Updated Password"}
        else:
            result = {"code": 500, "result": "Wrong Password"}
    except Exception as ex:
        print(ex)
        result = {"code": 500, "result": "Server Error"}
    return result


def gen_link_confirm(username):
    time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).timestamp()
    token = username + "|" + str(time)
    token, nonce = fcrypto.aes_encrypt(token.encode("utf8"), config.SECRET_KEY)
    link = config.DOMAIN + "/api/auth/confirm?token=" + function.b64encode(token) + "&nonce=" + function.b64encode(nonce)
    content = "Please go to " + link + " to confirm your account"
    return content


def confirm(token, nonce):
    try:
        token = fcrypto.aes_decrypt(function.b64decode(token), config.SECRET_KEY, function.b64decode(nonce)).decode("utf-8").split("|")
        username = token[0]
        time = token[1]
        now = datetime.datetime.now().timestamp()
        if float(now) < float(time):
            update_confirm(username, 1)
            result = {"code": 200, "result": "Confirmed"}
        else:
            result = {"code": 500, "result": "Link Expired"}
    except:
        result = {"code": 500, "result": "Invalid token"}
    return result


def gen_reset_link(username_or_email, password):
    password = function.hash_with_salt(password)
    exist = select_user(username_or_email)
    if exist != "Not existed":
        time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).timestamp()
        token = username_or_email + "|" + password + "|" + str(time)
        token, nonce = fcrypto.aes_encrypt(token.encode("utf8"), config.SECRET_KEY)
        link = config.DOMAIN + "/api/auth/newPass?token=" + function.b64encode(token) + "&nonce=" + function.b64encode(nonce)
        content = "Password will be change to this encrypted password (" + password + ") if you go to " + link
        result = {"code": 200, "result": "Link sent"}
    else:
        content = ""
        result = {"code": 500, "result": "Not exist that username or email"}

    return content, result


def reset(token, nonce):
    try:
        token = fcrypto.aes_decrypt(function.b64decode(token), config.SECRET_KEY, function.b64decode(nonce)).decode("utf-8").split("|")
        username = token[0]
        password = token[1]
        time = token[2]
        now = datetime.datetime.now().timestamp()
        if float(now) < float(time):
            update_pw(username, password)
            result = {"code": 200, "result": "Password Changed"}
        else:
            result = {"code": 500, "result": "Link Expired"}
    except:
        result = {"code": 500, "result": "Invalid token"}
    return result

