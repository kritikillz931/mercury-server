from django.db import models
from django.contrib.auth.models import User #pylint:disable=(imported-auth-user)

class Employee(models.Model):
    """Employee Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100 )
    dateHired = models.DateField()
    image = models.CharField(max_length=1000)
    department = models.ForeignKey("department", on_delete=models.CASCADE)
