from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic import View

from .models import Data

def index(request):
    return render(request, 'projects/index.html')

def detail(request):
    train_data = Data.objects.all()[:47]
    test_data = Data.objects.all()[47:]
    return render(request, 'projects/data.html', {'train_data': train_data, 'test_data': test_data})

def info(request):
    return render(request, 'projects/info.html')

def charts(request):
    return render(request, 'projects/charts.html')

class ChartsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'projects/charts.html')

def get_data(request):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)