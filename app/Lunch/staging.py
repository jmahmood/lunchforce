from Lunch.settings import *


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

print(os.environ.get('HEROKU_POSTGRESQL_JADE_URL'))
test_db_from_env = dj_database_url.config(env='HEROKU_POSTGRESQL_JADE_URL', conn_max_age=500)
DATABASES['default']['TEST'].update(test_db_from_env)
print(
    DATABASES
)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['jbm-lunchforce-staging.herokuapp.com']
SECURE_SSL_REDIRECT = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
