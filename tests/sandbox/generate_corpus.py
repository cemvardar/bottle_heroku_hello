from unittest import TestCase
from kose_yazisi import get_yazi_json, insert_doc_into_yazilar
from mongolab_helper import get_collection

__author__ = 'cvardar'

class GenerateCorpusTests(TestCase):
    def test_first(self):
        pass
        # cnt=0
        # for i in get_collection('links').find():
        #     for link in i['links']:
        #         print link
        #         json = get_yazi_json(link)
        #         if not json:
        #             continue
        #         insert_doc_into_yazilar(json,'corpus_test2')
        #         print 'saved:' + link
        #         cnt+=1
        #         print str(cnt) + ' editorial saved'


