from Lunch.settings import *

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# WARNING: Insecure settings. ############################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '454e6r$_043&d*_@b49@*w6fc$k_x(or^9$vgabsn+=-uc$n!i'

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# #######################################################################
