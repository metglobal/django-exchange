import unittest
from mock import patch


class TestConversion(unittest.TestCase):
    def test_convert(self):
        """Test :py:func:``exchange.conversion.convert``"""
        from exchange.conversion import convert, Price
        from exchange.managers import ExchangeRateManager
        price = Price(3, 'USD')
        with patch.object(ExchangeRateManager, 'get_rate', return_value=0.5):
            converted_price = convert(price, 'GBP')
            self.assertEqual(converted_price.value, 1.50)
            self.assertEqual(converted_price.currency, 'GBP')
