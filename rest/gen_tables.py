import psycopg2

conn = psycopg2.connect("dbname=moviedb user=yguo")
c = conn.cursor()

c.execute('''CREATE TABLE ratings (
                user_id     integer,  
                movie_id    integer,
                rating      decimal(1,0)
);''')

c.execute('''CREATE TABLE movies (
                movie_id    integer,
                title       varchar,   
                year        integer,
                director    varchar,
                genre       varchar,
                rating      decimal(2,1)
);''')

conn.commit()
conn.close()
