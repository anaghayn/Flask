from flask import Flask, request, render_template, redirect, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = 'jshdfyrg'
mysql = MySQLConnector(app, 'emaildb')
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")  


queries = {
    'create' : "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW());",
    'index' : "SELECT * FROM emails ORDER BY id DESC",
    'delete' : "DELETE FROM emails WHERE id = :id"
}

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if EMAIL_REGEX.match(request.form['email']):
            query = queries['create']
            data = { 'email' : request.form['email'] }
            mysql.query_db(query, data)
            flash('({}) is a VALID email address! Thank you!'.format(request.form["email"]), 'success')
            return redirect('/success')
        else:
            flash('{} is an invalid email address! Try again!'.format(request.form["email"]), 'error')
    return render_template('email_index.html')

@app.route('/success', methods=["POST", "GET"])
def success():
    query = queries['index']
    data = {}
    emails = mysql.query_db(query, data)
    return render_template('email_success.html', emails=emails)

@app.route('/remove/<id>', methods=["POST", "GET"])
def remove(id):
    query = queries['delete']
    data = { 'id' : id }
    flash('Successfully deleted email!', 'success')
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)