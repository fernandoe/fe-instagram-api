# # https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
#
# from azure.servicebus import ServiceBusService, Message
#
# from instagram.models import Tag
#
# SERVICE_BUS_NAMESPACE = 'hashtags-development'
#
# # HASHTAGS_QUEUE_NAME = 'hashtags'
# # POSTS_QUEUE_NAME = 'posts'
#
# QUEUE_JOB_TEXT_SEARCH = 'job-text-search'
# QUEUE_JOB_EXTRACT_HASHTAG_COUNT = 'job-extract-hashtag-count'
#
# # service_namespace = os.getenv('FE_AZURE_SERVICE_NAMESPACE')
# # shared_access_posts_key_name = os.getenv('FE_AZURE_SHARED_ACCESS_POSTS_KEY_NAME')
# # shared_access_posts_key_value = os.getenv('FE_AZURE_SHARED_ACCESS_POSTS_KEY_NAME')
# #
# # shared_access_hashtags_key_name = os.getenv('FE_AZURE_SHARED_ACCESS_HASHTAGS_KEY_NAME')
# # shared_access_hashtags_key_value = os.getenv('FE_AZURE_SHARED_ACCESS_HASHTAGS_KEY_VALUE')
# #
# # post_service = ServiceBusService(service_namespace=service_namespace,
# #                                  shared_access_key_name=shared_access_posts_key_name,
# #                                  shared_access_key_value=shared_access_posts_key_value)
# #
# # hashtag_service = ServiceBusService(service_namespace=service_namespace,
# #                                     shared_access_key_name=shared_access_hashtags_key_name,
# #                                     shared_access_key_value=shared_access_hashtags_key_value)
#
# bus_service = ServiceBusService(service_namespace=SERVICE_BUS_NAMESPACE,
#                                 shared_access_key_name='',
#                                 shared_access_key_value='')
#
#
#
# def create_queues(name):
#     bus_service.create_queue(name)
#
#
# def send_text_search(uuid):
#     message = Message(uuid)
#     bus_service.send_queue_message(QUEUE_JOB_TEXT_SEARCH, message)
#
#
# def send_hashtag_to_extract_count(hashtag):
#     message = Message(hashtag)
#     bus_service.send_queue_message(QUEUE_JOB_HASHTAG_EXTRACT_COUNT, message)
#
#
# def send_tag(name):
#     if not name:
#         return
#     return
#     # tag, created = Tag.objects.get_or_create(name=name)
#     # if created or tag.last_count is None:
#     #     message = Message(name)
#     #     bus_service.send_queue_message(HASHTAGS_QUEUE_NAME, message)
#
#
# def send_post(post):
#     pass
#
#
# def receive_queue_message(queue_name):
#     return bus_service.receive_queue_message(queue_name, peek_lock=True)
#
# # msg =
# # print(msg.body)
#
# # bus_service.create_queue('taskqueue', queue_options)
# # msg = Message(b'Test Message')
# # bus_service.send_queue_message('posts', msg)
