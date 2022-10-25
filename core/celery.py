from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

app = Celery('core')
app.config_from_object('django.conf:core', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(enable_utc=True, timezone='Asia/Tashkent')

# app.conf.beat_schedule = {
#     "check_spam_email_every_1_minutes": {
#         "task": "check_spam_email",
#         "schedule": crontab(minute='*/1')
#     },
#     "printer": {
#         'task': 'task.add',
#         'schedule': crontab(minute='*/1'),
#         'args': (16, 16),
#     }
# }