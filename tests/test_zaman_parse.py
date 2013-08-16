#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from HtmlAndTextParseHelper import get_gazete_name, get_unicode
from ZamanReader import ZamanReader

__author__ = 'cvardar'


class test_zaman_parse(TestCase):
    def test_read_yazarlar_zaman(self):
        f = open('ZamanYazarlar.html', 'r')
        f_read = f.read()
        reader = ZamanReader()
        links = reader.get_yazi_links(f_read)
        f = open('ZamanExpectedLinks.txt', 'r')
        expected_links = set([x.strip() for x in f.readlines()])
        self.assertEqual(expected_links, links)

    def test_read_yazi_zaman(self):
        f = open('ZamanYazi.html', 'r')
        f_read = f.read()
        url = 'http://zaman.com.tr/ahmet-kurucan/bu-kadar-basit-degil-olamaz-olmamali_2119892.html'
        reader = ZamanReader()

        yazi = reader.get_doc_from_html(f_read, url)
        self.assertEqual(get_unicode('Cehalet kıskacında teokrasi ve demokrasi'), yazi['title'])
        self.assertEqual(get_unicode(' 15 Ağustos 2013, Perşembe'), yazi['date'])
        self.assertEqual(get_unicode('Ahmet Kurucan'), yazi['author'])
        self.assertEqual(get_unicode('Zaman'), yazi['gazete'])
        self.assertEqual(3946, len(yazi['content']))

    def test_gazete_name(self):
        gazete_name = get_gazete_name("http://zaman.com.tr/yazarlar")
        self.assertEqual('zaman', gazete_name)
