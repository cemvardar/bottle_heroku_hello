from gevent import monkey; monkey.patch_all()
import datetime
from KelimelerPage import get_kelimeler_content, insert_new_keyword, delete_keyword
from SimpleQuery import SimpleQuery
# from gevent import monkey; monkey.patch_all()
import gviz_api
from kose_yazisi import get_yazi_json, upsert_doc_into_yazilar, delete_doc_from_yazilar, get_yazilar, delete_doc_from_yazilar_url
from mongolab_helper import get_commutes_collection
import os
from bottle import route, run, template, post, request, get, redirect, static_file
from yazi_crawler import get_daily_links_from_newspapers, get_articles_from_newspapers


def get_names():
    s = SimpleQuery('names')
    return s.get_docs()


def get_commutes():
    s = SimpleQuery('commutes')
    return s.get_data_as_list_of_lists(['date', 'duration'])


def get_yazi_content(user_name, object_id):
    s = SimpleQuery('yazilar')
    query = {'user_name': user_name, '_id': object_id}
    return s.get_first_doc(query)


@route('/koseyazisi/:user_name/tile')
def koseyazisi_show(user_name='cem'):
    rows, rows_new = get_yazilar(user_name)
    gazeteler = ['Hurriyet', 'Radikal', 'Zaman']
    return template('tiles', rows=rows, rows_new= rows_new, user_name=user_name , gazeteler = gazeteler)


@route('/koseyazisi/:user_name')
def koseyazisi_show(user_name='cem'):
    rows, rows_new = get_yazilar(user_name)
    return template('kose_yazisi', titles=[], rows=rows, rows_new= rows_new, user_name=user_name)


@post('/koseyazisi/:user_name')
def save_new_koseyazisi(user_name='cem'):
    url = request.forms.get('url')
    upsert_doc_into_yazilar(get_yazi_json(url), user_name)
    redirect('/koseyazisi/' + user_name + '/tile')


@post('/koseyazisi/:user_name/sil')
def delete_kose_yazisi(user_name='cem'):
    object_id = request.forms.get('url')
    delete_doc_from_yazilar_url(object_id, user_name)
    redirect('/koseyazisi/' + user_name + '/tile')


@post('/koseyazisi/:user_name/goster')
def show_kose_yazisi(user_name='cem'):
    object_id = request.forms.get('object_id')
    yazi_doc = get_yazi_content(user_name, object_id)
    return template('kose_yazisi_goster', author=yazi_doc['author'], date=yazi_doc['date'], content=yazi_doc['content'])


@route('/koseyazisi/:user_name/keywords')
def show_keywords(user_name='cem'):
    kelimeler = get_kelimeler_content(user_name)
    return template('kelimeler', titles=['keywords', 'action'], rows=kelimeler, user_name=user_name, collection_name='keywords')


@post('/koseyazisi/:user_name/keywords')
def save_new_keyword(user_name='cem'):
    yeniKelime = request.forms.get('kelime')
    insert_new_keyword(yeniKelime, user_name)
    redirect('/koseyazisi/' + user_name + '/keywords')

@post('/koseyazisi/:user_name/keywords_sil')
def save_new_keyword(user_name='cem'):
    yeniKelime = request.forms.get('object_id')
    delete_keyword(yeniKelime, user_name)
    redirect('/koseyazisi/' + user_name + '/keywords')

@route('/koseyazisi/:user_name/corpus_keywords')
def show_keywords(user_name='cem'):
    kelimeler = get_kelimeler_content(user_name, 'corpus_keywords')
    return template('kelimeler', titles=['keywords', 'action'], rows=kelimeler, user_name=user_name, collection_name='corpus_keywords')


@post('/koseyazisi/:user_name/corpus_keywords')
def save_new_keyword(user_name='cem'):
    yeniKelime = request.forms.get('kelime')
    insert_new_keyword(yeniKelime, user_name, 'corpus_keywords')
    redirect('/koseyazisi/' + user_name + '/corpus_keywords')

@post('/koseyazisi/:user_name/corpus_keywords_sil')
def save_new_keyword(user_name='cem'):
    yeniKelime = request.forms.get('object_id')
    delete_keyword(yeniKelime, user_name, 'corpus_keywords')
    redirect('/koseyazisi/' + user_name + '/corpus_keywords')

@get('/')
def index():
    redirect('/koseyazisi/cem')

@get('/crawl_newspapers')
def crawl():
    get_daily_links_from_newspapers()
    return get_articles_from_newspapers()

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

# a simple json test main page
@route('/json')
def jsontest():
    return template('json')


@route('/commutes')
def commutes():
    titles = ['Commute Date', 'duration']
    items = get_commutes()
    return template('commutes', titles=titles, rows=items)


@post('/commutes', method='POST')
def save_new_commute():
    date_string = request.forms.get('date')
    duration = request.forms.get('duration')
    date = datetime.datetime.strptime(date_string, '%m/%d/%Y')
    newRecord = {"date": date, "duration": int(duration)}
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
    data = [{"year": "2003", "Austria": 1336060, "Bulgaria": 400361, "Denmark": 1001582},
            {"year": "2004", "Austria": 1538156, "Bulgaria": 366849, "Denmark": 1119450},
            {"year": "2005", "Austria": 1576579, "Bulgaria": 440514, "Denmark": 993360}]

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
        data.append({"date": date, "duration": int(duration)})
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table.ToJSon(columns_order=("date", "duration"))


@route('/getallitems.json')
def shop_aj_getallitems():
    names = get_names()
    cnt = 1
    json = {}
    for i in names:
        json[cnt] = i['name'] + ' ' + i['lastname']
        cnt += 1
    return (json)


if __name__ == '__main__':
    # Get required port, default to 5000.
    port = os.environ.get('PORT', 5000)

    # Run the app.
    # bottle.run(server='gevent', port=os.environ.get('PORT', 5000))
    run(server='gevent', host='0.0.0.0', port=port)
