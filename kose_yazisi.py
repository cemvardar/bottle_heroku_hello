import urllib2
from HtmlAndTextParseHelper import strip_tags
from bottle import template
from bs4 import BeautifulSoup
from bson import ObjectId
from mongolab_helper import get_collection, SimpleQuery, get_date_username, find_one, insert, remove
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


def get_yazilar(user_name):
    s = SimpleQuery('yazilar')
    archive_rows = s.get_data(['author', 'date', 'title', '_id', 'keywords', 'url', 'gazete'], {'user_name': user_name})
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
    new_rows = s.get_data(['author', 'date', 'title', '_id', 'keywords', 'url', 'gazete'], {'user_name': date_user})
    while len(new_rows) == 0 and daysToGoBack < 7:
        daysToGoBack += 1
        date_user = get_date_username(daysToGoBack)
        new_rows = s.get_data(['author', 'date', 'title', '_id', 'keywords', 'url','gazete'], {'user_name': date_user})

    for row in new_rows:
        row[2] = template('link', url=row[5], link_text=row[2])
        row[3] = template('add_button', url=row[5], user_name=user_name)
        keywordsListEncoded = []
        for word in row[4]:
            keywordsListEncoded.append(word.encode('utf-8'))
        row[4] = keywordsListEncoded
    return archive_rows, new_rows

