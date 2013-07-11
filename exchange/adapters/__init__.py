import logging

from django.conf import settings

from exchange.utils import import_class
from exchange.models import Currency, ExchangeRate


logger = logging.getLogger(__name__)


EXCHANGE_ADAPTER_CLASS_KEY = 'EXCHANGE_ADAPTER_CLASS'
EXCHANGE_DEFAULT_ADAPTER_CLASS = \
    'exchange.adapters.openexchangerates.OpenExchangeRatesAdapter'


def update(adapter_class_name=None):
    adapter_class_name = (adapter_class_name or
                          getattr(settings,
                                  EXCHANGE_ADAPTER_CLASS_KEY,
                                  EXCHANGE_DEFAULT_ADAPTER_CLASS))

    adapter_class = import_class(adapter_class_name)
    adapter = adapter_class()
    if not isinstance(adapter, BaseAdapter):
        raise TypeError("invalid adapter class: %s" % adapter_class_name)
    adapter.update()


class BaseAdapter(object):
    """Base adapter class provides an interface for updating currency and
    exchange rate models

    """
    def update(self):
        """Actual update process goes here using auxialary ``get_currencies``
        and ``get_exchangerates`` methods. This method creates or updates
        corresponding ``Currency`` and ``ExchangeRate`` models

        """
        currencies = self.get_currencies()
        for code, name in currencies:
            _, created = Currency.objects.get_or_create(
                code=code, defaults={'name': name})
            if created:
                logger.info('currency: %s created', code)

        for source in Currency.objects.all():
            exchange_rates = self.get_exchangerates(source.code) or []
            for code, rate in exchange_rates:
                try:
                    target = Currency.objects.get(code=code)
                    exchange_rate = ExchangeRate.objects.get(source=source,
                                                             target=target)
                    exchange_rate.rate = rate
                    exchange_rate.save()
                    logger.info('exchange rate updated %s/%s=%s'
                                % (source, target, rate))
                except ExchangeRate.DoesNotExist:
                    exchange_rate = ExchangeRate.objects.create(
                        source=source, target=target, rate=rate)
                    logger.info('exchange rate created %s/%s=%s'
                                % (source, target, rate))

    def get_currencies(self):
        """Subclasses must implement this to provide all currency data

        :returns: currency tuples ``[(currency_code, currency_name),]``
        :rtype: list

        """
        raise NotImplemented()

    def get_exchangerates(self, base):
        """Subclasses must implement this to provide corresponding exchange
        rates for given base currency

        :returns: exchange rate tuples ``[(currency_code, rate),]``
        :rtype: list

        """
        raise NotImplemented()
