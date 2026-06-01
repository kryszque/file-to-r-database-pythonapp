import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_to_r_database_app.settings')

app = Celery('file_to_r_database_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()