import pymongo
import os

__author__ = 'cvardar'

def get_names_collection():
    userid = os.environ['mongolab_userid']
    password = os.environ['mongolab_password']
    mongodb_uri = "mongodb://"+userid+":"+ password+ "@ds053937.mongolab.com:53937/cem_heroku_hello"
    db_name = 'cem_heroku_hello'
    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
    except:
        print('Error: Unable to connect to database.')
        return None
    names_collection = database.names
    return names_collection

