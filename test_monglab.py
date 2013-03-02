from unittest import TestCase
import sys
from mongolab_helper import get_names_collection
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
