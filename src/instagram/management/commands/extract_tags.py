from django.core.management.base import BaseCommand
from django.db.models import Count

from instagram.helpers import save_tag, extract_tag_count, is_valid_tag, get_instagram_data
from instagram.models import Tag, Post, TagCount


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
                if tag_object.number_of_counts == 0:
                    tags.append(tag_object.name)

        unique_hashtags_from_instagram_page = set()
        for tag in tags:
            try:
                data = get_instagram_data(tag)
            except:
                continue
            tag_count = extract_tag_count(tag, data)
            process_posts_in('edge_hashtag_to_media', data, unique_hashtags_from_instagram_page)
            process_posts_in('edge_hashtag_to_top_posts', data, unique_hashtags_from_instagram_page)
            try:
                tag_object = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                tag_object = Tag.objects.create(name=tag)
            TagCount.objects.create(tag=tag_object, count=tag_count)

        for tag in unique_hashtags_from_instagram_page:
            save_tag(tag)


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

# from instagram.models import Tag, TagCount
# tags = TagCount.objects.all()
# for tag in tags:
#     tag.tag.last_count = tag.count
#     tag.tag.save()
#
