from django.db import models

class Department(models.Model):
    """Department Model"""
    name = models.CharField(max_length=100)