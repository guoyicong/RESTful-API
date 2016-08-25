from bottle import request, response, run, template, Bottle
from bottle import post, get, put, delete
import bottle.ext.sqlite


app = Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile = 'movies.db')
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


@app.post('/movies')
def create(db):
    data = request.json
    query = gen_ins('movies', list(data.keys()), list(data.values()))
    db.execute(query)
    return '<p>The new movie was added to the database.</p>'    


@app.get('/movies')
def retrieve(db): 
    query_string = request.query
    if not query_string:
        data = db.execute("SELECT * FROM movies").fetchall()
        return template('make_table', rows = data)
    else:
        query = gen_ret('movies', query_string)
        data = db.execute(query).fetchall()
        return template('make_table', rows = data)


@app.put('/movies/<uid:int>')
def update(uid, db):
    data = request.json 
    query = gen_upt('movies', data, {'uid': uid})
    db.execute(query)
    return '<p> The movie with original uid %d was updated.</p>'%uid


@app.delete('/movies/<uid:int>')
def delete(uid, db):
    db.execute("DELETE FROM movies WHERE uid LIKE ?",
              (uid,))
    return '<p> The movie with uid %d was deleted from the database.</p>'%uid


if __name__ == '__main__':
    run(app) 
