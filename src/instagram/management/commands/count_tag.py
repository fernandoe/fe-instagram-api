import json
import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from instagram.models import Tag


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        r = requests.get('https://www.instagram.com/explore/tags/paiefilha/')
        soup = BeautifulSoup(r.text, 'lxml')

        script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)

        print(data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count'])
