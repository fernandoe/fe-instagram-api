import logging
import os

from azure.common import AzureHttpError
from azure.servicebus import ServiceBusService, Message
from requests.exceptions import ConnectionError, ReadTimeout

logger = logging.getLogger(__name__)

SERVICE_BUS_NAMESPACE = os.getenv('FE_AZURE_SERVICE_NAMESPACE')
FE_AZURE_SHARED_ACCESS_KEY_NAME = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_NAME')
FE_AZURE_SHARED_ACCESS_KEY_VALUE = os.getenv('FE_AZURE_SHARED_ACCESS_KEY_VALUE')

QUEUE_TEXT_SEARCH = 'text-search'
QUEUE_HASHTAG = 'hashtag'

bus_service = ServiceBusService(service_namespace=SERVICE_BUS_NAMESPACE,
                                shared_access_key_name=FE_AZURE_SHARED_ACCESS_KEY_NAME,
                                shared_access_key_value=FE_AZURE_SHARED_ACCESS_KEY_VALUE)


def create_queues(name):
    logger.info(f'=> create_queues({name})')
    bus_service.create_queue(name)


def send_to_queue_text_search(uuid: str) -> None:
    logger.info(f'=> send_to_queue_text_search({uuid})')
    message = Message(uuid)
    bus_service.send_queue_message(QUEUE_TEXT_SEARCH, message)


def send_to_queue_hashtag(hashtag: str) -> None:
    logger.info(f'=> send_to_queue_hashtag({hashtag})')
    message = Message(hashtag)
    bus_service.send_queue_message(QUEUE_HASHTAG, message)


def receive_queue_message(queue_name):
    logger.info(f'=> receive_queue_message({queue_name})')
    try:
        return bus_service.receive_queue_message(queue_name, peek_lock=True)
    except AzureHttpError as err:
        logger.error(f'AzureHttpError: {err}')
    except ConnectionError as err:
        logger.error(f'ConnectionError: {err}')
    except ReadTimeout as err:
        logger.error(f'ReadTimeout: {err}')
    return None
