import urllib2
from bs4 import BeautifulSoup
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
    # print tarih
    yazarName = soup.find('div', attrs={'class': 'YazarNameContainer_2'}).find('a').text
    yazi['author'] = yazarName

    # print yazarName
    yaziContent = soup.find("div", {"id": "YazarDetayText"})
    title = yaziContent.find('span').text
    yazi['content'] = unicode(yaziContent)
    yazi['title'] = title
    return yazi


def get_yazilar_collection():
    return get_collection('yazilar')
    # connection = MongoClient()
    # db = connection['kose_yazilari']
    # yazilar = db['yazilar']
    # return yazilar

def insert_doc_into_yazilar(json_doc):
    yazilar = get_yazilar_collection()
    yazilar.ensure_index([('author', 1), ('date', 1)])
    yazilar.insert(json_doc)
