from HtmlAndTextParseHelper import get_gazete_name, get_links_from_html
from bs4 import BeautifulSoup

__author__ = 'cvardar'


class RadikalReader():
    def get_doc_from_html(self, html, url):
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

    def get_yazi_links(self, html):
        links = set([])
        for i in get_links_from_html(html):
            if i.has_attr('href'):
                if 'http://www.radikal.com.tr/yazarlar' in i['href']:
                    links.add(i['href'])
        links.remove('http://www.radikal.com.tr/yazarlar/')
        return links