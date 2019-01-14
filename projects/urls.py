from django.urls import path

from . import views
from .views import get_data

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.detail, name='detail'),
    path('info', views.info, name='info'),
    path('charts', views.charts, name='charts'),
    path('api/data/', get_data, name="api-data"),
]
