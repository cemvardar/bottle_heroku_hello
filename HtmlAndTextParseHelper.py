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




