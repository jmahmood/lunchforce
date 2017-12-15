import logging

from Lunch.settings import *
import subprocess
# export HEROKU_STAGING_APP_NAME=jbm-lunchforce-staging
#  ./manage.py shell --settings=Lunch.local

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
DATABASES['default']['TEST'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = None

logging.warning(DATABASES)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
