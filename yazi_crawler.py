from datetime import datetime, timedelta
from kose_yazisi import get_yazi_links_from_url, get_yazi_json, upsert_doc_into_yazilar
from mongolab_helper import get_collection, get_date_username, insert

__author__ = 'cvardar'

def get_daily_links_from_newspapers():
    yazar_page_urls = ["http://www.hurriyet.com.tr/yazarlar/",
                       "http://www.radikal.com.tr/yazarlar/",
                       "http://zaman.com.tr/yazarlar",
                       "http://www.sozcu.com.tr/kategori/yazarlar"]
    all_yazi_links=set([])
    for url in yazar_page_urls:
        all_yazi_links = all_yazi_links.union(get_yazi_links_from_url(url))

    collection = get_collection('links_by_date')
    collection.insert({'date':datetime.utcnow(), 'links': list(all_yazi_links)})

def get_articles_from_newspapers(userName = get_date_username(), logCollectionName='scrape_log'):
    cnt=0
    for link in get_links():
        # print link
        json = get_yazi_json(link)
        if not json:
            continue
        upsert_doc_into_yazilar(json, userName)
        # print 'saved:' + link
        cnt+=1
        print str(cnt) + ' editorial saved'
    doc = {'user_name': userName, 'date': datetime.utcnow(), 'article_count': cnt}
    insert(logCollectionName, doc)
    return str(cnt) + ' editorial saved'


def get_links():
    utc_now = datetime.utcnow()
    start = utc_now - timedelta(days=10)
    end = utc_now
    timeQuery = {"date": {"$gte": start, "$lt": end}}
    doc = get_collection('links_by_date').find_one(timeQuery, sort=[('date', -1)])
    return doc['links']

