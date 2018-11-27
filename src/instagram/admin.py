from django.contrib import admin

from .models import Tag, TagCount


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'name')
    list_display = ('get_uuid', 'name')
    ordering = ('name',)


@admin.register(TagCount)
class TagCountModelAdmin(admin.ModelAdmin):
    search_fields = ('uuid', 'tag')
    list_display = ('get_uuid', 'tag', 'count')
    ordering = ('tag',)
