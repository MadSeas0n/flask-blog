import sqlite3

with sqlite3.connect("blog.db") as connection:
	cur = connection.cursor()

	cur.execute("CREATE table posts(title text, post text)")

	cur.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
	cur.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
	cur.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
	cur.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')