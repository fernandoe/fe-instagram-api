import json
import time

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from fe_azure.queue import receive_queue_message, QUEUE_JOB_EXTRACT_HASHTAG_COUNT
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
                    tag.last_count = count
                    tag.save()

            print('Deleting message...')
            message.delete()
            print('Message deleted!')

            print('Sleep for 1 seconds...')
            time.sleep(1)


def extract_count(hashtag: str) -> int:
    r = requests.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    soup = BeautifulSoup(r.text, 'lxml')
    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    return data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
