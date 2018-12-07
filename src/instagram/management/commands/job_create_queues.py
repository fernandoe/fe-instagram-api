from django.core.management.base import BaseCommand

from fe_azure.queue import create_queues, QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH, \
    QUEUE_JOB_EXTRACT_HASHTAG_COUNT, QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_queues(QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH)
        create_queues(QUEUE_JOB_EXTRACT_HASHTAG_COUNT)
        create_queues(QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG)
