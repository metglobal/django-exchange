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
automatically. Currently it has built in support for openexhangerates.org service. It is
only a matter of supplying an api key obtained from http://openexhangerates.org as django
settings using the key ``OPENEXCHANGERATES_API_KEY``::

    OPENEXCHANGERATES_API_KEY = '<YOU_API_KEY_HERE>'

Now you can populate you currency and exchange rates magically by typing::

    $ python manage.py update_exchange_rates

If you want to use you own service provider, you should consider implementing
``exchange.adapters.BaseAdapter`` class and pass you implementation class path
as an argument to ``update_exchange_rates`` command::

    $ python manage.py update_exchange_rates -c myproj.providers.MyProvider

Quickstart
-----------

Currency conversions is dead easy. There are auxilaray methods helps you calculate 
conversions using populated exchange rates under ``exchange.conversions`` module.

Take a look at the example below::

    >>> from exchange.conversion import Price, convert
    >>> my_price = Price(50, 'USD')
    >>> my_price.convert('YEN')
    <Price (4678.50 YEN)>

Documentation
-------------

Coming soon...

Todo
----

* Convenient template tags
* Django price field implementation supporting currency conversions
* Easier api with convenient refaactorings
* A few more builtin exchange rate provider

License
-------
Copyright (c) 2013 Metglobal LLC.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
