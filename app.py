from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_session import Session
from cs50 import SQL
from pyTwistyScrambler import scrambler333
from werkzeug.security import check_password_hash, generate_password_hash
import time

from helpers import login_required, format_time, get_msec

app = Flask(__name__)
app.secret_key = 'dev'

app.jinja_env.filters["solve_time"] = format_time

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

# Special characters to check for in password
special_chars = r" !#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
numbers = "1234567890"


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
@login_required
def index():
    competitions = db.execute(
        'SELECT name, comp_id as id, datetime as created_on, username as creator, users.id as user_id FROM competitions '
        'JOIN users ON users.id = competitions.creator_id ORDER BY comp_id DESC LIMIT 10')
    return render_template("index.html", competitions=competitions)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not password or not confirm:
            flash("The forms cannot be left blank")
            return redirect('/register')

        if confirm != password:
            flash("Password and Confirmation do not match")
            return redirect('/register')

        contains_special = False
        contains_number = False

        for i in special_chars:
            if password.find(i) != -1:
                contains_special = True

        for i in numbers:
            if password.find(i) != -1:
                contains_number = True

        if not contains_number or not contains_special or not len(password) >= 8:
            flash("Password must contain at least 8 characters, a number and a special character")
            return redirect('/register')

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
            return redirect(url_for('index'))
        except ValueError:
            flash("Username has already been taken")

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password cannot be blank.")
            return redirect(url_for('login'))

        rows = db.execute("SELECT * FROM USERS WHERE LOWER(username) = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Username/Password is incorrect")
            return redirect(url_for('login'))

        session["user_id"] = rows[0]["id"]
        return redirect(url_for('index'))

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/newcomp', methods=["GET", "POST"])
@login_required
def newcomp():
    if request.method == "POST":
        comp_name = request.form.get("name")
        scramble = request.form.get("scramble")

        if not comp_name:
            flash("Competition name cannot be blank")
            return redirect(url_for('newcomp'))

        if not scramble:
            scramble = scrambler333.get_WCA_scramble()

        date_time = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())

        db.execute("INSERT INTO competitions (name, scramble, datetime, creator_id) VALUES (?, ?, ?, ?)", comp_name,
                   scramble, date_time, session["user_id"])

        return redirect(url_for('index'))

    return render_template('newcomp.html')


@app.route('/comps/<comp_id>', methods=["GET", "POST"])
@login_required
def comps(comp_id):
    if request.method == "POST":
        input_time = request.form.get("time")

        if not input_time:
            flash("Input time cannot be blank")
            return redirect('/comps/' + comp_id)

        if get_msec(input_time) is None:
            flash("There was an error inputting your time, please try again")
            return redirect('/comps/' + comp_id)
        else:
            input_time = get_msec(input_time)

        users_time = db.execute("SELECT time FROM solves WHERE user_id = ? AND comp_id = ?",
                                session["user_id"], comp_id)

        if not users_time:
            db.execute("INSERT INTO solves (time, user_id, comp_id) VALUES (?, ?, ?)",
                       input_time, session["user_id"], comp_id)
            return redirect('/comps/' + comp_id)

        if users_time[0]['time'] > input_time:
            db.execute("UPDATE solves SET time = ? WHERE user_id = ? AND comp_id = ?",
                       input_time, session["user_id"], comp_id)

    try:
        comp_id = int(comp_id)
    except ValueError:
        return redirect(url_for('index'))

    competition = db.execute('SELECT name, scramble, comp_id, username as creator, users.id as user_id FROM competitions '
                             'JOIN users ON competitions.creator_id = users.id '
                             'WHERE comp_id = ?', comp_id)

    try:
        competition[0]
    except IndexError:
        return redirect(url_for('index'))

    solves = db.execute('SELECT time, username, user_id, creator_id, solves.comp_id as comp_id FROM solves '
                        'JOIN users u on solves.user_id = u.id JOIN competitions c on c.comp_id = solves.comp_id '
                        'WHERE solves.comp_id = ? '
                        'ORDER BY solve_id DESC',
                        comp_id)

    return render_template('competition.html', competition=competition[0], solves=solves)


@app.route('/remove/<comp_id>', methods=["POST"])
@login_required
def remove(comp_id):
    solve_id = request.form.get("solve_id")
    if not solve_id:
        return redirect("/comps/" + comp_id)

    db.execute('DELETE FROM solves WHERE user_id = ? AND comp_id = ?', solve_id, comp_id)
    return redirect("/comps/" + comp_id)


@app.route('/users/<user_id>')
@login_required
def user_profile(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        redirect(url_for('index'))

    user = db.execute('SELECT username FROM users WHERE id = ?', user_id)

    try:
        user[0]
    except IndexError:
        return redirect(url_for('index'))

    pb = db.execute('SELECT MIN(time) as pb FROM solves WHERE user_id = ?', user_id)

    return render_template('profile.html', user=user[0], pb=format_time(pb[0]['pb']))


if __name__ == '__main__':
    app.run()
