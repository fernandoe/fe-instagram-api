import json

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from instagram.helpers import filter_tag
from instagram.models import Tag


class Command(BaseCommand):
    help = 'Extract tags from images'

    def handle(self, *args, **options):
        r = requests.get('https://www.instagram.com/explore/tags/fit/')
        soup = BeautifulSoup(r.text, 'lxml')

        script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)

        # for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
        #     # image_src = post['node']['thumbnail_resources'][1]['src']
        #     # print(image_src)
        #     print('=' * 100)
        #     print(json.dumps(post))

        for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
            edges = post['node']['edge_media_to_caption']['edges']
            if len(edges) <= 0:
                continue
            message = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
            print('=' * 100)
            words = extract_words_from_message(message)
            print('Words: %s' % words)
            tags = list(filter(filter_tag, words))
            print('Tags: %s' % tags)

            for tag in tags:
                if Tag.objects.filter(name=tag).count() == 0:
                    Tag.objects.create(name=tag)


def extract_words_from_message(message):
    result = []
    words = message.lower().split(' ')
    words_2_add = []
    for word in words:
        if '\n' in word:
            words_2_add.extend(word.split('\n'))
        else:
            words_2_add.append(word)

    for word in words_2_add:
        if word.startswith('#') and word.count('#') > 1:
            parse_tags = word.split('#')
            for parse_tag in parse_tags:
                words_2_add.append(f"#{parse_tag}")
            words_2_add.remove(word)
    result.extend(words_2_add)

    return result
