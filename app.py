import os
from bottle import route, run, template, post, request, get
import pymongo
from pymongo import MongoClient


def get_names_collection():
    mongodb_uri = "mongodb://heroku_hello:HerokuHello75@ds053937.mongolab.com:53937/cem_heroku_hello"
    db_name = 'cem_heroku_hello'
    try:
        connection = pymongo.Connection(mongodb_uri)
        # connection = MongoClient()
        database = connection[db_name]
    except:
        print('Error: Unable to connect to database.')
        connection = None
    names_collection = database.names
    return names_collection


def get_names():
    names_collection = get_names_collection()

    if names_collection is not None:

        # To begin with, we'll add a few adventurers to the database. Note that
        # nothing is required to create the adventurers collection--it is
        # created automatically when we insert into it. These are simple JSON
        # objects.
        #
        # database.names.insert({'name': 'liplip', 'lastname': 'tikir'})
        namesCursor = names_collection.find()
        rows = []
        for names in namesCursor:
            n = names['name']
            l = names['lastname']
            rows.append([n,l])
        return rows

@route('/hello/:name')
def index(name='World'):
    return '<b>Hello Cem %s!</b>' % name

@get('/')
def index2():
    titles = ['isim', 'soyadi']
    items= get_names()
    return template('make_table', titles=titles, rows=items)

@post('/', method='POST')
def login_submit():
    name     = request.forms.get('name')
    lastname = request.forms.get('lastname')
    newRecord = {"name":name, "lastname":lastname}
    names_collection = get_names_collection()
    names_collection.insert(newRecord)
    return index2()

items = {1: 'first item', 2: 'second item'}

# a simple json test main page
@route('/json')
def jsontest():
    return template('json')

@route('/chart')
def jsontest():
    return template('chart')

@route('/getallitems.json')
def shop_aj_getallitems():
    names = get_names()
    cnt=1
    json = {}
    for i in names:
        json[cnt] = i[0] + ' ' + i[1]
        cnt+=1
    return (json)

if __name__ == '__main__':
    # Get required port, default to 5000.
    port = os.environ.get('PORT', 5000)

    # Run the app.
    run(host='0.0.0.0', port=port)
