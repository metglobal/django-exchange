from django.db import models


class Currency(models.Model):
    """Model holds a currency information for a nationality"""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.code


class ExchangeRate(models.Model):
    """Model to persist exchange rates between currencies"""
    source = models.ForeignKey('exchange.Currency', related_name='rates')
    target = models.ForeignKey('exchange.Currency')
    rate = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return '%s / %s = %s' % (self.source, self.target, self.rate)
