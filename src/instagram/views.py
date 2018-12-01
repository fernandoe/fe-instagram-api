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


def tags(request):
    hashtags = request.GET.get('tags', '').split(' ')
    limit = request.GET.get('limit', '30')
    tags = Tag.objects.filter(name__in=hashtags, last_count__isnull=False).order_by('-last_count')[:int(limit)]
    result = ''
    result_count = ''
    count = tags.count()
    if count > 0:
        for tag in tags:
            result += f"#{tag.name} "
            result_count += f"#{tag.last_count} "
    return HttpResponse(result + '\n' + result_count + '\nResults: ' + str(count), status=200)
