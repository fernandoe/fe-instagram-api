import json
import re

import requests
from bs4 import BeautifulSoup


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
