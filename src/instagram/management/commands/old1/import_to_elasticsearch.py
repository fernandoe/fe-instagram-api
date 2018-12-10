# import datetime
# import os
# import time
#
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from elasticsearch_dsl.connections import connections
#
# from instagram.models import Post
# from instagram.search import PostIndex
#
#
# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         while True:
#             elasticsearch_host = os.getenv('FE_ELASTICSEARCH_HOST')
#             connections.create_connection(hosts=[elasticsearch_host])
#
#             PostIndex.init()
#
#             posts = Post.objects.filter(ingest_at__isnull=True)
#             for post in posts.iterator():
#                 print(f"Processing: {post}")
#                 post.indexing()
#                 post.ingest_at = datetime.datetime.now(tz=timezone.utc)
#                 post.save()
#
#             print('Sleep for 5 seconds...')
#             time.sleep(5)
#             print('Continue after sleep...')
