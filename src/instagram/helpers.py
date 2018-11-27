import re


def filter_tag(word):
    hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)$")
    if hashtag_re.match(word):
        return True
    else:
        print(f"Inválido: {word}")
        return False


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
