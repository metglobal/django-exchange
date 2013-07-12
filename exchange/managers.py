from django.db import models


class ExchangeRateManager(models.Manager):

    def get_query_set(self):
        return super(ExchangeRateManager, self).get_query_set()\
            .select_related('source', 'target')
