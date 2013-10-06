from HtmlAndTextParseHelper import get_links_from_html
from bs4 import BeautifulSoup

__author__ = 'cvardar'


class ZamanReader():
    def get_doc_from_html(self, html, url):
        soup = BeautifulSoup(html)
        yazi = {}
        yazi['gazete'] = 'Zaman'
        yazi['url'] = url
        tarih = soup.find('div', attrs={'class': 'detayTarih'}).text
        yazi['date'] = tarih
        yazarName = soup.find('span', attrs={'itemprop': 'author'}).text
        yazi['author'] = yazarName
        yaziContent = soup.find('span', {"itemprop": "articleBody"})
        yazi['content'] = unicode(yaziContent)
        yazi['title'] = soup.find('title').text.strip('- ZAMAN')
        return yazi

    def get_yazi_links(self, html):
        links = set([])
        for a in get_links_from_html(html):
            if 'href' in a.attrs \
                and '.html' in a['href']\
                and 'http:' not in a['href']:
                links.add("http://zaman.com.tr" + a['href'])
        return links