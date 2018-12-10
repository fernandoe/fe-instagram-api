import logging
import time

import django.db
from azure.servicebus import AzureServiceBusPeekLockError
from django.core.management.base import BaseCommand

from fe_azure.queue import QUEUE_TEXT_SEARCH, receive_queue_message, send_to_queue_hashtag
from instagram.models import TextSearch, Tag

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            django.db.close_old_connections()
            message = receive_queue_message(QUEUE_TEXT_SEARCH)
            if message:
                continue
            if message.body is None:
                logger.info('The message body is None')
            else:
                text_search_uuid = message.body.decode("utf-8")
                logger.info(f'text_search_uuid: {text_search_uuid}')
                text_search = TextSearch.objects.get(uuid=text_search_uuid)
                hashtags = text_search.get_hashtags_from_result()
                for hashtag in hashtags:
                    logger.info(f'Processing tag: {hashtag}')
                    send_to_queue_hashtag(hashtag)
                    Tag.objects.get_or_create(name=hashtag)

            logger.info('Deleting message...')
            try:
                message.delete()
                logger.info('Message deleted!')
            except AzureServiceBusPeekLockError:
                logger.info('Timeout getting new message!')
            logger.info('Sleep for 1 seconds...')
            time.sleep(1)
