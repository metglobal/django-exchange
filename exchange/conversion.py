from collections import namedtuple

from django.conf import settings

from exchange.adapters import BaseAdapter
from exchange.utils import import_class
from exchange.models import ExchangeRate
from exchange.cache import (update_rates_cached, get_rate_cached,
                            get_rates_cached, CACHE_ENABLED)

Price = namedtuple('Price', ('value', 'currency'))

EXCHANGE_ADAPTER_CLASS_KEY = 'EXCHANGE_ADAPTER_CLASS'
EXCHANGE_DEFAULT_ADAPTER_CLASS = \
    'exchange.adapters.openexchangerates.OpenExchangeRatesAdapter'


def update_rates(adapter_class_name=None):
    adapter_class_name = (adapter_class_name or
                          getattr(settings,
                                  EXCHANGE_ADAPTER_CLASS_KEY,
                                  EXCHANGE_DEFAULT_ADAPTER_CLASS))

    adapter_class = import_class(adapter_class_name)
    adapter = adapter_class()
    if not isinstance(adapter, BaseAdapter):
        raise TypeError("invalid adapter class: %s" % adapter_class_name)
    adapter.update()

    if CACHE_ENABLED:
        update_rates_cached()


def convert_values(args_list):
    value_map = {}
    rate_map = {}
    conversions = {args[1:3] for args in args_list}

    if CACHE_ENABLED:
        rate_map = get_rates_cached(conversions)

    for args in args_list:
        conversion = args[1:3]
        rate = rate_map.get(conversion)
        if not rate:
            rate = ExchangeRate.objects.get_rate(conversion[1], conversion[2])
        value_map[args] = rate

    return value_map


def get_rate(source_currency, target_currency):
    rate = None
    if CACHE_ENABLED:
        rate = get_rate_cached(source_currency, target_currency)

    if not rate:
        rate = ExchangeRate.objects.get_rate(source_currency, target_currency)

    return rate


def convert_value(value, source_currency, target_currency):
    """Converts the price of a currency to another one using exhange rates

    :param price: the price value
    :param type: decimal

    :param source_currency: source ISO-4217 currency code
    :param type: str

    :param target_currency: target ISO-4217 currency code
    :param type: str

    :returns: converted price instance
    :rtype: ``Price``

    """
    # If price currency and target currency is same
    # return given currency as is
    if source_currency == target_currency:
        return value

    rate = get_rate(source_currency, target_currency)

    return value * rate


def convert(price, currency):
    """Shorthand function converts a price object instance of a source
    currency to target currency

    :param price: the price value
    :param type: decimal

    :param currency: target ISO-4217 currency code
    :param type: str

    :returns: converted price instance
    :rtype: ``Price``

    """
    # If price currency and target currency is same
    # return given currency as is
    value = convert_value(price.value, price.currency, currency)
    return Price(value, currency)
