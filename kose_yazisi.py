from collections import defaultdict
import urllib2
from HtmlAndTextParseHelper import strip_tags, get_gazete_name, get_html_from_url
from HurriyetReader import HurriyetReader
from RadikalReader import RadikalReader
from SimpleQuery import SimpleQuery
from ZamanReader import ZamanReader
from bottle import template
from bson import ObjectId
from mongolab_helper import get_collection, get_date_username, find_one, insert, remove, upsert

__author__ = 'cvardar'

def get_contained_keywords(yazi, keywords):
    wordSet = set(strip_tags(yazi['content']).lower().split())
    contained_keywords = set([])
    for kw in keywords:
        if kw in wordSet:
            contained_keywords.add(kw)
    return contained_keywords


def get_yazi_json(url):
    try:
        print url
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return {}
        else:
            raise
    html = response.read()
    try:
        return get_gazete_reader(url).get_doc_from_html(html,url)
    except:
        print url
        return {}

def get_yazilar_collection():
    return get_collection('yazilar')


def upsert_doc_into_yazilar(json_doc, user_name='cem'):
    json_doc['user_name'] = user_name
    keywordsDoc = find_one('keywords', {'user_name': user_name})
    if keywordsDoc:
        containedKeywords = get_contained_keywords(json_doc, keywordsDoc['include'])
        json_doc['keywords'] = list(containedKeywords)
    query = {'url': json_doc['url'], 'user_name': user_name}
    upsert('yazilar', query, json_doc)


def delete_doc_from_yazilar(object_id, user_name):
    query = {'_id': ObjectId(object_id), 'user_name': user_name}
    remove('yazilar', query)


def delete_doc_from_yazilar_url(url, user_name):
    query = {'url': url, 'user_name': user_name}
    remove('yazilar', query)


def get_value_if_exists(document, fieldName):
    if fieldName in document:
        return document[fieldName]
    else:
        return ''


def link_cell(doc):
    url = get_value_if_exists(doc, 'url')
    url_text = get_value_if_exists(doc, 'title')
    link_cell = template('link', url=url, link_text=url_text)
    return link_cell


def actions_cell_new_row(doc, user_name='cem'):
    object_id = get_value_if_exists(doc, '_id')
    url = get_value_if_exists(doc, 'url')
    actionsCell= template('add_button', url=url, user_name=user_name)
    data = {}
    data['form_id'] = "silFormHidden"
    data['object_id'] = object_id
    data['user_id'] = user_name
    data['url'] = url
    return actionsCell + template('delete_button', data=data, form_id="silFormHidden", object_id=object_id, user_name=user_name)



def actions_cell_archive_row(doc, user_name='cem', form_id='silForm'):
    object_id = get_value_if_exists(doc, '_id')
    actionsCell = template('goster_button', object_id=object_id, user_name=user_name)
    data = {}
    data['form_id'] = form_id
    data['object_id'] = object_id
    data['user_id'] = user_name
    data['url'] = get_value_if_exists(doc, 'url')
    return actionsCell + template('delete_button', data = data, form_id=form_id, object_id=object_id, user_name=user_name)


def keywords_cell(doc):
    keywordsListEncoded = []
    keywords_from_db = get_value_if_exists(doc, 'keywords')
    for word in keywords_from_db:
        keywordsListEncoded.append(word.encode('utf-8'))
    return str(keywordsListEncoded)


def get_most_recent_docs(s):
    new_docs = s.get_docs(get_username_query(get_current_user_name()))
    return list(new_docs)

def get_current_user_name(collectionName='scrape_log'):
    doc = get_collection(collectionName).find_one(sort=[('date', -1)])
    return doc['user_name']

def get_archive_docs_list(s, user_name_query):
    retList =[]
    for doc in s.get_docs(user_name_query):
        retList.append(doc)
    return retList


def get_username_query(user_name):
    return {'user_name': user_name}


def archive_rows_for_html(archive_docs_list, user_name):
    archive_rows = []
    for doc in archive_docs_list:
        doc_row = []
        doc_row.append(get_author_plus_date(doc))
        doc_row.append(link_cell(doc))
        doc_row.append(get_archive_actions_plus_gazete_image(doc, user_name))
        archive_rows.append(doc_row)
    if len(archive_rows) >0:
        return archive_rows
    else:
        return [["Buraya surukleyerek arsivlemeye baslayabilirsiniz"]]

def get_archive_actions_plus_gazete_image(doc, user_name):
    image_html = get_gazete_image_html(doc)
    archiveAction = actions_cell_archive_row(doc, user_name)
    return image_html + archiveAction


def most_recent_rows_for_html(most_recent_docs_list, user_name, other_docs):
    new_rows = []
    for doc in most_recent_docs_list:
        key = get_key(doc)
        if key in other_docs:
            continue
        doc_row = []
        doc_row.append(get_author_plus_date(doc))
        doc_row.append(link_cell(doc))

        doc_row.append(get_most_recent_actions_plus_gazete_image(doc, user_name))
        # doc_row.append(actions_cell_new_row(doc, user_name))
        # doc_row.append(get_gazete_image_html(doc))
        doc_row.append(get_value_if_exists(doc, 'url'))
        new_rows.append(doc_row)
    return new_rows

def get_most_recent_actions_plus_gazete_image(doc, user_name):
    mostRecentAction = actions_cell_new_row(doc, user_name)
    image_html = get_gazete_image_html(doc)
    return  image_html + mostRecentAction

def get_author_plus_date(doc):
    authorText = get_value_if_exists(doc, 'author')
    dateText = get_value_if_exists(doc, 'date')
    return authorText + "--" + dateText


def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    archive_docs_list = get_archive_docs_list(s, get_username_query(user_name))
    most_recent_docs_list = get_most_recent_docs(s)

    authorCounts = defaultdict(int)

    counter = {}
    for doc in archive_docs_list:
        authorCounts[doc['author']]+=1
        key = get_key(doc)
        if key not in counter:
            counter[key] = doc

    most_recent_docs_list.sort( key=lambda x: -(authorCounts[x['author']]))
    titles = ['yazar', 'tarih', 'baslik', 'action', 'keywords', 'gazete']
    archive_rows = archive_rows_for_html(archive_docs_list, user_name)
    new_rows = most_recent_rows_for_html(most_recent_docs_list, user_name, counter)

    return titles, archive_rows, new_rows

def get_gazete_image_html(doc):
    gazete_name = get_value_if_exists(doc, 'gazete')
    if gazete_name =='Hurriyet':
        return "<img src='/hurriyet_logo.jpg' alt='some_text'>"
    if gazete_name =='Radikal':
        return "<img src='/radikal_logo.jpg' alt='some_text'>"
    if gazete_name =='Zaman':
        return "<img src='/zaman_logo.jpg' alt='some_text'>"
    return ''


def get_gazete_reader(url):
    gazete_name = get_gazete_name(url)
    if gazete_name =='hurriyet':
        return HurriyetReader()
    if gazete_name =='radikal':
        return RadikalReader()
    if gazete_name =='zaman':
        return ZamanReader()

def get_yazi_links_from_url(url):
    html = get_html_from_url(url)
    return get_gazete_reader(url).get_yazi_links(html)

def get_key(doc):
    key = HashableDict()
    key['author'] = doc['author']
    key['date'] = doc['date']
    key['title'] = doc['title']
    return key

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))