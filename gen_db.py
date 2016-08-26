import sqlite3

conn = sqlite3.connect('movies.db')
c = conn.cursor()

c.execute('CREATE TABLE ratings'
          '(user_id, movie_id, rating)')

c.execute('CREATE TABLE movies'
          '(movie_id, title, year, director, genre, rating)')

conn.commit()
conn.close()
