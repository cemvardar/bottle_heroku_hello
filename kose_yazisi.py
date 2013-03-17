import urllib2
from bs4 import BeautifulSoup
from bson import ObjectId
from mongolab_helper import get_collection
from pymongo import MongoClient

__author__ = 'cvardar'

def get_yazi_json(url):
    yazi={}
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    tarih = soup.find('div', attrs={'class': 'tarihSp FL'}).text
    yazi['date'] = tarih
    yazarName = soup.find('div', attrs={'class': 'YazarNameContainer_2'}).find('a').text
    yazi['author'] = yazarName

    yaziContent = soup.find("div", {"id": "YazarDetayText"})
    title = yaziContent.find('span').text
    yazi['content'] = unicode(yaziContent)
    yazi['title'] = title
    return yazi


def get_yazilar_collection():
    return get_collection('yazilar')

def insert_doc_into_yazilar(json_doc, user_name='cem'):
    yazilar = get_yazilar_collection()
    yazilar.ensure_index([('user_name', 1),('author', 1), ('date', 1)])
    json_doc['user_name'] = user_name
    yazilar.insert(json_doc)

def delete_doc_from_yazilar(object_id, user_name):
    yazilar = get_yazilar_collection()
    yazilar.ensure_index([('author', 1), ('date', 1)])
    yazilar.remove({'_id': ObjectId(object_id) , 'user_name': user_name})
