from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic import View
from django.shortcuts import redirect
from .modules.linear_regression import LinearRegression

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

def calculate(request):
    reg = LinearRegression()
    data = Data.objects.all()
    
    x = [row.workedYears for row in data]
    y = [row.salaryBrutto for row in data]

    train_X = x[:47]
    train_y = y[:47]

    reg.fit(train_X, train_y)

    test_x = [row.workedYears for row in data[47:]]
    for i in Data.objects.all():
        if(i.salaryBrutto == None):
            i.salaryBrutto = reg.predict([i.workedYears])[0]
            i.save()

    return redirect('/data')

def reset(request):
    test_x = [row.workedYears for row in Data.objects.all()[47:]]
    id = 48
    for i in range(len(test_x)):
        q = Data.objects.get(pk=id)
        q.salaryBrutto = None
        q.save()
        id += 1

    return redirect('/data')
