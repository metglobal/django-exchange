import unittest
from mock import patch


class UtilsTest(unittest.TestCase):

    def test_convert(self):
        """Test :py:func:``exchange.utils.convert``"""
        from exchange.utils import convert, Price
        with patch('exchange.utils.ExchangeRates') as exchange_rates:
            exchange_rates.get_instance.return_value = \
                {'USD': {'GBP': 0.5}}
            price = Price(3, 'USD')
            self.assertEqual(convert(price, 'GBP'), 1.50)

    def test_price(self):
        """Test :py:class:``exchange.utils.Price``"""
        from exchange.utils import Price
        with patch('exchange.utils.ExchangeRates') as exchange_rates:
            exchange_rates.get_instance.return_value = \
                {'USD': {'GBP': 0.5}}
            price = Price(3, 'USD')
            self.assertEqual(price.convert('GBP'), 1.50)

    def test_exchangerates(self):
        """Test :py:class:``exchange.utils.ExchangeRates``"""
        from exchange.utils import ExchangeRates
        from exchange.models import Currency, ExchangeRate
        usd = Currency.objects.get(code='USD')
        gbp = Currency.objects.create(code='GBP')
        afn = Currency.objects.create(code='AFN')

        ExchangeRate.objects.create(source=usd, target=gbp, rate='2.00')
        ExchangeRate.objects.create(source=usd, target=afn, rate='3.00')

        rates = ExchangeRates.get_instance()
        rates.populate()
        self.assertIn('USD', rates)
        self.assertIn('GBP', rates['USD'])
        self.assertEqual(rates['USD']['GBP'], 2.00)
        self.assertIn('AFN', rates['USD'])
        self.assertEqual(rates['USD']['AFN'], 3.00)
        rates2 = ExchangeRates.get_instance()
        self.assertEqual(rates, rates2)
        rates.clear()
        self.assertEqual(len(rates), 0)
