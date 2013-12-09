from django.core.cache import get_cache
from django.conf import settings

from exchange.models import ExchangeRate


CACHE_ENABLED_KEY = 'EXCHANGE_CACHE_ENABLED'
CACHE_ENABLED_DEFAULT = True

CACHE_DATABASE_KEY = 'EXCHANGE_DATABASE'
CACHE_DATABASE_DEFAULT = 'default'

CACHE_KEY_PREFIX_KEY = 'EXCHANGE_CACHE_KEY_PREFIX'
CACHE_KEY_PREFIX_DEFAULT = 'exchange'

CACHE_DATABASE = getattr(settings, CACHE_DATABASE_KEY, CACHE_DATABASE_DEFAULT)
CACHE_ENABLED = getattr(settings, CACHE_ENABLED_KEY, CACHE_ENABLED_DEFAULT)
CACHE_KEY_PREFIX = getattr(settings, CACHE_KEY_PREFIX_KEY,
                           CACHE_KEY_PREFIX_DEFAULT)

CACHE_TIMEOUT = 0  # Not configurable at all

cache = get_cache(CACHE_DATABASE)

local_cache = {}


def _get_cache_key(source_currency, target_currency):
    return ':'.join([CACHE_KEY_PREFIX, source_currency, target_currency])


def update_rates_cached():
    rates = ExchangeRate.objects.all()
    cache_map = {_get_cache_key(rate.source.code, rate.target.code): rate.rate
                 for rate in rates}
    cache.set_many(cache_map, timeout=CACHE_TIMEOUT)
    local_cache.clear()
    return cache_map


def get_rate_cached(source_currency, target_currency):
    key = _get_cache_key(source_currency, target_currency)
    try:
        rate = local_cache[key]
    except KeyError:
        rate = cache.get(key)
        local_cache[key] = rate
    return rate


def get_rates_cached(args_list):
    key_map = {_get_cache_key(*args): args for args in args_list}
    cache_map = cache.get_many(key_map.keys())
    return {key_map[key]: cache_map.get(key) for key in key_map.keys()}
