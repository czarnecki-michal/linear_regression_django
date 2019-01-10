from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Data

def index(request):
    return render(request, 'data_presentation/index.html')

def show(request):
    my_data_list = Data.objects.all()
    return render(request, 'data_presentation/show.html', {'my_data_list': my_data_list})
