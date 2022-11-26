from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test1234'
app.config['MYSQL_DB'] = 'IBMAssign2'

mysql = MySQL(app)


@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        emailregex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(emailregex, email):
            return render_template('signup.html', email=email, password=password, confirmpassword=confirmpassword, emailerr=True)
        elif not any(char.isdigit() for char in password) or not any(char.isdigit() for char in password) or not any(char.isdigit() for char in password) or len(password) < 8:
            return render_template('signup.html', email=email, password=password, confirmpassword=confirmpassword, passworderr=True)
        elif password != confirmpassword:
            return render_template('signup.html', email=email, password=password, confirmpassword=confirmpassword, confirmpassworderr=True)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO login VALUES(%s,%s)", (email, password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('signin.html')
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM login where email = %s", (email,))
        data = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()
        if data == None:
            return render_template('signin.html', err=1)
        elif data[1] != password:
            return render_template('signin.html', err=2)
        else:
            return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
