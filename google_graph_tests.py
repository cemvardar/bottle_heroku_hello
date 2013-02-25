from unittest import TestCase
import gviz_api

__author__ = 'cvardar'

class google_graph_tests(TestCase):
    def test_first(self):
        a= [
            ['Year', 'Austria', 'Bulgaria', 'Denmark', 'Greece'],
            ['2003',  1336060,    400361,    1001582,   997974],
            ['2004',  1538156,    366849,    1119450,   941795],
            ['2005',  1576579,    440514,    993360,    930593],
            ['2006',  1600652,    434552,    1004163,   897127],
            ['2007',  1968113,    393032,    979198,    1080887],
            ['2008',  1901067,    517206,    916965,    1056036]
        ]
        print a

        description = {"year": ("number", "Year"),
                       "Austria": ("number", "Austria"),
                       "Bulgaria": ("number", "Bulgaria"),
                       "Denmark": ("number", "Denmark")}
        data = [{"year": 2003, "Austria": 1336060, "Bulgaria": 400361, "Denmark":1001582},
                {"year": 2004, "Austria": 1538156, "Bulgaria": 366849, "Denmark":1119450},
                {"year": 2005, "Austria": 1576579, "Bulgaria": 440514, "Denmark":993360}]

        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        # print data_table["table"]
        print "Content-type: text/plain"
        print
        print data_table.ToJSonResponse(columns_order=("year", "Austria", "Bulgaria", "Denmark"),
                                        order_by="Austria")

        print data_table.ToJSon()