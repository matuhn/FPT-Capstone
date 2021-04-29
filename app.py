import flask
import function
import config
import user
from Crypto.PublicKey import ECC
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import share
import fcrypto
import mimetypes
import stats
from flask_mail import Mail, Message


global ecc_private_key
global ecc_public_key


app = flask.Flask(__name__)
app.secret_key = config.APP_KEY
CORS(app, supports_credentials=True)
mail = Mail(app)
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/api/install')
def index():
    function.init_database()
    text = "Init Database"
    function.init_directory(config.UPLOAD_DIR)
    text += "\nInit Upload Directory"
    return text


def send_email(subject, receiver, content):
    try:
        msg = Message(subject, sender='fenclown.team@gmail.com', recipients=[receiver])
        msg.body = content
        mail.send(msg)
        print("SENT")
    except Exception as e:
        print(e)


@app.route('/api/auth/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == "GET":
        text = "POST username, email, fullname, password"
        return text
    elif flask.request.method == "POST":
        username = flask.request.form.get("username")
        email = flask.request.form.get("email")
        fullname = flask.request.form.get("fullname")
        password = flask.request.form.get("password")
        result = user.register(username, email, fullname, password, 0)
        content = user.gen_link_confirm(username)
        send_email("User Confirmation", email, content)
        result = flask.jsonify(result)
        return result


@app.route('/api/auth/confirm', methods=['GET', 'POST'])
def confirm():
    if flask.request.method == "GET":
        token = flask.request.args.get("token")
        nonce = flask.request.args.get("nonce")
        result = user.confirm(token, nonce)
        return result


@app.route('/api/auth/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == "GET":
        text = "POST username, password"
        return text
    elif flask.request.method == "POST":
        username_or_email = flask.request.form.get("username_or_email")
        password = flask.request.form.get("password")
        result = user.login(username_or_email, password)
        for key, value in result.items():
            if "successfully" in str(value):
                flask.session['USERNAME'] = user.select_user(username_or_email)[1]
        result = flask.jsonify(result)

        return result


@app.route('/api/auth/logout', methods=['GET', 'POST'])
def logout():
    flask.session.clear()
    return flask.jsonify({"code": 200, "result": "Logout successfully"})


@app.route('/api/auth/resetPass', methods=['GET', 'POST'])
def reset():
    if flask.request.method == "POST":
        username_or_email = flask.request.form.get("username_or_email")
        new_password = flask.request.form.get("new_password")
        email = user.select_user(username_or_email)[2]
        username = user.select_user(username_or_email)[1]
        content, result = user.gen_reset_link(username, new_password)
        if content != "":
            send_email("Reset Password", email, content)
        return result


@app.route('/api/auth/newPass', methods=['GET', 'POST'])
def new_pass():
    if flask.request.method == "GET":
        token = flask.request.args.get("token")
        nonce = flask.request.args.get("nonce")
        result = user.reset(token, nonce)
        return result


@app.route('/api/auth/getUserInfo', methods=['GET', 'POST'])
def get_user_info():
    try:
        username = flask.session['USERNAME']
        row = user.select_user(username)
        _id = row[0]
        email = row[2]
        fullname = row[4]
        return flask.jsonify({"code": 200, "result": {"id": _id, "username": username, "fullname": fullname, "email": email}})
    except:
        return flask.jsonify({"code": 500, "result": None})


@app.route('/api/editUserInfo', methods=['GET', 'POST'])
def edit_user_info():
    if flask.request.method == "GET":
        text = "POST email, fullname"
        return text
    elif flask.request.method == "POST":
        try:
            username = flask.session['USERNAME']
        except KeyError:
            return flask.jsonify({"code": 500, "result": "Please login before doing this"})
        email = flask.request.form.get("email")
        fullname = flask.request.form.get("fullname")
        result = user.edit(username, email, fullname)
        result = flask.jsonify(result)

        return result


@app.route('/api/changePassword', methods=['GET', 'POST'])
def change_pw():
    if flask.request.method == "GET":
        text = "POST old, new"
        return text
    elif flask.request.method == "POST":
        try:
            username = flask.session['USERNAME']
        except KeyError:
            return flask.jsonify({"code": 500, "result": "Please login before doing this"})
        old_password = function.hash_with_salt(flask.request.form.get("old_password"))
        new_password = function.hash_with_salt(flask.request.form.get("new_password"))
        result = user.change_pass(username, old_password, new_password)

        return result


@app.route('/api/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        parent_dir = flask.request.form.get("dir")
        if 'file' not in flask.request.files:
            return flask.jsonify({"code": 500, "result": "No file part"})
        file = flask.request.files['file']
        if file.filename == '':
            return flask.jsonify({"code": 500, "result": "No selected file"})
        if file:
            content = file.read()
            filename = secure_filename(file.filename)
            try:
                filename, directory, new_name = function.gen_file_name(filename, flask.session['USERNAME'], parent_dir)
            except KeyError:
                return flask.jsonify({"code": 500, "result": "Please login before doing this"})
            share.add_permission(directory, new_name, "|")
            stats.add_times(directory, new_name, "0")
            fcrypto.encrypt_file(directory, new_name, content, ecc_public_key)
            return flask.jsonify({"code": 200, "result": "dir=" + directory + "&file_name=" + new_name})


@app.route('/api/createDirectory', methods=['GET', 'POST'])
def create_dir():
    try:
        if flask.request.method == 'POST':
            sub_dir = flask.request.form.get("dir")
            if sub_dir is None:
                sub_dir = "NONAME"
            temp = sub_dir.split("/")
            temp[-1] = function.make_unique(temp[-1])
            sub_dir = "/".join(temp)
            username = function.md5_hash(flask.session['USERNAME'])
            parent_dir = username
            # share.add_permission(parent_dir, sub_dir, "|")
            function.init_directory(os.path.join(os.path.join(config.UPLOAD_DIR, parent_dir), sub_dir))
            return flask.jsonify({"code": 200, "result": "Created"})
    except Exception as e:
        print(e)
        return flask.jsonify({"code": 500, "result": "Please login before doing this"})


@app.route('/api/downloadFile', methods=['GET', 'POST'])
def download_file():
    try:
        parent_dir = flask.request.args.get("dir")
        name = flask.request.args.get("file_name")
        parent_dir = secure_filename(parent_dir)
        permission = "|" + flask.session['USERNAME'] + "|"
        if function.md5_hash(flask.session['USERNAME']) == parent_dir or permission in share.check_permission(parent_dir, name):
            key, nonce = fcrypto.get_key_and_nonce(parent_dir, name)
            path, content = fcrypto.decrypt_file(parent_dir, name, key, nonce, ecc_private_key)
            stats.download(parent_dir, name)
            #return flask.send_from_directory(config.DOWNLOAD_DIR, name)
            mime = mimetypes.guess_type(path)[0]
            return flask.Response(content, mimetype=mime, headers={"Content-disposition": "attachment; filename=" + name})
        else:
            return flask.jsonify({"code": 500, "result": "No Permission"})
    except Exception as e:
        print(e)
        return flask.jsonify({"code": 500, "result": "Something error"})


@app.route('/api/listFile', methods=['GET', 'POST'])
def list_file():
    try:
        if flask.request.method == 'POST':
            parent_dir = flask.request.form.get("dir")
            username = function.md5_hash(flask.session['USERNAME'])
            if parent_dir != "" and not parent_dir.startswith("\\") and not parent_dir.startswith("/"):
                path = os.path.join(function.make_file_path(username), parent_dir)
                print(path)
                files = function.list_file_in_directory(path, username, parent_dir)
            elif parent_dir == "":
                path = function.make_file_path(username)
                print(path)
                files = function.list_file_in_directory(path, username, parent_dir)
            else:
                return flask.jsonify({"code": 500, "result": "Try different path"})
            return flask.jsonify({"code": 200, "result": {"fileList": files}})
    except Exception as e:
        print(e)
        return flask.jsonify({"code": 500, "result": "Internal Error"})
    
    
@app.route('/api/editFile', methods=['GET', 'POST'])
def edit_file():
    try:
        parent_dir = flask.request.form.get("dir")
        name = flask.request.form.get("file_name")
        parent_dir = secure_filename(parent_dir)
        permission = "|" + flask.session['USERNAME'] + "|"
        if function.md5_hash(flask.session['USERNAME']) == parent_dir or (permission in share.check_permission(parent_dir, name)):
            action = flask.request.form.get("action")
            #delete file
            if action == "delete":
                try:
                    function.delete_file(parent_dir, name)
                    share.delete_file(parent_dir, name)
                    fcrypto.delete_file(parent_dir, name)
                    stats.delete_file(parent_dir, name)
                except:
                    return flask.jsonify({"code": 404, "result": "Not Found"})
                return flask.jsonify({"code": 200, "result": "Deleted"})
            #rename file
            elif action == "rename":
                new_name = function.make_unique(flask.request.form.get("new_name"))
                old_name = name.split("/")[-1]
                new_name = name.replace(old_name, new_name)

                is_dir = function.rename_file(parent_dir, name, new_name)

                share.edit_file_name(parent_dir, name, new_name, is_dir, old_name)
                fcrypto.edit_file_name(parent_dir, name, new_name, is_dir, old_name)
                stats.edit_file_name(parent_dir, name, new_name, is_dir, old_name)
                return flask.jsonify({"code": 200, "result": "Renamed"})
            #share_file
            elif action == "share":
                username = flask.request.form.get("username_list")
                return share.add_permission_of_list_username(username, parent_dir, name)
            #get_share_list
            elif action == "list_share":
                share_list = share.check_permission(parent_dir, name)
                return flask.jsonify({"code": 200, "result": share_list})
            #revoke_share_file
            elif action == "revoke":
                username = flask.request.form.get("username_list")
                return share.revoke_permission_of_list_username(username, parent_dir, name)
            else:
                return flask.jsonify({"code": 200, "result": "Please provide one action"})
        else:
            return flask.jsonify({"code": 500, "result": "No Permission"})
    except Exception as e:
        print(e)
        return flask.jsonify({"code": 500, "result": "Please login before doing this"})


@app.route('/api/listUser', methods=['GET', 'POST'])
def list_user():
    try:
        users = user.get_all_user()
        return flask.jsonify({"code": 200, "result": {"userList": users}})
    except KeyError:
        return flask.jsonify({"code": 500, "result": "Something wrong"})


@app.route('/api/listSharedFile', methods=['GET', 'POST'])
def list_shared_file():
    try:
        permission = "|" + flask.session['USERNAME'] + "|"
        files = share.get_shared_file_by_username(permission)
        return flask.jsonify({"code": 200, "result": {"sharedFileList": files}})
    except KeyError:
        return flask.jsonify({"code": 500, "result": "Something wrong"})


@app.route('/api/dataUsage', methods=['GET', 'POST'])
def data_usage():
    try:
        path = function.make_file_path(function.md5_hash(flask.session['USERNAME']))
        return flask.jsonify({"code": 200, "result": {"used": function.get_size(path)}})
    except KeyError:
        return flask.jsonify({"code": 500, "result": "Something wrong"})


@app.route('/api/getStats', methods=['GET', 'POST'])
def get_stats():
    try:
        dir = function.md5_hash(flask.session['USERNAME'])
        st = stats.get_stats(dir)
        return flask.jsonify({"code": 200, "result": {"stats": st}})
    except KeyError:
        return flask.jsonify({"code": 500, "result": "Something wrong"})


@app.route('/api/getSumOwn', methods=['GET', 'POST'])
def get_sum_own():
    try:
        username = function.md5_hash(flask.session['USERNAME'])
        path = function.make_file_path(username)
        return flask.jsonify({"code": 200, "result": {"stats": stats.sum_file(path)}})
    except KeyError:
        return flask.jsonify({"code": 500, "result": "Something wrong"})


@app.route('/api/getSumShared', methods=['GET', 'POST'])
def get_sum_share():
    try:
        username = flask.session['USERNAME']
        return flask.jsonify({"code": 200, "result": {"stats": stats.sum_shared_file(username)}})
    except KeyError:
        return flask.jsonify({"code": 500, "result": "Something wrong"})


if __name__ == '__main__':
    dev = 1
    if dev != 1:
        if len(sys.argv) < 2:
            print("Unable to load key")
            sys.exit(1)

        if len(sys.argv) < 3:
            try:
                ecc_key = ECC.import_key(open(sys.argv[1], 'rt').read())
            except Exception as e:
                print("Unable to load key", e)
                sys.exit(1)
        else:
            try:
                ecc_key = ECC.import_key(open(sys.argv[1], 'rt').read(), passphrase=sys.argv[2])
            except Exception as e:
                print("Unable to load key", e)
                sys.exit(1)
    else:
        ecc_key = ECC.import_key(open("test/private.pem", 'rt').read(), passphrase="hay")
    ecc_public_key = ecc_key.public_key()
    if ecc_key.has_private():
        ecc_private_key = ecc_key

    app.run()
