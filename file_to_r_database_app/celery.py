import os
from celery import Celery

# Ustawiamy domyślny moduł ustawień Django dla programu 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_to_r_database_app.settings')

app = Celery('file_to_r_database_app')

# Pobieramy ustawienia z settings.py (zaczynające się od CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatycznie wykrywa zadania z plików tasks.py w naszych aplikacjach (np. z 'core')
app.autodiscover_tasks()