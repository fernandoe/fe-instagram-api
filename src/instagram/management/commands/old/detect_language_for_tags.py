from django.core.management.base import BaseCommand

from fe_azure.translate import detect
from instagram.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        tags = Tag.objects.filter(languages__isnull=True)
        for tag in tags:
            tag_name = tag.name
            print(f"TAG: {tag_name}")
            if has_numbers(tag_name):
                tag.languages = 'has_numbers'
            elif has_special_chars(tag_name):
                tag.languages = 'has_special_chars'
            else:
                languages = detect(tag_name)
                if languages is None or len(languages) == 0:
                    tag.languages = 'N/A'
                else:
                    tag.languages = ' '.join(languages)
            print(f"Languages: {tag.languages}")
            tag.save()


def has_numbers(word):
    return any(char.isdigit() for char in word)


SPECIAL_CHARS = '-_'


def has_special_chars(word):
    return any(char in SPECIAL_CHARS for char in word)
