from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('data_presentation.urls')),
    path('admin/', admin.site.urls),
]
