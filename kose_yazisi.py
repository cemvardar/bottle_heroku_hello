from collections import defaultdict
import urllib2
from HtmlAndTextParseHelper import strip_tags, get_gazete_reader
from bottle import template
from bson import ObjectId
from mongolab_helper import get_collection, SimpleQuery, get_date_username, find_one, insert, remove

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
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return {}
        else:
            raise
    html = response.read()
    return get_gazete_reader(url).get_doc_from_html(html,url)


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
    new_docs = s.get_docs(get_username_query(date_user))
    while new_docs.count() == 0 and daysToGoBack < 7:
        daysToGoBack += 1
        date_user = get_date_username(daysToGoBack)
        new_docs = s.get_docs(get_username_query(date_user))
    return list(new_docs)


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
        doc_row.append(get_value_if_exists(doc, 'author'))
        doc_row.append(get_value_if_exists(doc, 'date'))
        doc_row.append(link_cell(doc))
        doc_row.append(actions_cell_archive_row(doc, user_name))
        doc_row.append(keywords_cell(doc))
        doc_row.append(get_value_if_exists(doc, 'gazete'))
        archive_rows.append(doc_row)
    return archive_rows


def most_recent_rows_for_html(most_recent_docs_list, user_name):
    new_rows = []
    for doc in most_recent_docs_list:
        doc_row = []
        doc_row.append(get_value_if_exists(doc, 'author'))
        doc_row.append(get_value_if_exists(doc, 'date'))
        doc_row.append(link_cell(doc))
        doc_row.append(actions_cell_new_row(doc, user_name))
        doc_row.append(keywords_cell(doc))
        doc_row.append(get_value_if_exists(doc, 'gazete'))
        new_rows.append(doc_row)
    return new_rows


def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    archive_docs_list = get_archive_docs_list(s, get_username_query(user_name))
    most_recent_docs_list = get_most_recent_docs(s)

    authorCounts = defaultdict(int)
    for doc in archive_docs_list:
        authorCounts[doc['author']]+=1

    most_recent_docs_list.sort( key=lambda x: -(authorCounts[x['author']]))
    titles = ['yazar', 'tarih', 'baslik', 'action', 'keywords', 'gazete']
    archive_rows = archive_rows_for_html(archive_docs_list, user_name)
    new_rows = most_recent_rows_for_html(most_recent_docs_list, user_name)

    return titles, archive_rows, new_rows

