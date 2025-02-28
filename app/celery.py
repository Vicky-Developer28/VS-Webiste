# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in the registered Django app.
app.autodiscover_tasks()

# Define periodic tasks (Beat schedule)
app.conf.beat_schedule = {
    'send-daily-messages': {
        'task': 'myapp.tasks.send_daily_messages',  # Update with your app name
        'schedule': crontab(hour=0, minute=0),  # Run every day at midnight
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
