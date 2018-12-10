# from django.core.management.base import BaseCommand
#
# from instagram.helpers import is_valid_tag
# from instagram.models import Tag
#
#
# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         tags = Tag.objects.all()
#         for tag in tags:
#             if not is_valid_tag(f"#{tag.name}"):
#                 tag.delete()
