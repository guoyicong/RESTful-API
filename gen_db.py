import sqlite3

conn = sqlite3.connect('movies.db')
c = conn.cursor()

c.execute('''CREATE TABLE movies
             (uid, title, year, director, genre)''')

conn.commit()
conn.close()
