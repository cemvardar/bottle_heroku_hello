from unittest import TestCase
import sys
from bson import ObjectId
from mongolab_helper import get_names_collection, SimpleQuery
import os
import pymongo
from pymongo import MongoClient

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
        for r in q.get_data(fieldsToPull):
            print r

    def test_simple_query(self):
        q = SimpleQuery('yazilar')
        fieldsToPull = ['_id']
        for r in q.get_data(fieldsToPull, {'_id': ObjectId('514535ed123f8fc61223f39e')}):
            print r[0]
            # print dir(r[0])

