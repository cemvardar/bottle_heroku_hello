from unittest import TestCase
from mongolab_helper import get_collection
from HTMLParser import HTMLParser
__author__ = 'cvardar'

class KeywordLookupTests(TestCase):
    def test_first(self):
        pass
        # for i in get_collection('yazilar').find():
        #     print strip_tags(i['content'])

    def test_remove_all_keywords(self):
        keywordCollection = get_collection('keywords')
        # keywordCollection.remove()
    def test_insert_single_record_keywords(self):
        keywordCollection = get_collection('keywords')
        # keywordCollection.insert({'user_name':'cem', 'include':[]})

    def test_insert_keywords(self):
        pass
        # get_collection('keywords').insert({'include':['bir', 'halk']})
        keywordCollection = get_collection('keywords')
        keywords = keywordCollection.find_one({'user_name':'cem'})['include']
        # keywords=['halk', 'millet', 'vatan', 'tayyip', 'bakan', 'tbmm']
        keywords+=['millet', 'tayyip']
        print keywords
        # keywordCollection.update({'user_name':'cem'}, {'user_name':'cem', 'include': keywords},True)
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

    def test_delete_kelime(self):
        a = ['cem', 'hula', 'cem']
        # a.remove('cem')
        a.remove('hula')
        a.remove('hula')
        print a
