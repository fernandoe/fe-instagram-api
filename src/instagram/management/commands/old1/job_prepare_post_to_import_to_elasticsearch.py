# import datetime
# import logging
# import time
#
# import django.db
# from django.core.management.base import BaseCommand
# from django.utils import timezone
#
# from fe_azure.queue import send_to_job_prepare_post_to_import_to_elasticsearch
# from instagram.models import Post
#
# logger = logging.getLogger(__name__)
#
#
# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         while True:
#             django.db.close_old_connections()
#
#             posts = Post.objects.filter(ingest_at__isnull=True)[:1000]
#             for post in posts.iterator():
#                 send_to_job_prepare_post_to_import_to_elasticsearch(str(post.uuid))
#                 post.ingest_at = datetime.datetime.now(tz=timezone.utc)
#                 post.save()
#
#             logger.info('Sleep for 10 seconds...')
#             time.sleep(10)
