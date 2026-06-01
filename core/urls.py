from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'), # Twój widok wgrywania plików z Celery
    path('reports/', views.import_report_list, name='report_list'),
    path('reports/<int:session_id>/', views.import_report_detail, name='report_detail'),
]