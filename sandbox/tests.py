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
from instagram.models import Post
from django.db import close_old_connections

close_old_connections()
Post.objects.filter(shortcode__isnull=True).count()
