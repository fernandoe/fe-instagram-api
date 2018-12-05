from django.test import TestCase

from fe_azure.queue import create_queues, QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH, QUEUE_JOB_EXTRACT_HASHTAG_COUNT


class TestQueueCreateQueues(TestCase):

    def test_create_queues(self):
        create_queues(QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH)
        create_queues(QUEUE_JOB_EXTRACT_HASHTAG_COUNT)
