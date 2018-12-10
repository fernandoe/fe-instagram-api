from django.core.management.base import BaseCommand

from fe_azure.queue import create_queues, QUEUE_TEXT_SEARCH, QUEUE_HASHTAG


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_queues(QUEUE_TEXT_SEARCH)
        create_queues(QUEUE_HASHTAG)
