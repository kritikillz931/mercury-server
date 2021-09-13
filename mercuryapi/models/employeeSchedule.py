from django.db import models

class EmployeeSchedule(models.Model):
    """Employee Schedule"""
    employee = models.ForeignKey("employee", on_delete=models.CASCADE)
    date = models.DateField()
    startTime = models.IntegerField()
    endTime = models.IntegerField()
    totalHours = models.IntegerField()