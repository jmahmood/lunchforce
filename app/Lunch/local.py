import logging

from Lunch.settings import *
import subprocess
# export HEROKU_STAGING_APP_NAME=jbm-lunchforce-staging
#  ./manage.py shell --settings=Lunch.local

db_from_env = dj_database_url.config(conn_max_age=5)
test_db_from_env = dj_database_url.config(env='HEROKU_POSTGRESQL_JADE_URL', conn_max_age=5)
DATABASES['default'].update(db_from_env)
DATABASES['default']['TEST'].update(test_db_from_env)  # Doesn't work correctly.

logging.warning(DATABASES)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

