import os
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from instagram.models import Tag, TagPriority, TextSearch

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
    s.aggs.bucket('wordcloud', 'terms', field='tags', size=35)
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


def search(request):
    q = request.GET.get('q', None)
    limit = request.GET.get('limit', '30')
    return search_impl(q, limit)


def search_impl(q, limit):
    try:
        limit = int(limit)
    except ValueError:
        limit = 30

    result = {
        'items': []
    }

    if q:
        s = Search(index="post-index").query("match", tags=q)
        s.aggs.bucket('wordcloud', 'terms', field='tags', size=limit)
        response = s.execute()
        for hit in response:
            print(hit)

        # get tags in our database
        tag_list = []
        for tag in response.aggregations.wordcloud.buckets:
            tag_list.append(tag.key)

        tags_in_database = {}
        for tag in Tag.objects.filter(name__in=tag_list):
            tags_in_database[tag] = tag.last_count

        for idx, tag in enumerate(response.aggregations.wordcloud.buckets):
            print(f"{idx}: {tag}")
            result['items'].append({
                'name': tag.key,
                'count': tags_in_database[tag.key] if tag.key in tags_in_database else None,
                'doc_count': tag.doc_count,
                'index': idx + 1
            })
        TextSearch.objects.create(text=q, result=json.dumps(result))
    return JsonResponse(result)
