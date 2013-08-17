from unittest import TestCase
from SimpleQuery import SimpleQuery
from kose_yazisi import get_archive_docs_list, HashableDict, get_key
from mongolab_helper import get_names_collection, create_indexes

__author__ = 'cvardar'

class mongolab_tests(TestCase):
    def test_first(self):
        database = get_names_collection()
        if database is not None:
            database.names.insert({'name': 'liplip', 'lastname': 'tikir'})
            party = database.names.find()
            for i in party:
                print i

    def test_simple_query(self):
        q = SimpleQuery('commutes')
        fieldsToPull = ['duration']
        for r in q.get_data_as_list_of_lists(fieldsToPull):
            print r


    def test_simple_query(self):
        q = SimpleQuery('yazilar')
        user_name_query= {"user_name":"cem"}
        counter = {}
        for doc in get_archive_docs_list(q, user_name_query):
            key = get_key(doc)
            if key not in counter:
                counter[key] = [doc['_id']]
            else:
                counter[key].append(doc['_id'])
        for doc in get_archive_docs_list(q, user_name_query):
            if get_key(doc) in counter:
                print 'yeppa'
            else:
                print 'nope'

    def test_dictionary_behavior(self):
        a = HashableDict()
        a['user_name'] = 'cem'
        b = {a: 1}
        print b[a]

    def test_create_indexes(self):
        create_indexes()