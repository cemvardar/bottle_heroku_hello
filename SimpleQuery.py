from mongolab_helper import get_docs

__author__ = 'cvardar'


class SimpleQuery():
    def __init__(self, collectionName):
        self.collectionName = collectionName

    def get_data_as_list_of_lists(self, fieldsToPull, query=None):
        rows = []
        for document in get_docs(self.collectionName, query):
            row = []
            for f in fieldsToPull:
                if f in document:
                    row.append(document[f])
                else:
                    row.append('')
            rows.append(row)
        return rows

    def get_docs(self, query = None):
        return get_docs(self.collectionName, query)

    def get_first_doc(self, query = None):
        return get_docs(self.collectionName, query)[0]