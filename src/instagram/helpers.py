import re


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
    from .models import Tag, TagCount
    count = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count']
    tag_object = Tag.objects.get(name=tag)
    TagCount.objects.create(tag=tag_object, count=count)


def extract_shortcode(data):
    # shortcode = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges'][0]['count']
    shortcode = ''
    return shortcode


# for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
#     edges = post['node']['edge_media_to_caption']['edges']
#     if len(edges) <= 0:
#         continue
#     message = post['node']['edge_media_to_caption']['edges'][0]['node']['text']


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
