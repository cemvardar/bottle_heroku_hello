from unittest import TestCase
from mongolab_helper import get_collection
from HTMLParser import HTMLParser
__author__ = 'cvardar'

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class KeywordLookupTests(TestCase):
    def test_first(self):
        for i in get_collection('yazilar').find():
            print strip_tags(i['content'])

    def test_remove_all_keywords(self):
        keywordCollection = get_collection('keywords')
        # keywordCollection.remove()
    def test_insert_single_record_keywords(self):
        keywordCollection = get_collection('keywords')
        keywordCollection.insert({'user_name':'cem', 'include':[]})

    def test_insert_keywords(self):
        # get_collection('keywords').insert({'include':['bir', 'halk']})
        keywordCollection = get_collection('keywords')
        keywords = keywordCollection.find_one({'user_name':'cem'})['include']
        # keywords=['halk', 'millet', 'vatan', 'tayyip', 'bakan', 'tbmm']
        keywords+=['millet', 'tayyip']
        print keywords
        keywordCollection.update({'user_name':'cem'}, {'user_name':'cem', 'include': keywords},True)
        for i in keywordCollection.find():
        # for i in keywordCollection.find({'user_name':'cem'}):
            if 'user_name' in i:
                print i['user_name']
                print i['include']
        # for i in get_collection('yazilar').find():
        #     wordset = set(strip_tags(i['content']).lower().split())
        #     for kw in keywords:
        #         if kw in wordset:
        #             print kw

    # def test_insert_update(self):
