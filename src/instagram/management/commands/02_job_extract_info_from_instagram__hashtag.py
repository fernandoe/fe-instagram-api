import json
import logging

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from instagram.models import Tag, Post, Profile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-t', '--hashtag', type=str)

    def handle(self, *args, **options):
        hashtag = options['hashtag']
        extract_info_from_instagram__hashtag(hashtag)
        #
        # while True:
        #     django.db.close_old_connections()
        #     message = receive_queue_message(QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG)
        #     if message:
        #         continue
        #     if message.body is None:
        #         logger.info('The message body is None')
        #     else:
        #         hashtag = message.body.decode("utf-8")
        #         process(hashtag)
        #     logger.info('Deleting message...')
        #     try:
        #         message.delete()
        #         logger.info('Message deleted!')
        #     except AzureServiceBusPeekLockError:
        #         logger.info('Timeout getting new message!')
        #     logger.info('Sleep for 1 seconds...')
        #     time.sleep(1)


def extract_info_from_instagram__hashtag(hashtag: str) -> bool:
    logger.info(f'=> extract_info_from_instagram__hashtag({hashtag})')
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    logger.debug(f"URL: {url}")

    tag, created = Tag.objects.get_or_create(name=hashtag)

    r = requests.get(url)

    if r.status_code == 404:
        tag.valid = False
        tag.save()
        return False

    if r.status_code != 200:
        logger.error(f"Status code: {r.status_code} - Text: {r.text}")
        return False

    soup = BeautifulSoup(r.text, 'lxml')

    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)

    count = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
    print(count)

    process_posts_in('edge_hashtag_to_media', data)
    process_posts_in('edge_hashtag_to_top_posts', data)


def process_posts_in(field, data):
    for post in data['entry_data']['TagPage'][0]['graphql']['hashtag'][field]['edges']:
        if len(post['node']['edge_media_to_caption']['edges']) == 0:
            continue

        data = {
            'identifier': post['node']['id'],
            'shortcode': post['node']['shortcode'],
            'message': post['node']['edge_media_to_caption']['edges'][0]['node']['text'].encode('utf-8'),
            'taken_at_timestamp': post['node']['taken_at_timestamp'],
            'display_url': post['node']['display_url'],
            'edge_liked_by': post['node']['edge_liked_by']['count'],
            'owner': post['node']['owner']['id']
        }
        logger.debug(f'data: {data}')

        profile, created = Profile.objects.get_or_create(identifier=data['owner'])
        data['profile'] = profile

        post, created = Post.objects.get_or_create(shortcode=data['shortcode'])
        for attr, value in data.items():
            setattr(post, attr, value)
        post.save()
        logger.debug(f'Post created: {created} - Post: {post}')

        # logger.info(f"Message: {message}")
        # words = extract_words_from_message(message)
        # tags_in_message = set(filter(is_valid_tag, words))
        # logger.info('Valid Tags: %s' % tags_in_message)
        # try:
        #     Post.objects.get(shortcode=shortcode)
        # except Post.DoesNotExist:
        #     tags_in_str = ' '.join([e[1:] for e in tags_in_message])
        #     Post.objects.create(shortcode=shortcode, tags=tags_in_str)
