import celery

from exchange.adapters import update


@celery.task
def update_task(adapter_class_name=None):
    update(adapter_class_name=adapter_class_name)
