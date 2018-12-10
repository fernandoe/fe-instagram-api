import json

import requests
from bs4 import BeautifulSoup

url = 'https://www.instagram.com/emagrecendocomsaude_18/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
print(data)

# ----------------------------------------------------------------------------------------------------------------------
# from django.db.models import Count
# from instagram.models import Tag, TagCount
# tags = Tag.objects.annotate(number_of_counts=Count('tagcount'))
# for tag in tags:
#     if tag.number_of_counts > 0:
#         print(tag)
# ----------------------------------------------------------------------------------------------------------------------
# from instagram.models import Tag, TagCount
# tags = TagCount.objects.all()
# for tag in tags:
#     tag.tag.last_count = tag.count
#     tag.tag.save()
# ----------------------------------------------------------------------------------------------------------------------
# from instagram.models import Post
# from django.db import close_old_connections
# close_old_connections()
# Post.objects.filter(shortcode__isnull=True).count()
# ----------------------------------------------------------------------------------------------------------------------
# from django.db.models import Count
# from instagram.models import Profile
# from django.db import close_old_connections; close_old_connections()
# dupes = Profile.objects.values('identifier').annotate(Count('identifier')).filter(identifier__count__gt=1)
# dupes.count()
# Profile.objects.filter(identifier__in=[item['identifier'] for item in dupes]).delete()
# ----------------------------------------------------------------------------------------------------------------------
# from fe_azure.queue import send_to_queue_hashtag
# from instagram.models import Tag
# tags = Tag.objects.filter(last_count__isnull=True)
# print(f'Total tags: {tags.count()}')
# for tag in tags:
#     print(f'Hashtag: {tag.name}')
#     send_to_queue_hashtag(tag.name)
# ----------------------------------------------------------------------------------------------------------------------
# from fe_azure.queue import send_to_queue_hashtag
# send_to_queue_hashtag('20181210')
# ----------------------------------------------------------------------------------------------------------------------
