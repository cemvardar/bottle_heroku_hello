from unittest import TestCase

__author__ = 'cvardar'

class DocRowTest(TestCase):
    def test_first(self):
        docRow = DocRow("www.google.com")
        docRow.append('cem')
        docRow.append('ali')
        print docRow.url
        for i in docRow:
            print i

class DocRow(list):
    def __init__(self, url):
        self.url = url
