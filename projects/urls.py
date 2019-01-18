from django.urls import path

from . import views
from .views import calculate, reset, ProjectView

urlpatterns = [
    path('', views.index, name='index'),
    path('detail', views.ProjectView.as_view(), name='detail'),
    path('api/calculate', views.calculate, name="calculate"),
    path('api/reset', views.reset, name="reset"),
    path('update', views.insert, name="insert"),
]
