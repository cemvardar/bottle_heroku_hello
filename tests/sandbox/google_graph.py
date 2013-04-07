from unittest import TestCase
import unittest
import gviz_api

__author__ = 'cvardar'

class google_graph_tests(TestCase):
    def test_first(self):
        description = {"year": ("string", "Year"),
                       "Austria": ("number", "Austria"),
                       "Bulgaria": ("number", "Bulgaria"),
                       "Denmark": ("number", "Denmark")}
        data = [{"year": "2003", "Austria": 1336060, "Bulgaria": 400361, "Denmark":1001582},
                {"year": "2004", "Austria": 1538156, "Bulgaria": 366849, "Denmark":1119450},
                {"year": "2005", "Austria": 1576579, "Bulgaria": 440514, "Denmark":993360}]

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        # print data_table["table"]
        print "Content-type: text/plain"
        print
        print data_table.ToJSonResponse(columns_order=("year", "Austria", "Bulgaria", "Denmark"))
        print data_table.ToJSon()