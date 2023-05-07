from __future__ import absolute_import, unicode_literals
from datetime import timedelta

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djolowin.settings')

app = Celery('djolowin')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "check_auction_end": {
        "task": "auction.tasks.check_auction_end",
        "schedule": timedelta(minutes=1),
    },
    "check_auction_endings": {
        "task": "auction.tasks.check_auction_ending_soon",
        "schedule": timedelta(minutes=30),
    },
}