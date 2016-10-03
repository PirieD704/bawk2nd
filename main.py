# Import flask stuff
from flask import Flask, render_template, redirect, request, session
from flaskext.mysql import MySQL
import bcrypt

# Set up mysql connection later

app = Flask(__name__)
#create an instance of the mysql class
mysql = MySQL()

#add to the app (Flask object) some config data for our connection
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
#The name of the database we want to connect to at the DB server
app.config['MYSQL_DATABASE_DB'] = 'bawk'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# user the mysql object's method "init_app" and pass it the flask object
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
app.secret_key = "HAOEA2342352LKT3049203ytO4htr130JSasdKLF239"

# Create route for home page
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register')
def register():
	if request.args.get('username'):
		# the username variable is set in the query string
		return render_template('register.html', message="that username is already taken")
	else:
		return render_template('register.html')

@app.route('/register_submit', methods=['POST'])
def register_submit():
	#first, check to see if the username is already taken
	# this means a select statement
	check_username_query = "SELECT * FROM user WHERE username = '%s'" % request.form['username']
	print check_username_query
	cursor.execute(check_username_query)
	check_username_result = cursor.fetchone()
	if check_username_result is None:
		# No match. Insert
		session['username'] = request.form['username']
		print session['username']
		fullName = request.form['real_name']
		username = request.form['username']
		password = request.form['password'].encode('utf-8')
		hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
		email = request.form['email']
		# avatar = request.file['avatar']
		username_insert_query = "INSERT INTO user(real_name, username, password, email) VALUES (%s, %s, %s, %s)"
		cursor.execute(username_insert_query, (fullName, username, hashed_password, email))
		conn.commit()
		return redirect('/'+username)
	else:
		return redirect('/register?username=taken')
	print  check_username_result
	return render_template('index.html', check_username_result = check_username_result) 

	# second, if it is taken, send them back to the register page with a message
	# second b, if it's not taken, then insert the user into mysql

@app.route('/login')
def login():
	return render_template('/login.html')

@app.route('/login_submit', methods=["POST"])
def login_submit():
	# to check a has against english:
	check_username_query = "SELECT password FROM user WHERE username = '%s'" % request.form['username']
	cursor.execute(check_username_query)
	check_username_result = cursor.fetchone()
	session['username'] = request.form['username']
	print session['username']
	hashed_password_from_mysql = check_username_result[0].encode('utf-8')
	password = request.form['password'].encode('utf-8')
	username = request.form['username']
	print  check_username_result
	if bcrypt.hashpw(password, hashed_password_from_mysql) == hashed_password_from_mysql:
		# we have a match
		print "password matched"
		return redirect('/' + username)
	return "no dice"

@app.route('/logout')
def logout():
	session.clear()
	return render_template('/index.html', message="logged out")

@app.route('/<username>')
def user_page(username):
	return 'I made it!'

if __name__ == "__main__":
	app.run(debug=True)











