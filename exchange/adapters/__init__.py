import logging

from exchange.models import Currency, ExchangeRate

from exchange.utils import update_many, insert_many

logger = logging.getLogger(__name__)


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

        pairs = set(ExchangeRate.objects.values_list('source__code',
                                                     'target__code'))
        updates = []
        inserts = []
        for source in Currency.objects.all():
            exchange_rates = self.get_exchangerates(source.code) or []
            for code, rate in exchange_rates:
                target = Currency.objects.get(code=code)
                exchange_rate = ExchangeRate(source=source,
                                             target=target,
                                             rate=rate)
                if (source.code, target.code) in pairs:
                    updates.append(exchange_rate)
                    logger.debug('exchange rate updated %s/%s=%s'
                                 % (source, target, rate))
                else:
                    inserts.append(exchange_rate)
                    logger.debug('exchange rate created %s/%s=%s'
                                 % (source, target, rate))

            logger.info('exchange rates updated for %s' % source.code)
        update_many(updates)
        insert_many(inserts)
        logger.info('saved rates to db')

    def get_currencies(self):
        """Subclasses must implement this to provide all currency data

        :returns: currency tuples ``[(currency_code, currency_name),]``
        :rtype: list

        """
        raise NotImplementedError()

    def get_exchangerates(self, base):
        """Subclasses must implement this to provide corresponding exchange
        rates for given base currency

        :returns: exchange rate tuples ``[(currency_code, rate),]``
        :rtype: list

        """
        raise NotImplementedError()
