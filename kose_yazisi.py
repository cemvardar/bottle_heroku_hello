import urllib2
from HtmlAndTextParseHelper import strip_tags
from bottle import template
from bs4 import BeautifulSoup
from bson import ObjectId
from mongolab_helper import get_collection, SimpleQuery, get_date_username, find_one, insert, remove, get_docs
import urlparse
__author__ = 'cvardar'

def get_gazete_name(url):
    parse_object = urlparse.urlparse(url)
    address = parse_object.netloc
    return address.replace('.tr', '').replace('.com','').replace('www.', '')

def get_yazi_from_html(html, url):
    soup = BeautifulSoup(html)
    yazi = {}
    yazi['gazete'] = get_gazete_name(url)
    yazi['url'] = url
    tarih = soup.find('div', attrs={'class': 'tarihSp FL'}).text
    yazi['date'] = tarih
    yazarName = soup.find('div', attrs={'class': 'YazarNameContainer_2'}).find('a').text
    yazi['author'] = yazarName
    yaziContent = soup.find("div", {"id": "YazarDetayText"})
    title = yaziContent.find('span').text
    yazi['content'] = unicode(yaziContent)
    yazi['title'] = title
    return yazi


def get_contained_keywords(yazi, keywords):
    wordSet = set(strip_tags(yazi['content']).lower().split())
    contained_keywords = set([])
    for kw in keywords:
        if kw in wordSet:
            contained_keywords.add(kw)
    return contained_keywords


def get_yazi_json(url):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return {}
        else:
            raise
    html = response.read()
    return get_yazi_from_html(html, url)


def get_yazilar_collection():
    return get_collection('yazilar')


def insert_doc_into_yazilar(json_doc, user_name='cem'):
    json_doc['user_name'] = user_name
    keywordsDoc = find_one('keywords', {'user_name': user_name})
    if keywordsDoc:
        containedKeywords = get_contained_keywords(json_doc, keywordsDoc['include'])
        json_doc['keywords'] = list(containedKeywords)
    insert('yazilar', json_doc)


def delete_doc_from_yazilar(object_id, user_name):
    query = {'_id': ObjectId(object_id), 'user_name': user_name}
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
    url = get_value_if_exists(doc, 'url')
    return template('add_button', url=url, user_name=user_name)

def actions_cell_archive_row(doc, user_name='cem'):
    object_id = get_value_if_exists(doc, '_id')
    actionsCell = template('goster_button', object_id=object_id, user_name=user_name)
    return actionsCell + template('delete_button', object_id=object_id, user_name=user_name)


def keywords_cell(doc):
    keywordsListEncoded = []
    keywords_from_db = get_value_if_exists(doc, 'keywords')
    for word in keywords_from_db:
        keywordsListEncoded.append(word.encode('utf-8'))
    return str(keywordsListEncoded)


def get_most_recent_docs(s):
    daysToGoBack = 0
    date_user = get_date_username(daysToGoBack)
    new_docs = s.get_docs({'user_name': date_user})
    while not new_docs and daysToGoBack < 7:
        daysToGoBack += 1
        date_user = get_date_username(daysToGoBack)
        new_docs = s.get_docs({'user_name': date_user})
    return new_docs


def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    titles = ['yazar', 'tarih', 'baslik', 'action', 'keywords', 'gazete']
    user_name_query = {'user_name': user_name}
    archive_rows = []
    for doc in s.get_docs(user_name_query):
        doc_row = []
        doc_row.append(get_value_if_exists(doc,'author'))
        doc_row.append(get_value_if_exists(doc,'date'))
        doc_row.append(link_cell(doc))
        doc_row.append(actions_cell_archive_row(doc, user_name))
        doc_row.append(keywords_cell(doc))
        doc_row.append(get_value_if_exists(doc, 'gazete'))
        archive_rows.append(doc_row)

    new_rows = []

    for doc in get_most_recent_docs(s):
        doc_row = []
        doc_row.append(get_value_if_exists(doc,'author'))
        doc_row.append(get_value_if_exists(doc,'date'))
        doc_row.append(link_cell(doc))
        doc_row.append(actions_cell_new_row(doc, user_name))
        doc_row.append(keywords_cell(doc))
        doc_row.append(get_value_if_exists(doc, 'gazete'))
        new_rows.append(doc_row)

    return titles, archive_rows, new_rows

def get_yazilar_old(user_name):
    s = SimpleQuery('yazilar')
    titles = ['yazar', 'tarih', 'baslik', 'action', 'keywords', 'link', 'gazete']
    mongo_fields_needed = ['author', 'date', 'title', '_id', 'keywords', 'url', 'gazete']
    user_name_query = {'user_name': user_name}
    archive_rows = s.get_data(mongo_fields_needed, user_name_query)
    for row in archive_rows:
        row[2] = template('link', url=row[5], link_text=row[2])
        actionsCell = template('goster_button', object_id=row[3], user_name=user_name)
        row[3] = actionsCell + template('delete_button', object_id=row[3], user_name=user_name)
        keywordsListEncoded = []
        for word in row[4]:
            keywordsListEncoded.append(word.encode('utf-8'))
        row[4] = str(keywordsListEncoded)
    daysToGoBack = 0
    date_user = get_date_username(daysToGoBack)
    new_rows = s.get_data(mongo_fields_needed, {'user_name': date_user})
    while len(new_rows) == 0 and daysToGoBack < 7:
        daysToGoBack += 1
        date_user = get_date_username(daysToGoBack)
        new_rows = s.get_data(mongo_fields_needed, {'user_name': date_user})

    for row in new_rows:
        row[2] = template('link', url=row[5], link_text=row[2])
        row[3] = template('add_button', url=row[5], user_name=user_name)
        keywordsListEncoded = []
        for word in row[4]:
            keywordsListEncoded.append(word.encode('utf-8'))
        row[4] = keywordsListEncoded

    return titles, archive_rows, new_rows

