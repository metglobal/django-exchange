from setuptools import setup, find_packages

import exchange

setup(
    name='django-exchange',
    version=exchange.__version__,
    description='currency, exchange rates and conversions support for django',
    long_description=open('README.rst').read(),
    url='https://github.com/metglobal/django-exchange',
    license=exchange.__license__,
    author=exchange.__author__,
    author_email='kadir.pekel@metglobal.com',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    extras_require={
        'openexchangerates': ["openexchangerates"]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
