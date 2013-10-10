from unittest import TestCase
from kose_yazisi import DocRowContainer

__author__ = 'cvardar'

class DocRowTest(TestCase):
    def test_first(self):
        docRow = DocRow("www.google.com")
        docRow.append('cem')
        docRow.append('ali')
        print docRow.url
        for i in docRow:
            print i

    def test_doc_row_container(self):
        docRowContainer = DocRowContainer()
        docRowContainer.append(1)
        docRowContainer.append(2)
        for i in docRowContainer:
            print i

class DocRow(list):
    def __init__(self, url):
        self.url = url
