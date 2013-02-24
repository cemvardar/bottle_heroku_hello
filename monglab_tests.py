from unittest import TestCase
import sys
import pymongo
from pymongo import MongoClient

__author__ = 'cvardar'

class mongolab_tests(TestCase):
    def test_first(self):

        mongodb_uri = "mongodb://heroku_hello:HerokuHello75@ds053937.mongolab.com:53937/cem_heroku_hello"
        mongodb_uri = "localhost:27017"
        db_name = 'cem_heroku_hello'

        try:
            # connection = pymongo.Connection(mongodb_uri)
            connection = MongoClient()
            database = connection[db_name]
        except:
            print('Error: Unable to connect to database.')
            connection = None

        if connection is not None:

            # To begin with, we'll add a few adventurers to the database. Note that
            # nothing is required to create the adventurers collection--it is
            # created automatically when we insert into it. These are simple JSON
            # objects.
            #
            database.names.insert({'name': 'liplip', 'lastname': 'tikir'})
            party = database.names.find()
            for i in party:
                print i
