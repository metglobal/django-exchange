from exchange.models import Currency, ExchangeRate


def convert(price, currency):
    """Converts the price of a currency to another one using exhange rates

    :param price: the price value
    :param type: decimal

    :param currency: ISO-4217 currency code
    :param type: str

    """
    rates = ExchangeRates.get_instance()
    return price.value * rates[price.currency][currency]


class Price(object):
    """Class holds the information of a price value with its currency"""

    def __init__(self, value, currency):
        """Convenient constrcutor

        :param value: the price value
        :param type: decimal

        :param currency: ISO-4217 currency code
        :param type: str

        """
        self.value = value
        self.currency = currency

    def convert(self, currency):
        """Converts the price of a currency hold by currenct instance to
        another one

        :param currency: ISO-4217 currency code
        :param type: str

        """
        return convert(self, currency)


class ExchangeRates(dict):
    """Singleton dictionary implementation which hold the exchange rates
    populated from corresponding database models.

    """
    _instance = None

    @classmethod
    def get_instance(cls):
        """Singleton instance method"""
        if not cls._instance:
            cls._instance = ExchangeRates()
            cls._instance.populate()
        return cls._instance

    def reset(self):
        """Clears all the exchange rate data"""
        self.clear()

    def populate(self):
        """Clears and populates all the exchange rate data via database"""
        self.reset()
        currencies = Currency.objects.all()
        for source_currency in currencies:
            self[source_currency.code] = {}
            for rate in source_currency.rates.all():
                self[source_currency.code][rate.target.code] = rate.rate
