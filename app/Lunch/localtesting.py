from Lunch.settings import *

# export HEROKU_STAGING_APP_NAME=jbm-lunchforce-staging
#  ./manage.py shell --settings=Lunch.local

db_from_env = dj_database_url.config(conn_max_age=5)
test_db_from_env = dj_database_url.config(env='HEROKU_POSTGRESQL_JADE_URL', conn_max_age=5)
DATABASES['default'].update(test_db_from_env)
DATABASES['default']['TEST'].update(test_db_from_env)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    'version': 1,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    },
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
