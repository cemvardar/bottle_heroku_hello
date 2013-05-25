from HTMLParser import HTMLParser
import urllib2
import urlparse
from bs4 import BeautifulSoup

__author__ = 'cvardar'

def get_gazete_name(url):
    parse_object = urlparse.urlparse(url)
    address = parse_object.netloc
    return address.replace('.tr', '').replace('.com','').replace('www.', '')

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_unicode(utf8):
    return utf8.decode('UTF-8')


def get_links_from_html(html):
    soup = BeautifulSoup(html)
    links_html = soup.findAll('a')
    return links_html

def get_html_from_url(url):
    request = urllib2.Request(url)
    return urllib2.urlopen(request)


def get_soup_links(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return get_links_from_html(response)

def get_hurriyet_yazi_links(linkToScrape):
    links_html = get_soup_links(linkToScrape)
    links = set([])
    for a in links_html:
        if 'yazarlar' in a['href'] and 'asp' in a['href'] \
            and 'default' not in a['href'] and 'ID' not in a['href']:
            links.add(a['href'])
    return links

def get_radikal_yazi_links(html):
    links = set([])
    for i in get_links_from_html(html):
        if i.has_attr('href'):
            if 'http://www.radikal.com.tr/yazarlar' in i['href']:
                links.add(i['href'])
    links.remove('http://www.radikal.com.tr/yazarlar/')
    return links

def get_radikal_doc_from_url(url):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, err:
        if err.code == 404:
            return ''
        else:
            raise
    html = response.read()
    return get_radikal_doc_from_html(html, url)

def get_radikal_doc_from_html(html, url):
    soup = BeautifulSoup(html)
    yazi = {}
    yazi['gazete'] = get_gazete_name(url)
    yazi['url'] = url
    tarih = soup.find('div', attrs={'class': 'text_size'}).text
    yazi['date'] = tarih.strip()[:-1]
    yazarName = soup.find('div', attrs={'class': 'author'}).find('img')['alt']
    yazi['author'] = yazarName
    yaziContent = soup.find("div", {"id": "metin2"})
    title = soup.find('div', attrs={'class': 'news_detail_top'}).text
    yazi['content'] = unicode(yaziContent)
    yazi['title'] = title
    return yazi