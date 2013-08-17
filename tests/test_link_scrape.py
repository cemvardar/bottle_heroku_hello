from datetime import datetime
from unittest import TestCase
from mongolab_helper import get_collection
from yazi_crawler import get_links

__author__ = 'cvardar'

class LinkScrapeTests(TestCase):

    def test_one(self):
        collection = get_collection('links_by_date')
        links = ['www.hurriyet.com.tr', 'www.radikal.com.tr']
        objectId  = collection.insert({'date':datetime.utcnow(), 'links': list(links)})
        self.assertEqual(2, len(get_links()))
        collection.remove({"_id" : objectId})