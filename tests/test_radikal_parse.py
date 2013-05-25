#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from HtmlAndTextParseHelper import get_radikal_yazi_links, get_radikal_doc_from_html, get_unicode, get_html_from_url

__author__ = 'cvardar'

class kose_yazisi_tests(TestCase):
    def get_expected_links(self):
        expected_links = set([
            'http://www.radikal.com.tr/yazarlar/fatih_ozatay/henuz_gec_degil-1134903',
            'http://www.radikal.com.tr/yazarlar/cem_erciyes/kurula_dirsek_mesafesi-1134908',
            'http://www.radikal.com.tr/yazarlar/muge_akgun/sivil_bir_sanat_tarihi_kitabi_umut_burnundan_dolasarak-1134907',
            'http://www.radikal.com.tr/yazarlar/jale_ozgenturk/kadin_girisimci_mutfaktan_cikacak-1134904',
            'http://www.radikal.com.tr/yazarlar/eyup_can/kemalistlerin_hukukunu_kim_koruyacak-1134898',
            'http://www.radikal.com.tr/yazarlar/akif_beki/nusayrilige_de_ihanettir-1134899',
            'http://www.radikal.com.tr/yazarlar/altan_oymen/12_eylulun_kapattigi_17_partiden_biri-1134901',
            'http://www.radikal.com.tr/yazarlar/metin_ercan/kamu_ozel_sektor_ortakliklari-1134905',
            'http://www.radikal.com.tr/yazarlar/ilker_birbil/kisik_ateste_dijital_delil_corbasi-1134906',
            'http://www.radikal.com.tr/yazarlar/tanil_bora/ham_xavi_elmasi-1134902'])
        return expected_links

    def test_read_yazarlar(self):
        f = open('RadikalYazarlar.html', 'r')
        f_read = f.read()
        expected_links = self.get_expected_links()
        self.assertEqual(expected_links, get_radikal_yazi_links(f_read))

    def test_read_yazarlar2(self):
        # f = open('RadikalYazarlar.html', 'r')
        f_read = get_html_from_url("http://www.radikal.com.tr/yazarlar/")
        print f_read
        expected_links = self.get_expected_links()
        links = get_radikal_yazi_links(f_read)
        print links
        self.assertEqual(expected_links, links)

    def test_read_yazi(self):
        f = open('RadikalYazi.html', 'r')
        f_read = f.read()
        url = 'http://www.radikal.com.tr/yazarlar/fatih_ozatay/henuz_gec_degil-1134903'
        yazi = get_radikal_doc_from_html(f_read, url)
        self.assertEqual(get_unicode('Ham Xavi elması'), yazi['title'])
        self.assertEqual(get_unicode('25/05/2013'), yazi['date'])
        self.assertEqual(get_unicode('TANIL BORA'), yazi['author'])
        self.assertEqual(get_unicode('radikal'), yazi['gazete'])
        # print yazi['title']==get_unicode('Ham Xavi elması')


