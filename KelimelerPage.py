from HtmlAndTextParseHelper import get_unicode
from mongolab_helper import SimpleQuery, get_collection

__author__ = 'cvardar'

def get_kelimeler_content(user_name):
    s = SimpleQuery('keywords')
    query = {'user_name': user_name}
    content = s.get_data(['user_name', 'include'], query)
    kelimeler = []
    if content:
        for i in content[0][1]:
            kelimeler.append([i])
    return kelimeler

def insert_new_keyword(yeniKelime, userName='cem'):
    newWordUnicode = get_unicode(yeniKelime).lower()
    keywordCollection = get_collection('keywords')
    record = keywordCollection.find_one({'user_name': userName})
    if record:
        keywords = record['include']
        keywords.append(newWordUnicode)
    else:
        keywords = [newWordUnicode]
    keywordCollection.update({'user_name': userName}, {'$set': {'include': keywords}}, upsert=True)
