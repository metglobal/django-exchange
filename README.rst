===============
django-exchange
===============
Currency, exchange rate and conversions support for django projects.

Install
-------

``django-exchange`` is available on pypi repositories so youre free to use
``pip`` or ``easy_install``::

    $ pip install django-exchange

Or you might want to install from source::

    $ wget https://github.com/metglobal/django-exchange/archive/django-exchange-xxx.zip
    $ unzip django-exchange-xxx.zip
    $ cd django-exchange-xxx
    $ python setup.py install

Add ``exchange`` into your ``INSTALLED_APPS`` settings of your django project::

    INSTALLED_APPS += [
        'exchange',
    ]

Don't forget to sync your db to create corresponding database tables::

    $ python manage.py syncdb

Populating Data
---------------

django-exchange supports populating currency and exchange rates using a service provider
automatically. Currently it has built in support for openexchangerates.org service. It is
only a matter of supplying an api key obtained from http://openexchangerates.org as django
settings using the key ``OPENEXCHANGERATES_API_KEY``::

    OPENEXCHANGERATES_API_KEY = '<YOU_API_KEY_HERE>'

Now you can populate you currency and exchange rates magically by typing::

    $ python manage.py update_rates


Quickstart
-----------

Currency conversions is dead easy. There are auxilaray methods helps you calculate
conversions using populated exchange rates under ``exchange.conversions`` module.

Take a look at the example below::

    >>> from exchange.conversion import Price, convert
    >>> my_price = Price(50, 'USD')
    >>> convert(my_price, 'EUR')
    <Price(value=Decimal('36.68585000'), currency='EUR')>

Documentation
-------------

Coming soon...

Todo
----

* Convenient template tags
* Django price field implementation supporting currency conversions
* Easier api with convenient refaactorings
* A few more builtin exchange rate provider
