import flask
import function
import config
import user
from flask_cors import CORS

app = flask.Flask(__name__)
app.secret_key = config.SECRETKEY
CORS(app)


@app.route('/api/install')
def index():
    function.init_database()
    text = "Init Database"
    return text


@app.route('/api/auth/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == "GET":
        text = "POST username, email, password"
        return text
    elif flask.request.method == "POST":
        username = flask.request.form.get("username")
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        result = user.register(username, email, password)
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
        id = user.select_user(username)[0]
        email = user.select_user(username)[2]
        return flask.jsonify({"code": 200, "result": {"id": id, "username": username, "email": email}})
    except:
        return flask.jsonify({"code": 500, "result": None})


if __name__ == '__main__':
    app.run()
