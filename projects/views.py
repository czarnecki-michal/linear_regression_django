import json
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.views.generic import View
from .modules.linear_regression import LinearRegression
from .forms import ChartForm
from pprint import pprint

from .models import Data


def index(request):
    
    return render(request, 'projects/index.html')


class ProjectView(View):
    template_name = 'projects/detail.html'
    train_data = Data.objects.filter(test=0)
    test_data = Data.objects.filter(test=1)

    def get_data(self):
        data = []
        train_data = Data.objects.filter(test=0)
        test_data = Data.objects.filter(test=1)
        for val in self.train_data:
            data.append({
                'x': val.workedYears,
                'y': val.salaryBrutto,
                'test': val.test,
            })
        for val in self.test_data:
            data.append({
                'x': val.workedYears,
                'y': val.salaryBrutto,
                'test': val.test,
            })
        data = json.dumps(data)
        return data

    def get(self, request, *args, **kwargs):
        form = ChartForm()
        data = self.get_data()
        try:
            return render(request, 'projects/detail.html', {'train_data': self.train_data, 'test_data': self.test_data, 'data': data, 'form': form})
        except:
            return render(request, 'projects/detail.html')

    def post(self, request, *args, **kwargs):
        form = ChartForm(request.POST)
        if form.is_valid():
            workedYears_min = form.cleaned_data['workedYears_min']
            workedYears_max = form.cleaned_data['workedYears_max']
        
        self.train_data = Data.objects.filter(
            test=0,
            workedYears__range=[workedYears_min, workedYears_max]
            )
        self.test_data = Data.objects.filter(
            test=1,
            workedYears__range=[workedYears_min, workedYears_max]
            )
        data = self.get_data()
        args = {'form': form, 'train_data': self.train_data, 'test_data': self.test_data, 'data': data}

        return render(request, self.template_name, args)

def calculate(request):
    reg = LinearRegression()
    data = Data.objects.all()

    x = [row.workedYears for row in data]
    y = [row.salaryBrutto for row in data]

    train_X = x[:47]
    train_y = y[:47]

    reg.fit(train_X, train_y)

    for i in Data.objects.all():
        if i.salaryBrutto is None:
            i.salaryBrutto = reg.predict([i.workedYears])[0]
            i.save()

    return redirect('detail')


def reset(request):
    for i in Data.objects.all():
        if i.test == 1:
            i.salaryBrutto = None
            i.save()
    return redirect('detail')
