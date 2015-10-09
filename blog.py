from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps


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

#login required
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login first.")
			return redirect(url_for('login'))
	return wrap


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
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
	return render_template('main.html', posts=posts)


#add post
@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields are required. Please try again.")
		return redirect(url_for('main'))
	else:
		g.db = connect_db()
		g.db.execute('INSERT INTO posts (title, post) VALUES (?,?)',
		[request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted!')
		return redirect(url_for('main'))




#run app
if __name__ == '__main__':
	app.run(debug=True)
