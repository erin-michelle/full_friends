from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import time

count = 0

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key = "secretkey"
mysql = MySQLConnector('emails')

@app.route('/')
def index(): 
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def create():
	if len(request.form['name']) < 1:
		flash("Name cannot be empty.")	
		count += 1
	if request.form['name'].isalpha()	== False:
		flash("Name cannot contain numbers.")
		count += 1
	if len(request.form['email']) < 1:
		flash("Email cannot be blank.")
		count += 1
	if not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address")
		count += 1
	if count > 0:
		return redirect('/')	
	else:	
		query = "INSERT INTO emails (email, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['email'])
		mysql.run_mysql_query(query) 
		emails = mysql.fetch("SELECT * FROM emails")  
	
	return redirect('/')

app.run(debug=True)