from django.db import models
from django.contrib.auth.models import User #pylint:disable=(imported-auth-user)

class Employee(models.Model):
    """Employee Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100 )
    dateHired = models.DateField()
    monthlySales = models.IntegerField()
    department = models.ForeignKey("department", on_delete=models.CASCADE)
