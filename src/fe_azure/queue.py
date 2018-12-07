import logging
import os

from azure.common import AzureHttpError
from azure.servicebus import ServiceBusService, Message
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)

SERVICE_BUS_NAMESPACE = os.getenv('FE_AZURE_SERVICE_NAMESPACE')
FE_AZURE_SHARED_ACCESS_KEY_NAME = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_NAME')
FE_AZURE_SHARED_ACCESS_KEY_VALUE = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_VALUE')

QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH = 'job-extract-hashtags-from-text-search'
QUEUE_JOB_EXTRACT_HASHTAG_COUNT = 'job-extract-hashtag-count'
QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG = 'job-extract-post-from-hashtag'
QUEUE_JOB_PREPARE_POST_TO_IMPORT_TO_ELASTICSEARCH = 'job-prepare-post-to-import-to-elasticsearch'

bus_service = ServiceBusService(service_namespace=SERVICE_BUS_NAMESPACE,
                                shared_access_key_name=FE_AZURE_SHARED_ACCESS_KEY_NAME,
                                shared_access_key_value=FE_AZURE_SHARED_ACCESS_KEY_VALUE)


def create_queues(name):
    logger.info(f'=> create_queues({name})')
    bus_service.create_queue(name)


def send_to_job_extract_hashtags_from_text_search(uuid: str) -> None:
    logger.info(f'=> send_to_job_extract_hashtags_from_text_search({uuid})')
    message = Message(uuid)
    bus_service.send_queue_message(QUEUE_JOB_EXTRACT_HASHTAGS_FROM_TEXT_SEARCH, message)


def send_to_job_extract_hashtag_count(hashtag_name: str) -> None:
    logger.info(f'=> send_to_job_extract_hashtag_count({hashtag_name})')
    message = Message(hashtag_name)
    bus_service.send_queue_message(QUEUE_JOB_EXTRACT_HASHTAG_COUNT, message)


def send_to_job_extract_post_from_hashtag(hashtag_name: str) -> None:
    logger.info(f'=> send_to_job_extract_post_from_hashtag({hashtag_name})')
    message = Message(hashtag_name)
    bus_service.send_queue_message(QUEUE_JOB_EXTRACT_POST_FROM_HASHTAG, message)


def send_to_job_prepare_post_to_import_to_elasticsearch(uuid: str) -> None:
    logger.info(f'=> send_to_job_prepare_post_to_import_to_elasticsearch({uuid})')
    message = Message(uuid)
    bus_service.send_queue_message(QUEUE_JOB_PREPARE_POST_TO_IMPORT_TO_ELASTICSEARCH, message)


def receive_queue_message(queue_name):
    logger.info(f'=> receive_queue_message({queue_name})')
    try:
        return bus_service.receive_queue_message(queue_name, peek_lock=True)
    except AzureHttpError as err:
        logger.error(f'AzureHttpError: {err}')
    except ConnectionError as err:
        logger.error(f'ConnectionError: {err}')
    return None
