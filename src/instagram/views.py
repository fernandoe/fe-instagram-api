from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from instagram.models import Tag, TagPriority


@csrf_exempt
def tag_priority(request):
    hashtags = request.POST.get('tags', '').split(' ')
    for hashtag in hashtags:
        try:
            tag = Tag.objects.get(name=hashtag)
            TagPriority.objects.create(tag=tag)
        except Tag.DoesNotExist:
            continue
    return HttpResponse(status=201)
