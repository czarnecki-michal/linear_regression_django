from django.db import models

class Data(models.Model):
    workedYears = models.FloatField()
    salaryBrutto = models.FloatField(null=True)
    test = models.IntegerField(null=True, default=0)