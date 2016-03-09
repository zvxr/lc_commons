"""Configures and instantiates the Celery application.
"""

import kombu
import lc_commons.config as lc_config

from celery import Celery
from celery.schedules import crontab


class CeleryConfiguration(object):
    """An object wrapper for celery configuration when calling `app.config_from_object`."""

    BROKER_URL = "amqp://%(user)s:%(password)s@%(host)s" % {
        'user': lc_config.RABBIT_USER,
        'password': lc_config.RABBIT_PASSWORD,
        'host': lc_config.RABBIT_HOST
    }

    CELERYBEAT_SCHEDULE = {
        'get_listed_loans_every_minute': {
            'task': 'get_listed_loans',
            'schedule': crontab(minute='*')
        },
    }

    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_ENABLE_UTC = True
    CELERY_DEFAULT_QUEUE = "unspecified"
    CELERY_QUEUES = (
        kombu.Queue(
            'weekly_aggregators',
            kombu.Exchange('lending_club'),
            routing_key='events'
        ),
    )

    CELERYD_CONCURRENCY = lc_config.CELERY_WORKERS
    CELERYD_PREFETCH_MULTIPLIER = lc_config.CELERY_PREFETCH_MULTIPLIER

    CELERY_IMPORTS = (
        'lc_commons.main.extractors.api',
    )

    def __init__(self):
        pass


# Celery initialization
app = Celery()
app.config_from_object(CeleryConfiguration())
