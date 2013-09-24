from setuptools import setup

setup(
    name='django-exchange',
    packages=['exchange'],
    version='0.0.4',
    description='currency, exchange rates and conversions support for django',
    author='Metglobal',
    author_email='kadir.pekel@metglobal.com',
    url='https://github.com/metglobal/django-exchange',
    extras_require={
        'openexchangerates': ["openexchangerates"]
    }
)
