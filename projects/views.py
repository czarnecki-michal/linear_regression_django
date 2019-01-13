from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Data

def index(request):
    return render(request, 'projects/index.html')

def detail(request):
    train_data = Data.objects.all()[:47]
    test_data = Data.objects.all()[47:]
    return render(request, 'projects/data.html', {'train_data': train_data, 'test_data': test_data})