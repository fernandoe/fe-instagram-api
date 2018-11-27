from django.contrib.auth import get_user_model
from django.db import models
from fe_core.models import UUIDModel

User = get_user_model()


class Tag(UUIDModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class TagCount(UUIDModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.tag} => {self.count}"
