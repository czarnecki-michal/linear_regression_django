from django import forms

class ChartForm(forms.Form):
    workedYears_min = forms.IntegerField(label="workedYears_min", max_value=50000, min_value=0, initial=0)
    workedYears_max = forms.IntegerField(label="workedYears_max", max_value=50000, min_value=0, initial=100)