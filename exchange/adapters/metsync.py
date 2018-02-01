import os
import json
from decimal import Decimal
from django.conf import settings
from exchange.adapters import BaseAdapter
import requests
from collections import namedtuple

CurrencyTuple = namedtuple('CurrencyTuple', (
    'code', 'name'))


class MetsyncAdapter(BaseAdapter):
    """
    This Adapter uses Metglobals' internal data api to get rates from base
    systems.
    """
    def _request(self, endpoint):
        user = getattr(settings, 'METSYNC_USERNAME', False)
        password = getattr(settings, 'METSYNC_PASSWORD', False)
        url = getattr(settings, 'METSYNC_BASE_URL', False)
        if not (user and password and url):
            raise Exception("Missing configuration")
        url = os.path.join(url, endpoint)

        response = requests.get(url, auth=(user, password))
        if response.ok:
            return json.loads(response.content)
        return []

    def get_currencies(self):
        data = self._request('Currencies/getCurrencyRates')
        result = []
        for key in data.keys():
            result.append(CurrencyTuple(code=key, name=key))
        return result

    def get_exchangerates(self, base):
        data = self._request('Currencies/getCurrencyRates')
        result = []
        for k in data:
            result.append((k, Decimal(str(data[k]))))
        return result
