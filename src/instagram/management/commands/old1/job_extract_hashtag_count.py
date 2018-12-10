# import logging
# import time
#
# import django.db
# from azure.servicebus import AzureServiceBusPeekLockError
# from django.core.management.base import BaseCommand
#
# from fe_azure.queue import receive_queue_message, QUEUE_JOB_EXTRACT_HASHTAG_COUNT
# from instagram.helpers import extract_count
# from instagram.models import Tag
#
# logger = logging.getLogger(__name__)
#
#
# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         while True:
#             django.db.close_old_connections()
#             message = receive_queue_message(QUEUE_JOB_EXTRACT_HASHTAG_COUNT)
#             if message:
#                 continue
#             if message.body is None:
#                 logger.info('The message body is None')
#             else:
#                 hashtag = message.body.decode("utf-8")
#                 logger.info(f'Hashtag: {hashtag}')
#                 tag, created = Tag.objects.get_or_create(name=hashtag)
#                 if created or tag.last_count is None:
#                     logger.info(f'Getting the count...')
#                     count = extract_count(hashtag)
#                     if count is None:
#                         tag.last_count = -1
#                     else:
#                         tag.last_count = count
#                     tag.save()
#
#             logger.info('Deleting message...')
#             try:
#                 message.delete()
#                 logger.info('Message deleted!')
#             except AzureServiceBusPeekLockError:
#                 logger.info('Timeout getting new message!')
#             logger.info('Sleep for 1 seconds...')
#             time.sleep(1)
