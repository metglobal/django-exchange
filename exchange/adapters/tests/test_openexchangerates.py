from mock import patch

from django.test import TestCase

from exchange.models import Currency, ExchangeRate
from exchange.adapters.openexchangerates import OpenExchangeRatesAdapter


class OpenExchangeRatesAdapterTest(TestCase):

    def test_update(self):
        with patch(
            'exchange.adapters.openexchangerates.OpenExchangeRatesClient')\
                as client:
            currency_dict = {
                'AED': 'United Arab Emirates Dirham',
                'AFN': 'Afghan Afghani',
                'USD': 'USA'
            }
            latest_dict = {
                'disclaimer': "<Disclaimer data>",
                'license': "<License data>",
                'timestamp': 1358150409,
                'base': "USD",
                'rates': {
                    'AED': 3.66,
                    'AFN': 51.22,
                    'USD': 104.74
                }
            }
            client.return_value.currencies.return_value = currency_dict
            client.return_value.latest.return_value = latest_dict
            adapter = OpenExchangeRatesAdapter()
            adapter.update()
            for k, v in currency_dict.items():
                try:
                    Currency.objects.get(code=k)
                except Currency.DoesNotExist, detail:
                    self.fail(detail)
            for k, v in latest_dict['rates'].items():
                try:
                    ExchangeRate.objects.get(
                        source__code='USD',
                        target__code=k,
                        rate=str(v))
                except ExchangeRate.DoesNotExist, detail:
                    self.fail(detail)
