# from django.core.management.base import BaseCommand
# from django.db.models import Count
#
# from instagram.helpers import save_tag, process_tag
# from instagram.models import Tag
#
#
# class Command(BaseCommand):
#     help = 'Extract tags from teh Instagram images'
#
#     def add_arguments(self, parser):
#         parser.add_argument('-t', '--tag', type=str, help='Extract tags from the informed tag', )
#
#     def handle(self, *args, **options):
#         tag = options['tag']
#         if tag:
#             tags = [tag]
#         else:
#             # tags = Tag.objects.values_list('name', flat=True)
#             tags = []
#             tags_objects = Tag.objects.annotate(number_of_counts=Count('tagcount'))
#             for tag_object in tags_objects:
#                 if tag_object.number_of_counts == 0:
#                     tags.append(tag_object.name)
#
#         unique_hashtags_from_instagram_page = set()
#         for tag in tags:
#             try:
#                 tag_object = Tag.objects.get(name=tag)
#                 if tag_object.last_count is None:
#                     process_tag(tag, unique_hashtags_from_instagram_page)
#             except Tag.DoesNotExist:
#                 continue
#
#         for tag in unique_hashtags_from_instagram_page:
#             save_tag(tag)
