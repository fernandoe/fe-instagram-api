import time

from django.core.management.base import BaseCommand

from fe_azure.queue import receive_queue_message, QUEUE_JOB_EXTRACT_HASHTAG_COUNT
from instagram.helpers import extract_count
from instagram.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            message = receive_queue_message(QUEUE_JOB_EXTRACT_HASHTAG_COUNT)
            if message.body is None:
                print('The message body is None')
            else:
                hashtag = message.body.decode("utf-8")
                print(f'Hashtag: {hashtag}')
                tag, created = Tag.objects.get_or_create(name=hashtag)
                if created or tag.last_count is None:
                    print(f'Getting the count...')
                    count = extract_count(hashtag)
                    if count is None:
                        tag.last_count = -1
                    else:
                        tag.last_count = count
                    tag.save()

            print('Deleting message...')
            message.delete()
            print('Message deleted!')

            print('Sleep for 1 seconds...')
            time.sleep(1)
