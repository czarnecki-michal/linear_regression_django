from django import forms

class ChartForm(forms.Form):
    workedYears_min = forms.IntegerField(label="worked years min", max_value=100, min_value=0, initial=0)
    workedYears_max = forms.IntegerField(label="worked years max", max_value=100, min_value=0, initial=100)

    def clean(self):
        cleaned_data = super().clean()
        workedYears_min = cleaned_data.get('workedYears_min')
        workedYears_max = cleaned_data.get('workedYears_max')
        if workedYears_max <= workedYears_min:
            msg = 'workedYears_max musi być większe od workedYears_min'
            self.add_error('workedYears_max', msg)