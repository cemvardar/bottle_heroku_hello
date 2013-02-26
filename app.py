import gviz_api
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

@route('/chartdata')
def jsonchartdata():
    description = {"year": ("string", "Year"),
                   "Austria": ("number", "Austria"),
                   "Bulgaria": ("number", "Bulgaria"),
                   "Denmark": ("number", "Denmark")}
    data = [{"year": "2003", "Austria": 1336060, "Bulgaria": 400361, "Denmark":1001582},
            {"year": "2004", "Austria": 1538156, "Bulgaria": 366849, "Denmark":1119450},
            {"year": "2005", "Austria": 1576579, "Bulgaria": 440514, "Denmark":993360}]

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table.ToJSon(columns_order=("year", "Austria", "Bulgaria", "Denmark"))
    # return data_table.ToJSonResponse(columns_order=("year", "Austria", "Bulgaria", "Denmark"),
    #                                 order_by="Austria")

    # return [
    #     ['Year', 'Austria', 'Bulgaria', 'Denmark', 'Greece'],
    #     ['2003',  1336060,    400361,    1001582,   997974],
    #     ['2004',  1538156,    366849,    1119450,   941795],
    #     ['2005',  1576579,    440514,    993360,    930593],
    #     ['2006',  1600652,    434552,    1004163,   897127],
    #     ['2007',  1968113,    393032,    979198,    1080887],
    #     ['2008',  1901067,    517206,    916965,    1056036]
    # ]

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
