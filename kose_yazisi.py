import urllib2
from HtmlAndTextParseHelper import strip_tags
from bottle import template
from bs4 import BeautifulSoup
from bson import ObjectId
from mongolab_helper import get_collection, SimpleQuery, get_date_username

__author__ = 'cvardar'


def get_yazi_from_html(html, url):
    soup = BeautifulSoup(html)

    yazi = {}
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
    yazilar = get_yazilar_collection()
    yazilar.ensure_index([('user_name', 1),('author', 1), ('date', 1)])
    json_doc['user_name'] = user_name
    keywordsCollection =  get_collection('keywords')
    keywordsDoc = keywordsCollection.find_one({'user_name':user_name})
    if keywordsDoc:
        containedKeywords = get_contained_keywords(json_doc,keywordsDoc['include'])
        json_doc['keywords'] = list(containedKeywords)
    yazilar.insert(json_doc)

def insert_keyword_into_keywords(json_doc, user_name='cem'):
    keywordsCollection =  get_collection('keywords')
    keywordsCollection.ensure_index([('user_name', 1)])
    json_doc['user_name'] = user_name
    keywordsCollection.insert(json_doc)


def delete_doc_from_yazilar(object_id, user_name):
    yazilar = get_yazilar_collection()
    yazilar.ensure_index([('author', 1), ('date', 1)])
    yazilar.remove({'_id': ObjectId(object_id) , 'user_name': user_name})

def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    rows = s.get_data(['author', 'date', 'title', '_id', 'keywords', 'url'], {'user_name': user_name})
    my_authors = set([])
    for row in rows:
        my_authors.add(row[0])
        row[2] = template('link', url=row[5], link_text=row[2])
        actionsCell = template('goster_button', object_id=row[3], user_name=user_name)
        row[3] = actionsCell + template('delete_button', object_id=row[3], user_name=user_name)
        keywordsListEncoded = []
        for word in row[4]:
            keywordsListEncoded.append(word.encode('utf-8'))
        row[4] = keywordsListEncoded

    date_user= get_date_username()
    new_rows = s.get_data(['author', 'date', 'title', '_id', 'keywords', 'url'], {'user_name': date_user})

    new_rows_interesting = []
    new_rows_unrelated = []
    for row in new_rows:
        row[2] = template('link', url=row[5], link_text=row[2])
        # actionsCell = template('goster_button', object_id=row[3], user_name=user_name)
        # row[3] = actionsCell + template('delete_button', object_id=row[3], user_name=user_name)
        row[3] = 'YENI'
        keywordsListEncoded = []
        for word in row[4]:
            keywordsListEncoded.append(word.encode('utf-8'))
        row[4] = keywordsListEncoded
        # if(row[0] in my_authors):
    return rows, new_rows

