from pymongo import IndexModel, DESCENDING
from aiomongodel import Document, EmbeddedDocument
from aiomongodel.fields import (
    StrField, BoolField, ListField, EmbDocField, RefField, SynonymField,
    IntField, FloatField, DateTimeField, ObjectIdField)

from datetime import datetime


class Search_query(Document):

    user_id = StrField()
    engine = StrField()
    query = StrField()
    result = StrField()
    date = DateTimeField()

    def to_json(self):
        return {
            'user_id': self.user_id,
            'engine': self.engine,
            'query': self.query,
            'result': self.result,
            'date': self.date
        }

    class Meta:
        collection = 'search_query'
