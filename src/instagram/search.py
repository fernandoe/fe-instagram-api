from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Date, Keyword
from elasticsearch_dsl.connections import connections

from . import models

connections.create_connection(hosts=['elasticsearch'])


class Hashtags(DocType):
    tags = Keyword()
    created_at = Date()

    class Meta:
        index = 'hashtags-index'


# def bulk_indexing():
#     HashtagsIndex.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))
