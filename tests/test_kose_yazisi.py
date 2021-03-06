#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from HtmlAndTextParseHelper import get_unicode
from HurriyetReader import HurriyetReader
from KelimelerPage import insert_new_keyword
import bottle
from kose_yazisi import get_yazi_json, get_yazilar_collection, upsert_doc_into_yazilar, get_yazilar, get_contained_keywords
from mongolab_helper import get_collection

__author__ = 'cvardar'

def get_url():
     return 'http://www.hurriyet.com.tr/yazarlar/22878887.asp'

def get_url2():
     return 'http://www.hurriyet.com.tr/yazarlar/5.asp'

def get_mock_user_name():
    return 'unit_test_5161a220123f8f3a15798389'

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

    def clean_up_docs_for(self, userName):
        get_yazilar_collection().remove({'user_name': userName})
        get_collection('keywords').remove({'user_name': userName})

    def insert_keywords(self, keywords=['bir', 'iddia:', 'amca', 'yakışan']):
        for k in keywords:
            insert_new_keyword(k, get_mock_user_name())

    def html_from_local_file(self):
        f = open('test_article.txt', 'r')
        f_read = f.read()
        f.close()
        return f_read

    def get_yazi_with_url(self, url):
        reader = HurriyetReader()
        return reader.get_doc_from_html(self.html_from_local_file(), url)

    def test_save_doc_NoDuplicatesBasedOnUrl(self):
        bottle.TEMPLATE_PATH.append('../views')
        self.clean_up_docs_for(get_mock_user_name())

        self.insert_keywords()
        self.insert_doc_with_mock_user(self.get_yazi_with_url(get_url()))
        self.insert_doc_with_mock_user(self.get_yazi_with_url(get_url()))
        self.insert_doc_with_mock_user(self.get_yazi_with_url(get_url2()))

        rows, rows_new = get_yazilar(get_mock_user_name())
        self.assertEqual(2, len(rows))
        self.clean_up_docs_for(get_mock_user_name())

    def insert_doc_with_mock_user(self, doc):
        upsert_doc_into_yazilar(doc, get_mock_user_name())

    def test_find_keywords(self):
        f = open('test_article.txt', 'r')
        f_read = f.read()
        reader = HurriyetReader()
        yazi = reader.get_doc_from_html(f_read, get_url())
        test_keywords = [get_unicode('bir'), get_unicode('yakışan'), get_unicode('tayyip')]
        containedKeywords = get_contained_keywords(yazi, test_keywords)
        self.assertEqual(2, len(containedKeywords))
        self.assertTrue(get_unicode('yakışan'), containedKeywords)
        self.assertTrue(get_unicode('bir'), containedKeywords)

