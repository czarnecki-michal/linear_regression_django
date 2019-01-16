from django.db import models

class Data(models.Model):
    workedYears = models.FloatField()
    salaryBrutto = models.FloatField(null=True)
    test = models.IntegerField(null=True, default=0)

class ChartRange(models.Model):
    workedYears_min = models.IntegerField(null=True)
    workedYears_max = models.IntegerField(null=True)
    salaryBrutto_min = models.IntegerField(null=True)
    salaryBrutto_max = models.IntegerField(null=True)