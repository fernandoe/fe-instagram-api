import json
import logging
import re
import time

import django.db
import requests
from azure.servicebus import AzureServiceBusPeekLockError
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from fe_azure.queue import receive_queue_message, QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG
from instagram.models import Tag, Post

logger = logging.getLogger(__name__)


def get_instagram_data(tag):
    if tag.startswith('#'):
        tag = tag[1:]

    url = f"https://www.instagram.com/explore/tags/{tag}/"
    logger.info(f"URL: {url}")

    r = requests.get(url)
    if r.status_code != 200:
        logger.info(f"STATUS CODE: {r.status_code}")
        logger.info(f"TEXT: {r.text}")

    soup = BeautifulSoup(r.text, 'lxml')

    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    return json.loads(page_json)


def process_tag(tag):
    data = get_instagram_data(tag)

    process_posts_in('edge_hashtag_to_media', data)
    process_posts_in('edge_hashtag_to_top_posts', data)


def process_posts_in(field, data):
    for post in data['entry_data']['TagPage'][0]['graphql']['hashtag'][field]['edges']:
        if len(post['node']['edge_media_to_caption']['edges']) == 0:
            continue
        message = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
        shortcode = post['node']['shortcode']

        logger.info(f"Message: {message}")
        words = extract_words_from_message(message)
        tags_in_message = set(filter(is_valid_tag, words))
        logger.info('Valid Tags: %s' % tags_in_message)
        try:
            Post.objects.get(shortcode=shortcode)
        except Post.DoesNotExist:
            tags_in_str = ' '.join([e[1:] for e in tags_in_message])
            Post.objects.create(shortcode=shortcode, tags=tags_in_str)


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


def print_invalid_tag(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            logger.info(f"Invalid hashtag: {args[0]}")
        return result

    return wrapper


HASHTAG_RE = re.compile("(?:^|\s)[＃#]{1}(\w+)$")
ALLOWED_CHARS = '#abcdefghijklmnopqrstuvwxyzçãâáàäẽêéèëĩîíìïõôóòöũûúùüñ1234567890_-'


def is_invalid_char(char):
    return char not in ALLOWED_CHARS


@print_invalid_tag
def is_valid_tag(name):
    if name is None:
        return False

    if len(name) > 100:
        return False

    if not name.startswith('#'):
        return False

    invalid_chars = sum([is_invalid_char(x) for x in name])
    if invalid_chars > 0:
        return False

    if not HASHTAG_RE.match(name):
        return False

    return True


def process(hashtag: str) -> None:
    logger.info(f'Hashtag: {hashtag}')
    tag, created = Tag.objects.get_or_create(name=hashtag)
    logger.info(f'Tag: {tag} - Created: {created}')
    process_tag(tag.name)


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            django.db.close_old_connections()
            message = receive_queue_message(QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG)
            if message:
                continue
            if message.body is None:
                logger.info('The message body is None')
            else:
                hashtag = message.body.decode("utf-8")
                process(hashtag)
            logger.info('Deleting message...')
            try:
                message.delete()
                logger.info('Message deleted!')
            except AzureServiceBusPeekLockError:
                logger.info('Timeout getting new message!')
            logger.info('Sleep for 1 seconds...')
            time.sleep(1)
