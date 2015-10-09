from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3


#configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'rM\xb1\xdc\x12o\xd6i\xff+9$T\x8e\xec\x00\x13\x82.*\x16TG\xbd'

app = Flask(__name__)

app.config.from_object(__name__)

#connect db
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

#login
@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = "Failed to logon. Try again"
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error = error)

#logout
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

#main
@app.route('/main')
def main():
	return render_template('main.html')

#run app
if __name__ == '__main__':
	app.run(debug=True)
