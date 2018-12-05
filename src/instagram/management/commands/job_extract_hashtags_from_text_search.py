import time

from django.core.management.base import BaseCommand

from fe_azure.queue import QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH, send_to_job_extract_hashtag_count, \
    receive_queue_message
from instagram.models import TextSearch, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            message = receive_queue_message(QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH)
            text_search_uuid = message.body.decode("utf-8")
            text_search = TextSearch.objects.get(uuid=text_search_uuid)
            hashtags = text_search.get_hashtags_from_result()
            for hashtag in hashtags:
                print(f'Processing tag: {hashtag}')
                tag, created = Tag.objects.get_or_create(name=hashtag)
                if created or tag.last_count is None:
                    print(f'Tag: {tag} - Created: {created}')
                    send_to_job_extract_hashtag_count(hashtag)
            print('Deleting message...')
            message.delete()
            print('Message deleted!')

            print('Sleep for 1 seconds...')
            time.sleep(1)
