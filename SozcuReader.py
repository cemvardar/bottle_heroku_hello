from HtmlAndTextParseHelper import get_links_from_html
from bs4 import BeautifulSoup

__author__ = 'cvardar'

class SozcuReader():
    def get_doc_from_html(self, html, url):
        try:
            soup = BeautifulSoup(html)
            yazi = {}
            yazi['gazete'] = 'Sozcu'
            yazi['url'] = url
            tarih = soup.find('meta', attrs={'itemprop': 'datePublished'})['content']
            yazi['date'] = tarih
            yazarName = soup.find('div', attrs={'class': 'yazdet'}).text
            yazi['author'] = yazarName
            yaziContent = soup.find('div', {"class": "content"})
            yazi['content'] = unicode(yaziContent)
            yazi['title'] = soup.find('meta', attrs={'property': 'og:title'})['content']
            return yazi
        except:
            return {}

    def get_yazi_links(self, html):
        links = set([])
        for a in get_links_from_html(html):
            if (
                    'href' in a.attrs
                and 'yazarlar' in a['href']
                and 'kategori' not in a['href']
                and 'spor-yazarlari' not in a['href']
            ):
                links.add(a['href'])
        return links