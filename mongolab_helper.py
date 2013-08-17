from datetime import datetime, timedelta
from bson import ObjectId
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
    return database[collectionName]


def get_docs(collectionName, query=None):
    collection = get_collection(collectionName)
    if query and '_id' in query:
        query['_id'] = ObjectId(query['_id'])
    if collection is not None:
        return collection.find(query)

def upsert(collection_name, query, doc_to_upsert):
    collection = get_collection(collection_name)
    collection.update(query, doc_to_upsert, upsert=True, safe=True)

def find_one(collection_name, query):
    collection = get_collection(collection_name)
    return collection.find_one(query)

def get_date_username(daysToGoBack=0):
    d = datetime.today() - timedelta(days=daysToGoBack)
    return 'date' + str(d.month) +'-'  + str(d.day)+'-'  + str(d.year)

def insert(collection_name, json_doc):
    collection = get_collection(collection_name)
    collection.insert(json_doc)

def remove(collection_name, query):
    collection = get_collection(collection_name)
    collection.remove(query)

def create_indexes():
    collection = get_collection('yazilar')
    collection.ensure_index([('user_name', 1), ('author', 1), ('date', 1), ('title', 1)])
    collection.ensure_index([('url', 1)])

    collection = get_collection('links_by_date')
    collection.ensure_index([('date', 1)])

    collection = get_collection('scrape_log')
    collection.ensure_index([('date', 1)])
