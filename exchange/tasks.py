import celery

from exchange.conversion import update_rates


@celery.task
def update_task(adapter_class_name=None):
    update_rates(adapter_class_name=adapter_class_name)
