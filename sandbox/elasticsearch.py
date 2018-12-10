# ----------------------------------------------------------------------------------------------------------------------
# import os
# from elasticsearch_dsl.connections import connections
# from instagram.search import PostIndex
# elasticsearch_host = os.getenv('FE_ELASTICSEARCH_HOST')
# connections.create_connection(hosts=[elasticsearch_host])
# PostIndex.init()
# ----------------------------------------------------------------------------------------------------------------------
# from elasticsearch_dsl.connections import connections
# from elasticsearch_dsl.connections import connections
# connections.create_connection(hosts=['elasticsearch'])
# print(connections.get_connection().cluster.health())
# ----------------------------------------------------------------------------------------------------------------------
# from instagram.search import bulk_indexing
# bulk_indexing()
# ----------------------------------------------------------------------------------------------------------------------
# # # create and save and article
# hahstag = Hashtags(meta={'uuid': 42}, tags=['test'])
# hahstag.created_at = datetime.now()
# hahstag.save()
# ----------------------------------------------------------------------------------------------------------------------
# h = Hashtags.get(id=42)
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
#     def save(self, ** kwargs):
#         self.lines = len(self.body.split())
#         return super(Article, self).save(** kwargs)
#     def is_published(self):
#         return datetime.now() >= self.published_from
# ----------------------------------------------------------------------------------------------------------------------
# from instagram.search import PostIndex
# from elasticsearch_dsl.connections import connections
# connections.create_connection(hosts=['elasticsearch'])
# pi = PostIndex()
# pi.init()
# ----------------------------------------------------------------------------------------------------------------------
# from elasticsearch_dsl import Search
# from elasticsearch_dsl.connections import connections
# connections.create_connection(hosts=['elasticsearch'])
# # client = Elasticsearch()
# s = Search(index="post-index") \
#     .query("match", tags="banana")
# # response = s.execute()
# # response
# s.aggs.bucket('wordcloud', 'terms', field='tags')
# # \
#     # .metric('max_lines', 'max', field='lines')
# response = s.execute()
# for hit in response:
#     print(hit)
#     # print(hit.meta.score, hit.title)
#
# for tag in response.aggregations.per_tag.buckets:
#     print(tag)
# ----------------------------------------------------------------------------------------------------------------------
# GET post-index/_search
# {
#   "query": {
#     "match": {
#       "tags": "banana"
#     }
#   },
#   "aggs": {
#     "wordcloud": {
#       "terms": {
#         "field": "tags",
#         "size": 100
#       }
#     }
#   }
# }