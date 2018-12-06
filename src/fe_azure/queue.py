import os

from azure.servicebus import ServiceBusService, Message

SERVICE_BUS_NAMESPACE = os.getenv('FE_AZURE_SERVICE_NAMESPACE')
FE_AZURE_SHARED_ACCESS_KEY_NAME = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_NAME')
FE_AZURE_SHARED_ACCESS_KEY_VALUE = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_VALUE')

QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH = 'job-extract-hashtags-from-text-search'
QUEUE_JOB_EXTRACT_HASHTAG_COUNT = 'job-extract-hashtag-count'

bus_service = ServiceBusService(service_namespace=SERVICE_BUS_NAMESPACE,
                                shared_access_key_name=FE_AZURE_SHARED_ACCESS_KEY_NAME,
                                shared_access_key_value=FE_AZURE_SHARED_ACCESS_KEY_VALUE)


def create_queues(name):
    print(f'=> create_queues({name})')
    bus_service.create_queue(name)


def send_to_job_extract_hashtags_from_text_search(uuid: str) -> None:
    print(f'=> send_to_job_extract_hashtags_from_text_search({uuid})')
    message = Message(uuid)
    bus_service.send_queue_message(QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH, message)


def send_to_job_extract_hashtag_count(hashtag_name: str) -> None:
    print(f'=> send_to_job_extract_hashtag_count({hashtag_name})')
    message = Message(hashtag_name)
    bus_service.send_queue_message(QUEUE_JOB_EXTRACT_HASHTAG_COUNT, message)


def receive_queue_message(queue_name):
    print(f'=> receive_queue_message({queue_name})')
    return bus_service.receive_queue_message(queue_name, peek_lock=True)
