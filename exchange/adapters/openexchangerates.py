from __future__ import absolute_import

import logging
from openexchangerates import OpenExchangeRatesClient

from django.conf import settings

from exchange.adapters import BaseAdapter

logger = logging.getLogger(__name__)


class OpenExchangeRatesAdapter(BaseAdapter):
    """This adapter uses openexchangerates.org service to populate currency and
    exchange rate models.

    """

    API_KEY_SETTINGS_KEY = 'OPENEXCHANGERATES_API_KEY'

    def __init__(self):
        self.client = OpenExchangeRatesClient(
            getattr(settings, self.API_KEY_SETTINGS_KEY))

    def get_currencies(self):
        return self.client.currencies().items()

    def get_exchangerates(self, base):
        return self.client.latest(base)['rates'].items()
