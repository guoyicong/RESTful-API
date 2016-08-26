from bottle import request, response, run, template, Bottle
from bottle import route, post, get, put, delete
import bottle_pgsql


app = Bottle()
plugin = bottle_pgsql.Plugin('dbname=moviedb user=yguo password=pass')
app.install(plugin)


def gen_ins(table, fields, values):
    return 'INSERT INTO {} {} VALUES {}'.format(
        table, tuple(fields), tuple(values))


def gen_upt(table, update_pairs, criteria):
    s = ','.join(["'{}' = '{}'".format(k, v)
        for (k, v) in update_pairs.items()])
    where = 'AND'.join(["{} LIKE '{}'".format(k, v)
        for (k, v) in criteria.items()])
    return 'UPDATE {} SET {} WHERE {}'.format(
        table, s, where)


def gen_ret(table, filters):
    where = 'AND'.join(["{} LIKE '{}'".format(k, v)
        for (k, v) in filters.items()])
    return 'SELECT * FROM {} WHERE {}'.format(table, where)


def gen_del(table, filters):
    where = 'AND'.join(["{} LIKE {}".format(k, v)
        for (k, v) in filters.items()])
    return 'DELETE FROM {} WHERE {}'.format(table, where)


def gen_avg(uid):
    return 'SELECT avg(rating) FROM ratings WHERE movie_id LIKE {}'.format(uid)


def update_rating(uid, db):
    score = db.execute(gen_avg(uid)).fetchone()[0]
    db.execute(gen_upt('movies', {'rating': score}, {'movie_id': uid}))        


@app.post('/<table>')
def create(table, db):
    data = request.json
    query = gen_ins(table, list(data.keys()), list(data.values()))
    db.execute(query)
    return '<p>The new item was added to {}.</p>'.format(table)    


@app.get('/<table>')
def retrieve(table, db): 
    query_string = request.query
    if not query_string:
        data = db.execute("SELECT * FROM {}".format(table)).fetchall()
        return template('make_table', rows = data)
    else:
        query = gen_ret(table, query_string)
        data = db.execute(query).fetchall()
        return template('make_table', rows = data)


@app.get('/movies/<uid:int>')
def show_movie_info(uid, db):
    update_rating(uid, db)
    query = gen_ret('movies', {'movie_id': uid})
    info = db.execute(query).fetchall()
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
