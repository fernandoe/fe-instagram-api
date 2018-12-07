import logging
import os
import time

import django.db
from azure.servicebus import AzureServiceBusPeekLockError
from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections

from fe_azure.queue import QUEUE_JOB_PREPARE_POST_TO_IMPORT_TO_ELASTICSEARCH, receive_queue_message
from instagram.models import Post

logger = logging.getLogger(__name__)

elasticsearch_host = os.getenv('FE_ELASTICSEARCH_HOST')


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            django.db.close_old_connections()
            connections.create_connection(hosts=[elasticsearch_host])
            message = receive_queue_message(QUEUE_JOB_PREPARE_POST_TO_IMPORT_TO_ELASTICSEARCH)
            if message:
                continue
            if message.body is None:
                logger.info('The message body is None')
            else:
                post_uuid = message.body.decode("utf-8")
                logger.info(f'post_uuid: {post_uuid}')
                post = Post.objects.get(uuid=post_uuid)
                post.indexing()
            logger.info('Deleting message...')
            try:
                message.delete()
                logger.info('Message deleted!')
            except AzureServiceBusPeekLockError:
                logger.info('Timeout getting new message!')
            logger.info('Sleep for 1 seconds...')
            time.sleep(1)
