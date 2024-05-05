#!/bin/bash

pip install --upgrade pip

pip install -r requirements.txt

python manage.py makemigrations accounts

python manage.py migrate accounts

python manage.py makemigrations core

python manage.py migrate core

python manage.py makemigrations

python manage.py migrate

# create user groups


python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()

# Check if the superuser already exists
if not User.objects.filter(email='admin@gmail.com').exists():
    User.objects.create_superuser('admin@gmail.com', 'wafulaat@gmail.com', 'admin1234')
EOF