from django.urls import path

from . import views
from .views import get_data, calculate, reset

urlpatterns = [
    path('', views.index, name='index'),
    path('detail', views.detail, name='detail'),
    path('api/data/', get_data, name="api-data"),
    path('api/calculate', calculate, name="calculate"),
    path('api/reset', reset, name="reset"),
]
