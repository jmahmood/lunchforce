from Lunch.settings import *


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
test_env_database_key = [k for k in os.environ.keys() if k.startswith('HEROKU_POSTGRESQL_') and k.endswith('_URL')][0]
print(test_env_database_key)
test_db_from_env = dj_database_url.config(env=test_env_database_key, conn_max_age=500)
DATABASES['default']['TEST'].update(test_db_from_env)
print(DATABASES)
print(os.environ)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['jbm-lunchforce-staging.herokuapp.com']
SECURE_SSL_REDIRECT = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
