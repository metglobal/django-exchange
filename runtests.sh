#! /bin/sh
cd test_project
python manage.py migrate
python manage.py test exchange
