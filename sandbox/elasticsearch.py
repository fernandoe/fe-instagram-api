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
#
#     def save(self, ** kwargs):
#         self.lines = len(self.body.split())
#         return super(Article, self).save(** kwargs)
#
#     def is_published(self):
#         return datetime.now() >= self.published_from
# ----------------------------------------------------------------------------------------------------------------------
# from instagram.search import PostIndex
# from elasticsearch_dsl.connections import connections
# connections.create_connection(hosts=['elasticsearch'])
# pi = PostIndex()
# pi.init()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
