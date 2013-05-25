from collections import defaultdict
from datetime import datetime, timedelta
from unittest import TestCase
import urllib2
import urlparse
from HtmlAndTextParseHelper import get_html_from_url, get_hurriyet_yazi_links, get_radikal_yazi_links
from bs4 import BeautifulSoup
from kose_yazisi import get_yazi_json, insert_doc_into_yazilar
from mongolab_helper import get_collection, get_date_username

__author__ = 'cvardar'
#
# def get_links_html(linkToScrape):
#     request = urllib2.Request(linkToScrape)
#     response = urllib2.urlopen(request)
#     soup = BeautifulSoup(response)
#     links_html = soup.findAll('a')
#     return links_html

class CollectLinks(TestCase):
    def test_all_links_single_level(self):
        yazi_links = get_hurriyet_yazi_links("http://www.hurriyet.com.tr/yazarlar/")
        radikal_html = get_html_from_url("http://www.radikal.com.tr/yazarlar/")
        radikal_yazi_links = get_radikal_yazi_links(radikal_html)
        yazi_links = yazi_links.union(radikal_yazi_links)
        collection = get_collection('links_by_date')
        collection.insert({'date':datetime.utcnow(), 'links': list(yazi_links)})

    def test_hurriyet_links(self):
        yazi_links = get_hurriyet_yazi_links("http://www.hurriyet.com.tr/yazarlar/")
        radikal_html = get_html_from_url("http://www.radikal.com.tr/yazarlar/")
        radikal_yazi_links = get_radikal_yazi_links(radikal_html)
        yazi_links = yazi_links.union(radikal_yazi_links)
        for i in yazi_links:
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