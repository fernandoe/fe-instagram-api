import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from instagram.models import Tag, TagPriority

connections.create_connection(hosts=[os.getenv('FE_ELASTICSEARCH_HOST')])


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
    tag = request.GET.get('tag')
    s = Search(index="post-index").query("match", tags=tag)
    s.aggs.bucket('wordcloud', 'terms', field='tags')
    response = s.execute()
    for hit in response:
        print(hit)

    result = []
    result_count = []
    index = []
    for idx, tag in enumerate(response.aggregations.wordcloud.buckets):
        print(f"{idx}: {tag}")
        result.append(f"#{tag.key}")
        result_count.append(f"{tag.doc_count}".ljust(len(tag.key) + 1))
        index.append(f"{idx+1}".ljust(len(tag.key) + 1))

    r = ' '.join(result) + '\n' + ' '.join(result_count) + '\n' + ' '.join(index) + '\nResults: ' + str(len(result))
    return HttpResponse(r, status=200)

# def tags(request):
#     hashtags = request.GET.get('tags', '').split(' ')
#     limit = request.GET.get('limit', '30')
#     tags = Tag.objects.filter(name__in=hashtags, last_count__isnull=False).order_by('-last_count')[:int(limit)]
#     result = ''
#     result_count = ''
#     count = tags.count()
#     if count > 0:
#         for tag in tags:
#             result += f"#{tag.name} "
#             result_count += f"#{tag.last_count} "
#     return HttpResponse(result + '\n' + result_count + '\nResults: ' + str(count), status=200)
