from collections import defaultdict
from datetime import datetime, timedelta
from unittest import TestCase
from kose_yazisi import get_yazi_json, insert_doc_into_yazilar, get_yazi_links_from_url
from mongolab_helper import get_collection, get_date_username

__author__ = 'cvardar'

class CollectLinks(TestCase):
    def test_all_links_single_level(self):
        yazar_page_urls = ["http://www.hurriyet.com.tr/yazarlar/",
                           "http://www.radikal.com.tr/yazarlar/"]
        all_yazi_links=set([])
        for url in yazar_page_urls:
            all_yazi_links = all_yazi_links.union(get_yazi_links_from_url(url))

        collection = get_collection('links_by_date')
        collection.insert({'date':datetime.utcnow(), 'links': list(all_yazi_links)})

    def test_hurriyet_links(self):
        yazar_page_urls = ["http://www.hurriyet.com.tr/yazarlar/",
                           "http://www.radikal.com.tr/yazarlar/"]
        all_yazi_links=set([])
        for url in yazar_page_urls:
            all_yazi_links = all_yazi_links.union(get_yazi_links_from_url(url))

        for i in all_yazi_links:
            print i

    def test_first(self):
        cnt=0
        utc_now = datetime.utcnow()
        start = utc_now -  timedelta(days=1)
        end = utc_now
        timeQuery ={"date": {"$gte": start, "$lt": end}}
        for i in get_collection('links_by_date').find(timeQuery):
            for link in i['links']:
                print link
                json = get_yazi_json(link)
                if not json:
                    continue
                insert_doc_into_yazilar(json,get_date_username())
                print 'saved:' + link
                cnt+=1
                print str(cnt) + ' editorial saved'

    def test_default_dict(self):
        d = defaultdict(int)
        print d['cem']