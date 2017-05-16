import logging
from decimal import Decimal

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

        # Currencies which exist on db (not exist on currencies coming from
        # openexchangerates api) should be deleted from db.
        currencies_on_db = list(Currency.objects.all())
        for currency in currencies_on_db:
            if (currency.code, currency.name) not in currencies:
                currency.delete()

        for code, name in currencies:
            _, created = Currency.objects.get_or_create(
                code=code, defaults={'name': name})
            if created:
                logger.debug('currency: %s created', code)

        existing = ExchangeRate.objects.values('source__code',
                                               'target__code',
                                               'id')
        existing = {(d['source__code'], d['target__code']): d['id']
                    for d in existing}
        usd_exchange_rates = dict(self.get_exchangerates('USD'))

        updates = []
        inserts = []
        for source in currencies_on_db:
            for target in currencies_on_db:
                rate = self._get_rate_through_usd(source.code,
                                                  target.code,
                                                  usd_exchange_rates)

                exchange_rate = ExchangeRate(source=source,
                                             target=target,
                                             rate=rate)

                if (source.code, target.code) in existing:
                    exchange_rate.id = existing[(source.code, target.code)]
                    updates.append(exchange_rate)
                    logger.debug('exchange rate updated %s/%s=%s'
                                 % (source, target, rate))
                else:
                    inserts.append(exchange_rate)
                    logger.debug('exchange rate created %s/%s=%s'
                                 % (source, target, rate))

            logger.debug('exchange rates updated for %s' % source.code)
        logger.debug("Updating %s rows" % len(updates))
        update_many(updates)
        logger.debug("Inserting %s rows" % len(inserts))
        insert_many(inserts)
        logger.debug('saved rates to db')

    def _get_rate_through_usd(self, source, target, usd_rates):
        # from: https://openexchangerates.org/documentation#how-to-use
        # gbp_hkd = usd_hkd * (1 / usd_gbp)
        usd_source = usd_rates[source]
        usd_target = usd_rates[target]
        rate = Decimal(usd_target) * (Decimal(1.0) / Decimal(usd_source))
        rate = rate.quantize(Decimal('0.123456'))  # round to 6 decimal places
        return rate

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
