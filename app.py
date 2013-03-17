import datetime
import gviz_api
from kose_yazisi import get_yazi_json, insert_doc_into_yazilar, get_yazilar_collection, delete_doc_from_yazilar
from mongolab_helper import get_names_collection, get_commutes_collection, SimpleQuery, get_data_from_collection
import os
from bottle import route, run, template, post, request, get, redirect


def get_names():
    s = SimpleQuery('names')
    return s.get_data(['name','lastname'])

def get_commutes():
    s = SimpleQuery('commutes')
    return s.get_data(['date','duration'])

def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    return s.get_data(['author', 'date','title', '_id'], {'user_name':user_name})

@route('/koseyazisi/:user_name')
def koseyazisi_show(user_name='cem'):
    titles=['yazar','tarih','baslik','action']
    rows=get_yazilar(user_name)
    for row in rows:
        row[3] = (template('delete_botton', object_id=row[3], user_name=user_name))
    return template('kose_yazisi', titles=titles, rows=rows, user_name=user_name)

@post('/koseyazisi/:user_name')
def save_new_koseyazisi(user_name='cem'):
    url     = request.forms.get('url')
    insert_doc_into_yazilar(get_yazi_json(url), user_name)
    redirect('/koseyazisi/'+user_name)

@post('/koseyazisi/:user_name/sil')
def delete_kose_yazisi(user_name='cem'):
    object_id= request.forms.get('object_id')
    delete_doc_from_yazilar(object_id, user_name)
    redirect('/koseyazisi/'+user_name)

@get('/')
def show_names():
    titles = ['isim', 'soyadi']
    items= get_names()
    return template('make_table', titles=titles, rows=items)

@post('/', method='POST')
def save_new_name():
    name     = request.forms.get('name')
    lastname = request.forms.get('lastname')
    newRecord = {"name":name, "lastname":lastname}
    names_collection = get_names_collection()
    names_collection.insert(newRecord)
    return show_names()

# a simple json test main page
@route('/json')
def jsontest():
    return template('json')

@route('/commutes')
def commutes():
    titles = ['Commute Date', 'duration']
    items= get_commutes()
    return template('commutes', titles=titles, rows=items)

@post('/commutes', method='POST')
def save_new_commute():
    date_string = request.forms.get('date')
    duration = request.forms.get('duration')
    date = datetime.datetime.strptime(date_string,'%m/%d/%Y')
    newRecord = {"date":date, "duration":int(duration)}
    commutes_collection = get_commutes_collection()
    commutes_collection.insert(newRecord)
    return commutes()

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

@route('/commutedata')
def jsoncommutechartdata():
    commutes = get_commutes()
    description = {"date": ("string", "Date"),
                   "duration": ("number", "Duration")}
    data = []
    for (date, duration) in commutes:
        data.append({"date": date, "duration":int(duration)})
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table.ToJSon(columns_order=("date", "duration"))

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
