from django.core.management.base import BaseCommand

from fe_azure.queue import create_queues, QUEUE_TEXT_SEARCH


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_queues(QUEUE_TEXT_SEARCH)
        # create_queues(QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH)
        # create_queues(QUEUE_JOB_EXTRACT_HASHTAG_COUNT)
        # create_queues(QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG)
        # create_queues(QUEUE_JOB_PREPARE_POST_TO_IMPORT_TO_ELASTICSEARCH)
