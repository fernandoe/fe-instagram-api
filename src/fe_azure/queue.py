# https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
import os

from azure.servicebus import ServiceBusService, Message

from instagram.models import Tag

HASHTAGS_QUEUE_NAME = 'hashtags'
POSTS_QUEUE_NAME = 'posts'
QUEUE_JOB_TEXT_SEARCH = 'job-text-search'

service_namespace = os.getenv('FE_AZURE_SERVICE_NAMESPACE')
shared_access_posts_key_name = os.getenv('FE_AZURE_SHARED_ACCESS_POSTS_KEY_NAME')
shared_access_posts_key_value = os.getenv('FE_AZURE_SHARED_ACCESS_POSTS_KEY_NAME')

shared_access_hashtags_key_name = os.getenv('FE_AZURE_SHARED_ACCESS_HASHTAGS_KEY_NAME')
shared_access_hashtags_key_value = os.getenv('FE_AZURE_SHARED_ACCESS_HASHTAGS_KEY_VALUE')

post_service = ServiceBusService(service_namespace=service_namespace,
                                 shared_access_key_name=shared_access_posts_key_name,
                                 shared_access_key_value=shared_access_posts_key_value)

hashtag_service = ServiceBusService(service_namespace=service_namespace,
                                    shared_access_key_name=shared_access_hashtags_key_name,
                                    shared_access_key_value=shared_access_hashtags_key_value)

general_service = ServiceBusService(service_namespace='',
                                    shared_access_key_name='',
                                    shared_access_key_value='')


def send_text_search(uuid):
    message = Message(uuid)
    general_service.send_queue_message(QUEUE_JOB_TEXT_SEARCH, message)


def send_tag(name):
    if not name:
        return

    tag, created = Tag.objects.get_or_create(name=name)
    if created or tag.last_count is None:
        message = Message(name)
        hashtag_service.send_queue_message(HASHTAGS_QUEUE_NAME, message)


def send_post(post):
    pass

# bus_service.create_queue('taskqueue', queue_options)
# msg = Message(b'Test Message')
# bus_service.send_queue_message('posts', msg)
