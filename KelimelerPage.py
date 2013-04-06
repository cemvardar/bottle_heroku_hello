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

def insert_new_keyword(yeniKelime):
    keywordCollection = get_collection('keywords')
    record = keywordCollection.find_one({'user_name': 'cem'})
    if record:
        keywords = record['include']
        keywords.append(yeniKelime)
    else:
        keywords = [yeniKelime]
    keywordCollection.update({'user_name': 'cem'}, {'$set': {'include': keywords}}, upsert=True)
