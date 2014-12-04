import django
from django.db import models


class ExchangeRateManager(models.Manager):

    def get_queryset(self):
        super_ = super(ExchangeRateManager, self)
        if django.VERSION < (1, 7):
            qs = super_.get_query_set()
        else:
            qs = super_.get_queryset()
        return qs.select_related('source', 'target')

    if django.VERSION < (1, 7):
        get_query_set = get_queryset

    def get_rate(self, source_currency, target_currency):
        return self.get(source__code=source_currency,
                        target__code=target_currency).rate
