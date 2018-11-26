from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from fe_core.models import Entity, UUIDModel

User = get_user_model()


class Tag(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
