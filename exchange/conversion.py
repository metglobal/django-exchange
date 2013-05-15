from django.core.cache import cache
from django.conf import settings

from exchange.models import ExchangeRate

CACHE_ENABLED_KEY = 'EXCHANGE_CACHE_ENABLED'
CACHE_KEY_KEY = 'EXCHANGE_CACHE_KEY'

CACHE_ENABLED = True
CACHE_KEY = 'exchange_rates'


Price = namedtuple('Price', ('value', 'currency'))


class ExchangeRateNotFound(Exception):

    def __init__(self, source_currency, target_currency):
        super(ExchangeRateNotFound, self).__init__(
            '%s -> %s' % (source_currency, target_currency))


def get_cache_key():
    return getattr(settings, self.CACHE_KEY_KEY, CACHE_KEY)


def get_cache_enabled():
    return getattr(settings, self.CACHE_ENABLED_KEY, CACHE_ENABLED)


def populate_exchange_rates():
    table = {}
    rates = ExchangeRate.objects.all().select_related('source', 'target')
    for rate in rates:
        if rate.source.code not in table:
            table[rate.source.code] = {}
        table[rate.source.code][rate.target.code] = rate.rate
    return table


def get_exchangerate_cache():
    if get_cache_enabled():
        cache_key = get_cache_key()
        exchange_rates = cache.get(cache_key)
        if not exchange_rates:
            exchange_rates = populate_exchange_rates()
            cache.set(cache_key, exchange_rates)
    else:
        exchange_rates = populate_exchange_rates()
    return exchange_rates


def reset_exhangerate_cache():
    cache_key = getattr(settings, self.CACHE_KEY_KEY, CACHE_KEY)


def get_rate(source_currency, target_currency):
    exchange_rate_cache = get_exchangerate_cache()
    try:
        source = exchange_rate_cache[source_currency]
        return source.get(target_currency)
    except KeyError:
        raise ExchangeRateNotFound(source_currency, target_currency)


def convert(value, source_currency, target_currency):
    """Converts the price of a currency to another one using exhange rates

    :param price: the price value
    :param type: decimal

    :param currency: ISO-4217 currency code
    :param type: str

    :returns: converted value
    :rtype: decimal

    """
    rate = get_rate(source_currency, target_currency)
    return value * rate


def convert_price(price, target_currency):
    return Price(convert(price.value, price.currency, target_currency),
                 target_currency)
