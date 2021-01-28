import flask
import function
import config
import user
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


app = flask.Flask(__name__)
app.secret_key = config.SECRET_KEY
CORS(app, supports_credentials=True)


@app.route('/api/install')
def index():
    function.init_database()
    text = "Init Database"
    function.init_directory(config.UPLOAD_DIR)
    text += "\nInit Upload Directory"
    return text


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
        result = user.register(username, email, fullname, password)
        result = flask.jsonify(result)
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
        text = "POST email, fullname, password"
        return text
    elif flask.request.method == "POST":
        try:
            username = flask.session['USERNAME']
        except KeyError:
            return flask.jsonify({"code": 500, "result": "Please login before doing this"})
        email = flask.request.form.get("email")
        fullname = flask.request.form.get("fullname")
        password = flask.request.form.get("password")
        result = user.edit(username, email, fullname, password)
        result = flask.jsonify(result)

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
            filename = secure_filename(file.filename)
            try:
                filename, directory, new_name = function.gen_file_name(filename, flask.session['USERNAME'], parent_dir)
            except KeyError:
                return flask.jsonify({"code": 500, "result": "Please login before doing this"})
            file.save(filename)
            return flask.jsonify({"code": 200, "result": "dir=" + directory + "&file_name=" + new_name})


@app.route('/api/createDirectory', methods=['GET', 'POST'])
def create_dir():
    try:
        if flask.request.method == 'POST':
            parent_dir = flask.request.form.get("dir")
            sub_dir = flask.request.form.get("sub_dir")
            username = function.hash_password(flask.session['USERNAME'])
            if parent_dir == "":
                parent_dir = username
                function.init_directory(os.path.join(os.path.join(config.UPLOAD_DIR, parent_dir), sub_dir))
                return flask.jsonify({"code": 200, "result": "Created"})
            return flask.jsonify({"code": 500, "result": parent_dir})
    except Exception as e:
        print(e)
        return flask.jsonify({"code": 500, "result": "Please login before doing this"})


@app.route('/api/downloadFile', methods=['GET', 'POST'])
def download_file():
    try:
        parent_dir = flask.request.form.get("dir")
        name = flask.request.form.get("file_name")
        parent_dir = secure_filename(parent_dir)
        if function.hash_password(flask.session['USERNAME']) == parent_dir:
            return flask.send_from_directory(function.make_file_path(parent_dir), name)
        else:
            return flask.jsonify({"code": 500, "result": "No Permission"})
    except Exception as e:
        print(e)
        return flask.jsonify({"code": 500, "result": "Please login before doing this"})


@app.route('/api/listFile', methods=['GET', 'POST'])
def list_file():
    try:
        if flask.request.method == 'POST':
            parent_dir = flask.request.form.get("dir")
            username = flask.request.form.get("share")
            if username == "":
                username = function.hash_password(flask.session['USERNAME'])
            if parent_dir != "" and not parent_dir.startswith("\\") and not parent_dir.startswith("/"):
                print("dir "+parent_dir)
                path = os.path.join(function.make_file_path(username), parent_dir)
                print(path)
                files = function.list_file_in_directory(path, username, parent_dir)
            elif parent_dir == "":
                print("dir " + parent_dir)
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
        if function.hash_password(flask.session['USERNAME']) == parent_dir:
            action = flask.request.form.get("action")
            #delete file
            if action == "delete":
                try:
                    function.delete_file(parent_dir, name)
                except:
                    return flask.jsonify({"code": 404, "result": "Not Found"})
                return flask.jsonify({"code": 200, "result": "Deleted"})
            #rename file
            if action == "rename":
                new_name = flask.request.form.get("new_name")
                function.rename_file(parent_dir, name, new_name)
                return flask.jsonify({"code": 200, "result": "Renamed"})
            return flask.jsonify({"code": 200, "result": "Please provide one action"})
        else:
            print(flask.session['USERNAME'], parent_dir)
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


if __name__ == '__main__':
    app.run()
