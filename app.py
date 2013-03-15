import gviz_api
from mongolab_helper import get_names_collection
import os
from bottle import route, run, template, post, request, get

def get_names():
    names_collection = get_names_collection()
    if names_collection is not None:
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

# a simple json test main page
@route('/json')
def jsontest():
    return template('json')

@route('/commutes')
def commutes():
    return template('commutes')

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
