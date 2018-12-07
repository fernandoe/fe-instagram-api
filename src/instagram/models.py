import json
import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fe_core.models import UUIDModel

from fe_azure.queue import send_to_job_extract_hashtags_from_text_search

logger = logging.getLogger(__name__)
User = get_user_model()


class Tag(UUIDModel):
    name = models.CharField(max_length=100, unique=True)
    last_count = models.IntegerField(null=True)
    languages = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class TagCount(UUIDModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.tag} => {self.count}"


@receiver(post_save, sender=TagCount)
def update_tag_last_count(sender, instance, created, raw, using, **kwargs):
    if created:
        Tag.objects.filter(uuid=instance.tag.uuid).update(last_count=instance.count)


class Post(UUIDModel):
    identifier = models.IntegerField(null=True)
    shortcode = models.CharField(max_length=100, unique=True)
    tags = models.TextField()
    ingest_at = models.DateTimeField(null=True)

    def indexing(self):
        from instagram.search import PostIndex
        logger.info(f'=> indexing({self}')
        tags = []
        if len(self.tags) > 0:
            tags = self.tags.split(' ')
        obj = PostIndex(
            uuid=self.uuid,
            tags=tags,
            created_at=self.created_at
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class TagPriority(UUIDModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class TextSearch(UUIDModel):
    text = models.CharField(max_length=100)
    result = models.TextField()
    ingest_at = models.DateTimeField(null=True)

    def get_hashtags_from_result(self):
        result = []
        items = json.loads(self.result)['items']
        for item in items:
            result.append(item['name'])
        return result


@receiver(post_save, sender=TextSearch)
def post_save_text_search(sender, instance, created, raw, using, **kwargs):
    logger.info(f'=> post_save_text_search(instance={instance}, created={created})')
    if created is True:
        send_to_job_extract_hashtags_from_text_search(str(instance.uuid))
