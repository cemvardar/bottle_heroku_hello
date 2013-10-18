#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice

from unittest import TestCase
import urllib2
import time
from HtmlAndTextParseHelper import get_unicode, get_gazete_name, get_html_from_url
from SozcuReader import SozcuReader

__author__ = 'cvardar'


class test_sozcu_parse(TestCase):
    def test_read_yazarlar_zaman(self):
        f = open('SozcuYazarlar.html', 'r')
        f_read = f.read()
        reader = SozcuReader()
        links = reader.get_yazi_links(f_read)
        f = open('SozcuExpectedLinks.txt', 'r')
        expected_links = set([x.strip() for x in f.readlines()])
        self.assertEqual(expected_links, links)

    def test_read_yazi_zaman(self):
        f = open('SozcuYazi.html', 'r')
        f_read = f.read()
        url = 'http://zaman.com.tr/ahmet-kurucan/bu-kadar-basit-degil-olamaz-olmamali_2119892.html'
        reader = SozcuReader()

        yazi = reader.get_doc_from_html(f_read, url)
        self.assertEqual(get_unicode('Mehmet Akif “Irkçı” mı! -'), yazi['title'])
        self.assertEqual(get_unicode('2013-10-09 03:45:47'), yazi['date'])
        self.assertEqual(get_unicode('Emin Çölaşan'), yazi['author'])
        self.assertEqual(get_unicode('Sozcu'), yazi['gazete'])
        self.assertEqual(6381, len(yazi['content']))

    def test_gazete_name(self):
        yazarlarUrl = "http://www.sozcu.com.tr/kategori/yazarlar/"
        gazete_name = get_gazete_name(yazarlarUrl)
        self.assertEqual("sozcu", gazete_name)