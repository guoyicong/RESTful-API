import psycopg2

conn = psycopg2.connect("dbname=moviedb user=yguo")
c = conn.cursor()

c.execute('''CREATE TABLE ratings (
                user_id     integer,  
                movie_id    integer,
                rating      decimal
);''')

c.execute('''CREATE TABLE movies (
                movie_id    integer,
                title       varchar,   
                year        integer,
                director    varchar,
                genre       varchar,
                rating      decimal
);''')

conn.commit()
conn.close()
