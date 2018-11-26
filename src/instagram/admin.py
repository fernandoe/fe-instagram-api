from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'name')
    list_display = ('get_uuid', 'name')
    ordering = ('name',)
