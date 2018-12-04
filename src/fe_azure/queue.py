# https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
import os

from azure.servicebus import ServiceBusService

HASHTAGS_QUEUE_NAME = 'hashtags'
POSTS_QUEUE_NAME = 'posts'

service_namespace = os.getenv('FE_AZURE_SERVICE_NAMESPACE')
shared_access_key_name = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_NAME')
shared_access_key_value = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_VALUE')

bus_service = ServiceBusService(
    service_namespace=service_namespace,
    shared_access_key_name=shared_access_key_name,
    shared_access_key_value=shared_access_key_value)


def send_tag(name):
    pass


def send_post(post):
    pass

# bus_service.create_queue('taskqueue', queue_options)
# msg = Message(b'Test Message')
# bus_service.send_queue_message('posts', msg)
