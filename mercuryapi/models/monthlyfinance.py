from django.db import models
class MonthlyFinance(models.Model):
    """Monthly Finances"""
    month=models.CharField(max_length=100)
    year=models.CharField(max_length=100)
    cost=models.IntegerField()
    revenue=models.IntegerField()
    profit=models.IntegerField()