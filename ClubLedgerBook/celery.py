# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClubLedgerBook.settings')

# create a Celery instance and configure it.
app = Celery('ClubLedgerBook')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Use a string here to fully support Windows.
app.autodiscover_tasks()

# Schedule tasks
app.conf.beat_schedule = {
    'calculate-opening-closing-stock': {
        'task': 'api.tasks.calculate_opening_closing_stock',
        'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
    },
}
