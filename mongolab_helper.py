import pymongo
import os

__author__ = 'cvardar'


def get_mongoDb_url():
    userid = os.environ['mongolab_userid']
    password = os.environ['mongolab_password']
    mongodb_uri = "mongodb://" + userid + ":" + password + "@ds053937.mongolab.com:53937/cem_heroku_hello"
    return mongodb_uri

def get_mongoDb_url_local():
    return 'localhost'

def get_names_collection():
    return get_collection('names')

def get_commutes_collection():
    return get_collection('commutes')

def get_collection(collectionName):
    mongodb_uri = get_mongoDb_url()
    # mongodb_uri = get_mongoDb_url_local()
    db_name = 'cem_heroku_hello'
    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
    except:
        print('Error: Unable to connect to database.')
        return None
    names_collection = database[collectionName]
    return names_collection

class SimpleQuery():
    def __init__(self, collectionName):
        self.collectionName = collectionName

    def get_data(self, fieldsToPull):
        collection = get_collection(self.collectionName)
        if collection is not None:
            namesCursor = collection.find()
            rows = []
            for names in namesCursor:
                row = []
                for f in fieldsToPull:
                    row.append(names[f])
                rows.append(row)
            return rows
        return []