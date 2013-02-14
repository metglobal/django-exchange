#! /bin/sh
cd test_project
python manage.py syncdb
python manage.py test exchange
