from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.views.generic import View
from django.shortcuts import redirect
from .modules.linear_regression import LinearRegression
from django.db.models import Q
from pprint import pprint

from .models import Data, ChartRange

def index(request):
    return render(request, 'projects/index.html')

def detail(request):
    try:
        train_data = Data.objects.all()[:47]
        test_data = Data.objects.all()[47:]
        return render(request, 'projects/detail.html', {'train_data': train_data, 'test_data': test_data})
    except:
        return render(request, 'projects/detail.html')

def get_data(request):
    pprint(globals())
    pprint(locals())
    if request.method == "POST":
        workedYears_min = request.POST['workedYears_min']
        workedYears_max = request.POST['workedYears_max']
        salaryBrutto_min = request.POST['salaryBrutto_min']
        salaryBrutto_max = request.POST['salaryBrutto_max']

        if ChartRange.objects.all() is None:
            q = ChartRange(
                workedYears_min=workedYears_min,
                workedYears_max=workedYears_max,
                salaryBrutto_min=salaryBrutto_min,
                salaryBrutto_max=salaryBrutto_max)
            q.save()
        else:
            q = ChartRange.objects.get(pk=1)
            q.workedYears_min, q.workedYears_max, q.salaryBrutto_min, q.salaryBrutto_max = workedYears_min, workedYears_max, salaryBrutto_min, salaryBrutto_max
            q.save()
        return redirect(detail)
    else:
        chart_range = ChartRange.objects.all().first()

        data_range = Data.objects.filter(
            workedYears__range=[chart_range.workedYears_min, chart_range.workedYears_max], salaryBrutto__range=[chart_range.salaryBrutto_min, chart_range.salaryBrutto_max]
            )
            
        worked_years = [data.workedYears for data in data_range]
        salary_brutto = [data.salaryBrutto for data in data_range]
        test = [data.test for data in data_range]

        data = []

        for val in range(len(worked_years)):
            data.append({
                'x': worked_years[val],
                'y': salary_brutto[val],
                'test': test[val],
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

    for i in Data.objects.all():
        if(i.salaryBrutto is None):
            i.salaryBrutto = reg.predict([i.workedYears])[0]
            i.save()

    return redirect('/detail#data')

def reset(request):
    test_x = [row.workedYears for row in Data.objects.all()[47:]]
    id = 48
    for i in range(len(test_x)):
        q = Data.objects.get(pk=id)
        q.salaryBrutto = None
        q.save()
        id += 1

    return redirect('/detail#data')
