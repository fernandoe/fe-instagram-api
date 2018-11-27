import json

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Count

from instagram.helpers import save_tag, extract_tag_count, is_valid_tag
from instagram.models import Tag


class Command(BaseCommand):
    help = 'Extract tags from teh Instagram images'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--tag', type=str, help='Extract tags from the informed tag', )

    def handle(self, *args, **options):
        tag = options['tag']
        if tag:
            tags = [tag]
        else:
            # tags = Tag.objects.values_list('name', flat=True)
            tags = []
            tags_objects = Tag.objects.annotate(number_of_counts=Count('tagcount'))
            for tag_object in tags_objects:
                if tag_object.number_of_counts > 0:
                    tags.append(tag_object.name)

        for tag in tags:
            if tag.startswith('#'):
                tag = tag[1:]
            url = f"https://www.instagram.com/explore/tags/{tag}/"
            print(f"URL: {url}")

            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')

            script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
            page_json = script.text.split(' = ', 1)[1].rstrip(';')
            data = json.loads(page_json)

            extract_tag_count(tag, data)

            for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
                edges = post['node']['edge_media_to_caption']['edges']
                if len(edges) <= 0:
                    continue
                message = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
                print('=' * 100)
                words = extract_words_from_message(message)
                print('Words: %s' % words)
                tags = list(filter(is_valid_tag, words))
                print('Valid Tags: %s' % tags)

                for tag_name in tags:
                    save_tag(tag_name)


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

# from django.db.models import Count
# from instagram.models import Tag, TagCount
# tags = Tag.objects.annotate(number_of_counts=Count('tagcount'))
# for tag in tags:
#     if tag.number_of_counts > 0:
#         print(tag)
