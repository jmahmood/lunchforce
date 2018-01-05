"""Environmental variables for the pre-production / staging environment."""

from Lunch.settings import *

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

test_db_from_env = dj_database_url.config(env='HEROKU_POSTGRESQL_JADE_URL', conn_max_age=500)
DATABASES['default']['TEST'].update(test_db_from_env)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['jbm-lunchforce-staging.herokuapp.com']
SECURE_SSL_REDIRECT = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', '')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', '')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')
EMAIL_SUBJECT_PREFIX = 'Staging LunchForce'


DEFAULT_FROM_EMAIL = 'Jawaad Mahmood <jawaad.mahmood@ordisante.com>'
ADMINS = (
    ('Jawaad Mahmood', 'jawaad.mahmood@ordisante.com'),
)
MANAGERS = ADMINS

