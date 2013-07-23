from datetime import datetime, timedelta
from kose_yazisi import get_yazi_links_from_url, get_yazi_json, insert_doc_into_yazilar
from mongolab_helper import get_collection, get_date_username

__author__ = 'cvardar'

def get_daily_links_from_newspapers():
    yazar_page_urls = ["http://www.hurriyet.com.tr/yazarlar/",
                       "http://www.radikal.com.tr/yazarlar/"]
    all_yazi_links=set([])
    for url in yazar_page_urls:
        all_yazi_links = all_yazi_links.union(get_yazi_links_from_url(url))

    collection = get_collection('links_by_date')
    collection.insert({'date':datetime.utcnow(), 'links': list(all_yazi_links)})

def get_articles_from_newpapers():
    cnt=0
    utc_now = datetime.utcnow()
    start = utc_now - timedelta(days=1)
    end = utc_now
    timeQuery ={"date": {"$gte": start, "$lt": end}}
    for i in get_collection('links_by_date').find(timeQuery):
        for link in i['links']:
            # print link
            json = get_yazi_json(link)
            if not json:
                continue
            insert_doc_into_yazilar(json,get_date_username())
            # print 'saved:' + link
            cnt+=1
            print str(cnt) + ' editorial saved'
    return str(cnt) + ' editorial saved'