from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fe_core.models import UUIDModel

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
    shortcode = models.CharField(max_length=100, unique=True)
    tags = models.TextField()
    injest_at = models.DateTimeField(null=True)

    def indexing(self):
        from instagram.search import PostIndex
        print('indexing...')
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
