import time

from django.core.management.base import BaseCommand

from instagram.helpers import process_tag, save_tag
from instagram.models import TagPriority


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            tag_priorities = TagPriority.objects.all()
            for tag_priority in tag_priorities:
                print(f"tag_priority: {tag_priority.tag}")
                tag = tag_priority.tag
                if tag.last_count is None:
                    unique_hashtags_from_instagram_page = set()
                    process_tag(tag.name, unique_hashtags_from_instagram_page)
                    for tag in unique_hashtags_from_instagram_page:
                        save_tag(tag)
                tag_priority.delete()

            print('Sleep for 10 seconds...')
            time.sleep(3)
            print('Continue after sleep...')
