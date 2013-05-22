from HtmlAndTextParseHelper import get_unicode
from bottle import template
from mongolab_helper import SimpleQuery, upsert, find_one

__author__ = 'cvardar'

def get_kelimeler_content(user_name, collection_name='keywords'):
    s = SimpleQuery(collection_name)
    query = {'user_name': user_name}
    content = s.get_data(['user_name', 'include'], query)
    kelimeler = []
    if content:
        for i in content[0][1]:
            delete_button = template('delete_keyword_button', object_id=i, user_name=user_name, collection_name= collection_name)
            kelimeler.append([i, delete_button])
    return kelimeler

def insert_new_keyword(yeniKelime, userName='cem', collection_name='keywords'):
    newWordUnicode = get_unicode(yeniKelime).lower()
    record = find_one(collection_name, {'user_name': userName})
    if record:
        keywords = record['include']
        keywords.append(newWordUnicode)
    else:
        keywords = [newWordUnicode]
    upsert(collection_name,{'user_name': userName}, {'$set': {'include': keywords}})


def delete_keyword(kelime, userName='cem', collection_name='keywords'):
    newWordUnicode = get_unicode(kelime).lower()
    record = find_one(collection_name, {'user_name': userName})
    if record:
        keywords = record['include']
        if newWordUnicode in keywords:
            keywords.remove(newWordUnicode)
            upsert(collection_name,{'user_name': userName}, {'$set': {'include': keywords}})
