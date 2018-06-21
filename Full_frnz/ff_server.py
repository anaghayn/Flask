from flask import Flask, request, redirect, session, render_template, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'frnzzdb')

@app.route('/')
def index():
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	return render_template('ff_index.html', friends_list=friends)

@app.route('/addFrnz', methods=['POST'])
def add_friend():
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(request.form['first_name'], request.form['last_name'], request.form['occupation'])
	data = {
			'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'occupation': request.form['occupation']		
	        }

	mysql.query_db(query, data)
   # mysql.run_mysql_query(query)

	return redirect('/')
app.run(debug=True)