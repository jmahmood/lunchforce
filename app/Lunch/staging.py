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

EMAIL_HOST = os.getenv('MAILGUN_SMTP_SERVER', '')
EMAIL_PORT = os.getenv('MAILGUN_SMTP_PORT', '')
EMAIL_HOST_USER = os.getenv('MAILGUN_SMTP_LOGIN', ''),
EMAIL_HOST_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD', ''),
EMAIL_SUBJECT_PREFIX = 'Staging LunchForce'
EMAIL_USE_TLS = True
