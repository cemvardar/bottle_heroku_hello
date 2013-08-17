from datetime import datetime
from unittest import TestCase
from kose_yazisi import get_yazilar_collection, get_current_user_name
from mongolab_helper import get_collection
from yazi_crawler import get_links, get_articles_from_newspapers

__author__ = 'cvardar'

class LinkScrapeTests(TestCase):
    def test_gets_links_from_latest_doc(self):
        collection = get_collection('links_by_date')
        links = ['www.hurriyet.com.tr', 'www.radikal.com.tr']
        objectId  = collection.insert({'date':datetime.utcnow(), 'links': list(links)})
        self.assertEqual(2, len(get_links()))
        collection.remove({"_id" : objectId})

    def test_scrape_log(self):
        collection = get_collection('links_by_date')
        links = ['http://www.hurriyet.com.tr/yazarlar/23363349.asp',
                 'http://www.hurriyet.com.tr/yazarlar/23362639.asp']
        objectId  = collection.insert({'date':datetime.utcnow(), 'links': list(links)})
        get_articles_from_newspapers('test125', 'scrape_log_test')
        collection.remove({"_id" : objectId})
        self.clean_up_docs_for('test125')
        self.assertEqual('test125', get_current_user_name('scrape_log_test'))


    def clean_up_docs_for(self, userName):
        get_yazilar_collection().remove({'user_name': userName})
        get_collection('keywords').remove({'user_name': userName})