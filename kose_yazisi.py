import urllib2
from bottle import template
from bs4 import BeautifulSoup
from bson import ObjectId
from mongolab_helper import get_collection, SimpleQuery
from pymongo import MongoClient

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
    yazilar.insert(json_doc)

def insert_keyword_into_keywords(json_doc, user_name='cem'):
    yazilar =  get_collection('keywords')
    yazilar.ensure_index([('user_name', 1)])
    json_doc['user_name'] = user_name
    yazilar.insert(json_doc)


def delete_doc_from_yazilar(object_id, user_name):
    yazilar = get_yazilar_collection()
    yazilar.ensure_index([('author', 1), ('date', 1)])
    yazilar.remove({'_id': ObjectId(object_id) , 'user_name': user_name})

def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    rows = s.get_data(['author', 'date', 'title', '_id', 'url'], {'user_name': user_name})
    for row in rows:
        row[2] = (template('link', url=row[4], link_text=row[2]))
        row[3] = (template('delete_botton', object_id=row[3], user_name=user_name))
    return rows