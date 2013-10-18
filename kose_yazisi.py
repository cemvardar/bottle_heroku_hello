from collections import defaultdict
import urllib2
import time
from HtmlAndTextParseHelper import strip_tags, get_gazete_name, get_html_from_url
from HurriyetReader import HurriyetReader
from RadikalReader import RadikalReader
from SimpleQuery import SimpleQuery
from SozcuReader import SozcuReader
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
    print url
    html = try_10_times(url)
    if html:
        return get_gazete_reader(url).get_doc_from_html(html,url)
    print url
    return {}

def try_10_times(url):
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
        ]
        for i in range(10):
            # choice1 = choice(user_agents)
            choice1 = user_agents[i % 6]
            # print choice1

            headers = {'User-Agent': choice1}
            req = urllib2.Request(url, None, headers)
            try:
                html = urllib2.urlopen(req).read()
                return html
            except:
                time.sleep(3)
                pass

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
    data = {'form_id': "silFormHidden",
            'object_id': object_id,
            'user_id': user_name,
            'url': url}
    return actionsCell + template('delete_button', data=data)



def actions_cell_archive_row(doc, user_name='cem', form_id='silForm'):
    object_id = get_value_if_exists(doc, '_id')
    actionsCell = template('goster_button', object_id=object_id, user_name=user_name)
    data = {'form_id': form_id,
            'object_id': object_id,
            'user_id': user_name,
            'url': get_value_if_exists(doc, 'url')}
    return actionsCell + template('delete_button', data = data)


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
    archive_rows = DocRowContainer()
    for doc in archive_docs_list:
        doc_row = DocRow(doc)
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


def most_recent_rows_for_html(most_recent_docs_list, user_name, archive_docs_keys):
    new_rows = DocRowContainer()
    for doc in most_recent_docs_list:
        key = get_key(doc)
        if key in archive_docs_keys:
            continue
        doc_row = DocRow(doc)
        doc_row.append(get_author_plus_date(doc))
        doc_row.append(link_cell(doc))
        doc_row.append(get_most_recent_actions_plus_gazete_image(doc, user_name))
        new_rows.append(doc_row)
    return new_rows

class DocRowContainer(list):
    def __init__(self):
        self.newspapers = set([])
    def append(self, docRow):
        self.newspapers.add(docRow.gazete)
        super(DocRowContainer, self).append(docRow)

class DocRow(list):
    def __init__(self, doc):
        self.url = get_value_if_exists(doc, 'url')
        self.gazete = get_value_if_exists(doc, 'gazete')

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

    docsInArchive = {}
    for doc in archive_docs_list:
        authorCounts[doc['author']]+=1
        key = get_key(doc)
        if key not in docsInArchive:
            docsInArchive[key] = doc

    most_recent_docs_list.sort( key=lambda x: -(authorCounts[x['author']]))
    archive_rows = archive_rows_for_html(archive_docs_list, user_name)
    new_rows = most_recent_rows_for_html(most_recent_docs_list, user_name, docsInArchive)

    return archive_rows, new_rows

def get_gazete_image_html(doc):
    gazete_name = get_value_if_exists(doc, 'gazete')
    if gazete_name =='Hurriyet':
        return "<img src='/hurriyet_logo.jpg' alt='some_text'>"
    if gazete_name =='Radikal':
        return "<img src='/radikal_logo.jpg' alt='some_text'>"
    if gazete_name =='Zaman':
        return "<img src='/zaman_logo.jpg' alt='some_text'>"
    if gazete_name =='Sozcu':
        return "<img src='/sozcu_logo.jpg' alt='some_text'>"
    return ''


def get_gazete_reader(url):
    gazete_name = get_gazete_name(url)
    if gazete_name =='hurriyet':
        return HurriyetReader()
    if gazete_name =='radikal':
        return RadikalReader()
    if gazete_name =='zaman':
        return ZamanReader()
    if gazete_name =='sozcu':
        return SozcuReader()

def get_yazi_links_from_url(url):
    html = try_10_times(url)
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