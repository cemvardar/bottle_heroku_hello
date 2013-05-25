from HtmlAndTextParseHelper import get_gazete_name, get_links_from_html
from bs4 import BeautifulSoup

__author__ = 'cvardar'


class HurriyetReader():
    def get_doc_from_html(self, html, url):
        soup = BeautifulSoup(html)
        yazi = {}
        yazi['gazete'] = get_gazete_name(url)
        yazi['url'] = url
        tarih = soup.find('div', attrs={'class': 'tarihSp FL'}).text
        yazi['date'] = tarih
        yazarName = soup.find('div', attrs={'class': 'YazarNameContainer_2'}).find('a').text
        yazi['author'] = yazarName
        yaziContent = soup.find("div", {"id": "YazarDetayText"})
        title = yaziContent.find('span').text
        yazi['content'] = unicode(yaziContent)
        yazi['title'] = title
        return yazi

    def get_yazi_links(self, html):
        links = set([])
        for a in get_links_from_html(html):
            if 'yazarlar' in a['href'] and 'asp' in a['href'] \
                and 'default' not in a['href'] and 'ID' not in a['href']:
                links.add(a['href'])
        return links