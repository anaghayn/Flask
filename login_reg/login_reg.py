from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import md5


app = Flask(__name__)
app.secret_key = 'key'
mysql = MySQLConnector(app, 'loginregdb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    if len(request.form['email']) < 1 or len(request.form['password']) < 1:
        flash('Please enter your email and password.')
        return redirect('/')


app.run(debug=True)