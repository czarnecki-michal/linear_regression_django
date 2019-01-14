from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic import View
from django.core import serializers


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

def get_data(request):
    worked_years = [data.workedYears for data in Data.objects.all()]
    salary_brutto = [data.salaryBrutto for data in Data.objects.all()]
    data = []

    for val in range(len(worked_years)):
        data.append({
            'x': worked_years[val],
            'y': salary_brutto[val],
        })
    return JsonResponse(data, safe=False)