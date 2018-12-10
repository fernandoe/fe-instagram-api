import json
import re

import requests
from bs4 import BeautifulSoup

from instagram.models import Tag, Post, TagCount


def save_tag(tag):
    from .models import Tag
    if tag is None or not tag.startswith('#'):
        return
    tag = tag[1:]
    if len(tag) > 100:
        return
    try:
        if Tag.objects.filter(name=tag).count() == 0:
            Tag.objects.create(name=tag)
    except Exception as e:
        print(f"ERROR: {e.message}")
        print(f"TAG: {tag_name}")


def extract_tag_count(tag, data):
    count = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
    return count


def print_invalid_tag(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            print(f"Invalid hashtag: {args[0]}")
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


def get_instagram_data(tag):
    if tag.startswith('#'):
        tag = tag[1:]

    url = f"https://www.instagram.com/explore/tags/{tag}/"
    print(f"URL: {url}")

    r = requests.get(url)
    if r.status_code != 200:
        print(f"STATUS CODE: {r.status_code}")
        print(f"TEXT: {r.text}")

    soup = BeautifulSoup(r.text, 'lxml')

    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    return json.loads(page_json)


def process_tag(tag, unique_hashtags_from_instagram_page):
    try:
        data = get_instagram_data(tag)
    except:
        return
    tag_count = extract_tag_count(tag, data)
    process_posts_in('edge_hashtag_to_media', data, unique_hashtags_from_instagram_page)
    process_posts_in('edge_hashtag_to_top_posts', data, unique_hashtags_from_instagram_page)
    try:
        tag_object = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        tag_object = Tag.objects.create(name=tag)
    TagCount.objects.create(tag=tag_object, count=tag_count)


def process_posts_in(field, data, tags):
    for post in data['entry_data']['TagPage'][0]['graphql']['hashtag'][field]['edges']:
        if len(post['node']['edge_media_to_caption']['edges']) == 0:
            continue
        message = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
        shortcode = post['node']['shortcode']

        print(f"Message: {message}")
        words = extract_words_from_message(message)
        tags_in_message = set(filter(is_valid_tag, words))
        print('Valid Tags: %s' % tags_in_message)
        try:
            Post.objects.get(shortcode=shortcode)
        except Post.DoesNotExist:
            tags_in_str = ' '.join([e[1:] for e in tags_in_message])
            Post.objects.create(shortcode=shortcode, tags=tags_in_str)
        tags |= tags_in_message


def extract_words_from_message(message):
    result = []
    words = message.encode('utf-8').lower().split(' ')
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


def extract_count(hashtag: str) -> int:
    print(f'==> extract_count({hashtag})')
    r = requests.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    if r.status_code == 404:
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    return data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
