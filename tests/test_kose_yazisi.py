#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
from unittest import TestCase
import urllib2
import bottle
from kose_yazisi import get_yazi_json, get_yazi_from_html, get_yazilar_collection, insert_doc_into_yazilar, get_yazilar

__author__ = 'cvardar'

def get_url():
     return 'http://www.hurriyet.com.tr/yazarlar/22878887.asp'

def get_unicode(utf8):
    return utf8.decode('UTF-8')

class kose_yazisi_tests(TestCase):
    def assert_yazi(self, yazi):
        self.assertEqual(get_unicode(get_url()), yazi['url'])
        self.assertEqual(get_unicode('Yuh artık, bu kadar mı'), yazi['title'])
        self.assertEqual(get_unicode('23 Mart 2013'), yazi['date'])
        self.assertEqual(get_unicode('Ertuğrul ÖZKÖK'), yazi['author'])
        self.assertEqual(4449, len(yazi['content']))

    def test_from_web(self):
        yazi = get_yazi_json(get_url())
        self.assert_yazi(yazi)

    def test_from_local_file(self):
        f = open('test_article.txt', 'r')
        self.assert_yazi(get_yazi_from_html(f.read(), get_url()))

    def test_save_doc(self):
        bottle.TEMPLATE_PATH.append('../views')
        f = open('test_article.txt', 'r')
        f_read = f.read()
        yazi = get_yazi_from_html(f_read, get_url())
        insert_doc_into_yazilar(yazi, 'unit_test_5161a220123f8f3a15798389')
        yazi2 = get_yazi_from_html(f_read, get_url())
        insert_doc_into_yazilar(yazi2, 'unit_test_5161a220123f8f3a15798389')
        rows = get_yazilar('unit_test_5161a220123f8f3a15798389')
        self.assertEqual(2, len(rows))
        get_yazilar_collection().remove({'user_name':'unit_test_5161a220123f8f3a15798389'})


