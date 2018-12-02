from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections

from instagram.models import Post
from instagram.search import PostIndex


class Command(BaseCommand):

    def handle(self, *args, **options):
        connections.create_connection(hosts=['elasticsearch'])

        PostIndex.init()

        posts = Post.objects.all()
        for post in posts:
            print(f"Processing: {post}")
            post.indexing()
