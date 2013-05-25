from unittest import TestCase
from HtmlAndTextParseHelper import get_unicode
from HurriyetReader import HurriyetReader

__author__ = 'cvardar'


class hurriyet_kose_yazisi_tests(TestCase):
    def test_read_yazarlar(self):
        f = open('HurriyetYazarlar.html', 'r')
        f_read = f.read()
        reader = HurriyetReader()
        links = reader.get_yazi_links(f_read)
        f = open('HurriyetExpectedLinks', 'r')
        expected_links = set([x.strip() for x in f.readlines()])
        self.assertEqual(expected_links, links)

    def test_read_yazi(self):
        f = open('HurriyetYazi.html', 'r')
        f_read = f.read()
        url = 'http://www.hurriyet.com.tr/yazarlar/23364133.asp'
        reader = HurriyetReader()

        yazi = reader.get_doc_from_html(f_read, url)
        self.assertEqual(get_unicode('Baro’metre'), yazi['title'])
        self.assertEqual(get_unicode('25 Mayıs 2013'), yazi['date'])
        self.assertEqual(get_unicode('Yılmaz ÖZDİL'), yazi['author'])
        self.assertEqual(get_unicode('hurriyet'), yazi['gazete'])
        self.assertEqual(2915, len(yazi['content']))