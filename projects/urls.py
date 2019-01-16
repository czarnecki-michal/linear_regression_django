from django.urls import path

from . import views
from .views import calculate, reset, ProjectView

urlpatterns = [
    path('', views.index, name='index'),
    path('detail', ProjectView.as_view(), name='detail'),
    path('api/calculate', calculate, name="calculate"),
    path('api/reset', reset, name="reset"),
]
