from bottle import request, response, run, template, Bottle
from bottle import route, post, get, put, delete
import bottle_pgsql


app = Bottle()
plugin = bottle_pgsql.Plugin('dbname=moviedb user=yguo password=pass')
app.install(plugin)

keys = ["user_id", "movie_id", "rating", "title",
        "year", "director", "genre"]

tables = ["movies", "ratings"]


def gen_ins(table, fields):
    n = len(fields)
    k = ','.join([i for i in fields if i in keys])
    s = "("+",".join(["%s"] * n)+")"
    return 'INSERT INTO {} ({}) VALUES {}'.format(table, k, s)


def gen_upt(table, update_pairs, criteria):
    s = ','.join(["{} = '{}'".format(k, v)
        for (k, v) in update_pairs.items() if k in keys])
    where = 'AND'.join(["{} = '{}'".format(k, v)
        for (k, v) in criteria.items() if k in keys])
    return 'UPDATE {} SET {} WHERE {}'.format(
        table, s, where)


def gen_ret(table, filters):
    where = 'AND'.join(["{} = '{}'".format(k, v)
        for (k, v) in filters.items() if k in keys])
    return 'SELECT * FROM {} WHERE {}'.format(table, where)


def gen_del(table, filters):
    where = 'AND'.join(["{} = {}".format(k, v)
        for (k, v) in filters.items() if k in keys])
    return 'DELETE FROM {} WHERE {}'.format(table, where)


def gen_avg(uid):
    return '''SELECT to_char(avg(rating)::decimal,'FM90.0') 
        FROM ratings WHERE movie_id = {}'''.format(uid)


def update_rating(uid, db):  
    db.execute(gen_avg(uid))
    score = db.fetchone()['to_char']
    if score:
        db.execute(gen_upt('movies', {'rating': score}, {'movie_id': uid}))        

@app.post('/<table>')
def create(table, db):
    if table in tables:
        data = request.json
        query = gen_ins(table, data.keys())
        db.execute(query, tuple(data.values()))
        return '<p>The new item was added to {}.</p>'.format(table)    


@app.get('/<table>')
def retrieve(table, db):
    if table in tables: 
        query_string = request.query
        if not query_string:
            query = "SELECT * FROM {}".format(table)
            db.execute(query)
            data = db.fetchall()
            return template('make_table', rows = data)
        else:
            query = gen_ret(table, query_string)
            db.execute(query)
            data = db.fetchall()
            return template('make_table', rows = data)


@app.get('/movies/<uid:int>')
def show_movie_info(uid, db):
    update_rating(uid, db)
    query = gen_ret('movies', {'movie_id': uid})
    db.execute(query)
    info = db.fetchall()
    return template('make_table', rows = info)
    

# movies should be updated with movie_id only.
# ratings should be updated with user_id and movie_id only.
@app.put('/<table>')
def update(table, db):
    data = request.json
    query_string = request.query
    query = gen_upt(table, data, query_string)
    db.execute(query)
    return '<p> The {} table was updated.</p>'.format(table)


# movies should be deleted with movie_id only.
# ratings should be deleted with user_id and movie_id only.
@app.delete('/<table>')
def delete(table, db):
    query_string = request.query
    query = gen_del(table, query_string) 
    db.execute(query)
    return '<p> The item was deleted from {}.</p>'.format(table)


if __name__ == '__main__':
    run(app) 
