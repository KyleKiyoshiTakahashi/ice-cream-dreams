from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key= "IAMGROOT"
bcrypt = Bcrypt(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/icedream')
def icedream():
	# if session user is logged in, his ice cream is displayed 
	# with edit and delete buttons


	mysql=connectToMySQL('ice_creamDB')
	icecreams= mysql.query_db("SELECT * FROM ice_cream_flavors;")
	return render_template('icedream.html', icecreams=icecreams)

@app.route('/register', methods=['POST'])
def register():
	error = False
	if len(request.form['first_name']) < 3:
		flash("First Name must be 3 or more characters")
		error = True
	if len(request.form['last_name']) < 3:
		flash("Last Name must be 3 or more characters")
		error = True
	if len(request.form['password']) < 8:
		flash("Password must be 8 or more characters")
		error = True
	if request.form['password'] != request.form['c_password']: 
		flash("Password must match!")
		error = True
	if not request.form['first_name'].isalpha():
		flash("NO BOTS ALLOWED")
		error = True
	if not request.form['last_name'].isalpha():
		flash("NO BOTS ALLOWED-last name")
		error = True
	if not EMAIL_REGEX.match(request.form["email"]):
		flash("No BOT emails")
		error = True
	# email nonexistent
	data = {
		"email": request.form["email"]
	}
	query = "SELECT * FROM users WHERE email = %(email)s;"

	mysql = connectToMySQL('ice_creamDB')
	matching_email_users= mysql.query_db(query, data)
	if len(matching_email_users) > 0:
		flash("Identity theft is not a joke")
		error = True
	if error:
		return redirect('/')

	data = {
		"first_name" : request.form['first_name'],
		"last_name"  : request.form['last_name'],
		"email"      : request.form['email'],
		"password"   : bcrypt.generate_password_hash(request.form['password'])
	}
	query = "INSERT INTO users (first_name,last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
	mysql = connectToMySQL('ice_creamDB')
	user_id = mysql.query_db(query, data)
	print(user_id)
	session['user_id'] = user_id
	return redirect('/')

@app.route('/login', methods=['POST'])
def login():
	print(request.form)
	data = {
		"email": request.form["email"]
	}
	query = "SELECT * FROM users WHERE email = %(email)s;"
	mysql = connectToMySQL('ice_creamDB')
	matching_email_users= mysql.query_db(query, data)
	if len(matching_email_users) == 0:
		flash("invalid credentials")
		return redirect('/')
	user = matching_email_users[0]
	if bcrypt.check_password_hash(user['password'], request.form['password']):
		session['user_id']= user['id']
		return redirect('/icedream')
	flash('invalid credentials')
	return redirect('/icedream')

@app.route("/delete/<int:ice_cream_id>")
def delete(ice_cream_id):
	data= {
		"ice_cream_id": ice_cream_id
	}
	query= "DELETE FROM ice_cream_flavors WHERE id = (%(ice_cream_id)s);"
	mysql=connectToMySQL("ice_creamDB")
	mysql.query_db(query, data)
	return redirect('/icedream')

@app.route('/add/<int:user_id>', methods=["POST"])
def add(user_id):
	data={
		"names": request.form['name'],
		"description": request.form['description'],
		"user_id": session['user_id']
	}
	query="INSERT INTO ice_cream_flavors(user_id, name, description, created_at, updated_at) VALUES(%(user_id)s, %(names)s, %(description)s, NOW(), NOW());"
	mysql=connectToMySQL("ice_creamDB")
	mysql.query_db(query, data)
	return redirect('/icedream')

@app.route('/edit/<int:user_id>')
def edit_flavor(user_id):
	data={
		"user_id": session['user_id'] 

	}
	query="SELECT name, description FROM ice_cream_flavors WHERE id=(%(user_id)s);"
	mysql=connectToMySQL("ice_creamDB")
	my_icecream = mysql.query_db(query,data)
	
	return render_template('edit.html', icecream= my_icecream[0])

@app.route('/update/<int:user_id>')
def update(user_id):
	data={
		"user_id": session['user_id'],
		"ice_name": request.form['name_input'],
		"ice_description": request.form['input_description']
	}
	query="INSERT INTO ice_cream_flavors(user_id, name, description, created_at, updated_at) VALUES(%(user_id)s, %(ice_name)s, %(ice_description)s, NOW(), NOW());"
	mysql=connectToMySQL("ice_creamDB")
	mysql.query_db(query,data)
	return redirect('/icedream')



if __name__ == "__main__":
	app.run(debug=True)