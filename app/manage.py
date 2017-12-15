#!/usr/bin/env python

import subprocess

import os
import sys
import json

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lunch.settings")
    # We want to always use the same staging DB, simply to avoid the effect of having a different environment when
    # developing and deploying.  We use the heroku cli to get the correct info and set it as the environmental name.
    # You can't hardcode DBs, the URL is constantly changing.

    if os.environ.get('DATABASE_URL', None) is None:
        # We only use this locally, don't try this at home.
        cmd = 'heroku config --json -a {0}'.format(os.environ.get('HEROKU_STAGING_APP_NAME')).split(' ')
        sbp = subprocess.run(cmd, stdout=subprocess.PIPE)
        raw = sbp.stdout.decode('utf8')
        js_raw = json.loads(raw.replace('\n', ''))

        for v in ['KAFKA_CLIENT_CERT', 'DATABASE_URL', 'KAFKA_URL', 'DJANGO_SECRET_KEY']:
            os.environ.setdefault(v, js_raw.get(v))
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
