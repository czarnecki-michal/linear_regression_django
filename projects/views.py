import json
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.views.generic import View
from .modules.linear_regression import LinearRegression
from .forms import ChartForm
from pprint import pprint
import os

from .models import Data


def index(request):
    try:
        a = Data.objects.get(pk=1)
        return render(request, 'projects/index.html')
    except:
        error = "Błąd pobierania danych"
        return render(request, 'projects/index.html', {'error': error})

class ProjectView(View):
    template_name = 'projects/detail.html'
    train_data = Data.objects.filter(test=0)
    test_data = Data.objects.filter(test=1)

    def get_data(self):
        data = []
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
        train_data = Data.objects.filter(test=0)
        test_data = Data.objects.filter(test=1)
        try:
            data = self.get_data()
            return render(request, 'projects/detail.html', {'train_data': train_data, 'test_data': test_data, 'data': data, 'form': form})
        except:
            return redirect('index')

    def post(self, request, *args, **kwargs):
        form = ChartForm(request.POST)
        if form.is_valid():
            workedYears_min = form.cleaned_data['workedYears_min']
            workedYears_max = form.cleaned_data['workedYears_max']
        else:
            workedYears_min = 0
            workedYears_max = 100
        
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

def insert(request):
    import pandas as pd

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'static\\salary.csv')
    csv_file = pd.read_csv(file_path, sep=",")
    
    for i, row in csv_file.iterrows():
        test = 0
        if not pd.notnull(row['salaryBrutto']):
            test = 1

        data = Data(i, row['workedYears'], row['salaryBrutto'], test)

        try:
            data.save()
            message = "Pomyślnie zasilono bazę"
        except:
            message = "Wystąpił błąd przy importowaniu danych z wiersza: {}".format(i)

    return render(request, 'projects/index.html', {'message': message})
