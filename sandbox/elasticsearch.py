# from elasticsearch_dsl.connections import connections
# connections.create_connection(hosts=['elasticsearch'])
# print(connections.get_connection().cluster.health())
# ----------------------------------------------------------------------------------------------------------------------
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from datetime import datetime

class Hashtags(Document):
    tags = Keyword()
    created_at = Date()

    class Index:
        name = 'tags'

    class Meta:
        index = 'hashtags-index'

Hashtags.init()


# # create and save and article
hahstag = Hashtags(meta={'uuid': 42}, tags=['test'])
hahstag.created_at = datetime.now()
hahstag.save()

h = Hashtags.get(id=42)

#
# article = Article.get(id=42)
# print(article.is_published())

# class Article(Document):
#     title = Text(analyzer='snowball', fields={'raw': Keyword()})
#     body = Text(analyzer='snowball')
#     tags = Keyword()
#     published_from = Date()
#     lines = Integer()
#
#     class Index:
#         name = 'blog'
#         settings = {
#           "number_of_shards": 2,
#         }
#
#     def save(self, ** kwargs):
#         self.lines = len(self.body.split())
#         return super(Article, self).save(** kwargs)
#
#     def is_published(self):
#         return datetime.now() >= self.published_from



# from instagram.search import bulk_indexing
# bulk_indexing()


from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = 'blog'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from