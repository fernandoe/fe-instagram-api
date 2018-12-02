from elasticsearch_dsl import Document, Text, Keyword, Date


class PostIndex(Document):
    uuid = Text()
    tags = Keyword(multi=True)
    created_at = Date()

    class Index:
        name = 'post-index'
