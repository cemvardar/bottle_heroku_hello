#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from HtmlAndTextParseHelper import get_unicode
from KelimelerPage import insert_new_keyword, delete_keyword
from kose_yazisi import get_yazilar_collection
from mongolab_helper import get_collection

__author__ = 'cvardar'

class TestKeywordPage(TestCase):
    def setUp(self):
        self.userNameMock = 'unittest_123241341243'
        self.keywordCollection = get_collection('keywords')

    def test_insert_for_new_user(self):
        self.keywordCollection.remove({'user_name': self.userNameMock})
        insert_new_keyword('vatan', self.userNameMock)
        doc = self.keywordCollection.find_one({'user_name': self.userNameMock})
        self.assertTrue(get_unicode('vatan') in doc['include'])
        self.keywordCollection.remove({'user_name': self.userNameMock})

    def test_insert_for_existing_user(self):
        self.keywordCollection.remove({'user_name': self.userNameMock})
        insert_new_keyword('vatan', self.userNameMock)
        insert_new_keyword('yurt', self.userNameMock)
        doc = self.keywordCollection.find_one({'user_name': self.userNameMock})
        self.assertTrue(get_unicode('vatan') in doc['include'])
        self.assertTrue(get_unicode('yurt') in doc['include'])
        self.keywordCollection.remove({'user_name': self.userNameMock})

    def test_delete_for_existing_user(self):
        self.keywordCollection.remove({'user_name': self.userNameMock})
        insert_new_keyword('vatan', self.userNameMock)
        insert_new_keyword('yurt', self.userNameMock)
        doc = self.keywordCollection.find_one({'user_name': self.userNameMock})
        self.assertTrue(get_unicode('vatan') in doc['include'])
        self.assertTrue(get_unicode('yurt') in doc['include'])
        delete_keyword('vatan', self.userNameMock)
        doc = self.keywordCollection.find_one({'user_name': self.userNameMock})
        self.assertFalse(get_unicode('vatan') in doc['include'])
        self.assertTrue(get_unicode('yurt') in doc['include'])
        self.keywordCollection.remove({'user_name': self.userNameMock})

    def test_insert_for_turkish_letters(self):
        self.keywordCollection.remove({'user_name': self.userNameMock})
        insert_new_keyword('ışönüğç', self.userNameMock)
        insert_new_keyword('İsimleri', self.userNameMock)
        doc = self.keywordCollection.find_one({'user_name': self.userNameMock})
        self.assertTrue(get_unicode('ışönüğç') in doc['include'])
        self.assertTrue(get_unicode('isimleri') in doc['include'])
        self.keywordCollection.remove({'user_name': self.userNameMock})

    def test_insert_for_turkish_letters_not_working_correctly(self):
        self.keywordCollection.remove({'user_name': self.userNameMock})
        insert_new_keyword('Işık', self.userNameMock)
        doc = self.keywordCollection.find_one({'user_name': self.userNameMock})
        self.assertTrue(get_unicode('işık') in doc['include'])
        self.keywordCollection.remove({'user_name': self.userNameMock})