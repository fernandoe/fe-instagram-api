from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document, Date, Keyword, Text
from elasticsearch_dsl.connections import connections

from . import models

connections.create_connection(hosts=['elasticsearch'])


class PostIndex(Document):
    uuid = Text()
    tags = Keyword(multi=True)
    created_at = Date()

    class Index:
        name = 'post-index'


# class Index:
#     name = 'my-index-name'

def bulk_indexing():
    PostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))

# def bulk_indexing():
#     BlogPostIndex.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in models.BlogPost.objects.all().iterator()))
#
# def bulk_indexing():
#     Hashtags.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))
