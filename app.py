import flask
import function
import config
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
        text = "POST username, email, password, confirm_password"
        return text
    elif flask.request.method == "POST":
        username = flask.request.form.get("username")
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        result = function.register(username, email, password)
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
        result = function.login(username_or_email, password)
        for key, value in result.items():
            if ("successfully" in str(value)):
                flask.session['USERNAME'] = username_or_email
                print(flask.session['USERNAME'])
        result = flask.jsonify(result)

        return result


if __name__ == '__main__':
    app.run()
