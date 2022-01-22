from flask import *
import MySQLdb
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = "Steve"
db = MySQLdb.connect(host="shinyang.mysql.pythonanywhere-services.com", user='shinyang', passwd = '1qa2ws3ed!@#', db ='shinyang$default')
cursor = db.cursor()

def doFlash(data):
    base = session.get('_flashes', [])
    pass

@app.route('/', methods=['GET', 'POST'])
def home():
    flash_data = get_flashed_messages()
    if request.method == 'POST':
        if request.form.get("flash_button"):
            flash(request.form.get("value"))
            if request.form.get("is_success"):
                flash("Success")
            return render_template('flash.html')
        if request.form.get("reset_flash"):
            session.pop('_flashes', None)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    global cursor
    if request.method == 'POST':
        if request.form.get('password') is not request.form.get('passwordconfirm'):
            return '<!DOCTYPE html><html><head><title>Wrong password</title><meta charset="utf-8"></head><body><h1>Wrong Password</h1><p>please input your password again</p></body></html>'
        try:
            hash = pbkdf2_sha256.hash(request.form.get['password'])
            cursor.execute('INSERT INTO Users (Name, Email, PasswordHash, DisplayName) ("{0}", "{1}", "{2}", "{3}")'.format(request.form['name'], request.form['email'], hash, request.form['displayname']))
            return cursor.execute(f'SELECT * from Users where Name = "${request.form.get()}")
        except:
            return '<!DOCTYPE html><html><head><title>Wrong password</title><meta charset="utf-8"></head><body><h1>Duplicated Name</h1><p>You have duplicated name with other user. please change your name, or username, and try again.</p></body></html>'
    elif request.method == 'GET':
        pass
    return render_template('register.html')

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    name = request.form.get('name')
    return render_template('welcome.html').format(name)


@app.route('/test/<value1>/<value2>')
def test(value1, value2):
    return f'Value1: {value1} <br> Value2: {value2}'


@app.route('/css')
def css():
    return render_template('css.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.form.get("submit_1"):
        return render_template("submit_1")
    elif request.form.get("submit_2"):
        return render_template("submit_2")
    else:
        return render_template("form.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=8080)