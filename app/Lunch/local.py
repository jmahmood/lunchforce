from Lunch.settings import *
import subprocess


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
DATABASES['default']['TEST'].update(db_from_env)
print(
    DATABASES
)
print(
    os.environ
)

# WARNING: Insecure settings. ############################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# #######################################################################
