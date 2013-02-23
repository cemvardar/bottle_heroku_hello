import os
from bottle import route, run, template
import pymongo


def get_names():
    mongodb_uri = "mongodb://heroku_hello:HerokuHello75@ds053937.mongolab.com:53937/cem_heroku_hello"
    db_name = 'cem_heroku_hello'

    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
    except:
        print('Error: Unable to connect to database.')
        connection = None

    if connection is not None:

        # To begin with, we'll add a few adventurers to the database. Note that
        # nothing is required to create the adventurers collection--it is
        # created automatically when we insert into it. These are simple JSON
        # objects.
        #
        # database.names.insert({'name': 'liplip', 'lastname': 'tikir'})
        namesCursor = database.names.find()
        rows = []
        for names in namesCursor:
            n = names['name']
            l = names['lastname']
            rows.append([n,l])
        return rows

@route('/hello/:name')
def index(name='World'):
    return '<b>Hello Cem %s!</b>' % name

@route('/')
def index2():
    titles = ['isim', 'soyadi']
    # items = [['cem','vardar'], ['hulya','hisim']]
    items= get_names()
    return template('make_table', titles=titles, rows=items)



if __name__ == '__main__':
    # Get required port, default to 5000.
    port = os.environ.get('PORT', 5000)

    # Run the app.
    run(host='0.0.0.0', port=port)
