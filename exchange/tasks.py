import celery
import backoff
from requests.exceptions import ConnectionError
from exchange.conversion import update_rates


@celery.task
@backoff.on_exception(backoff.expo, ConnectionError, max_tries=3)
def update_task(adapter_class_name=None):
    update_rates(adapter_class_name=adapter_class_name)
