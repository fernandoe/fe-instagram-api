import json
import time

from django.core.management.base import BaseCommand

from instagram.models import TagPriority, TextSearch, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            texts_search = TextSearch.objects.filter(ingest_at__isnull=True)
            for ts in texts_search:
                tags = ts.text.split()
                for tag in tags:
                    try:
                        t = Tag.objects.get(name=tag)
                    except Tag.DoesNotExist:
                        t = Tag.objects.create(name=tag)
                    if t.last_count is None:
                        TagPriority.objects.create(tag=t)

                items = json.loads(ts.result)['items']
                for item in items:
                    try:
                        t = Tag.objects.get(name=item['name'])
                    except Tag.DoesNotExist:
                        t = Tag.objects.create(name=item['name'])
                    if t.last_count is None:
                        TagPriority.objects.create(tag=t)

            print('Sleep for 3 seconds...')
            time.sleep(3)
            print('Continue after sleep...')
