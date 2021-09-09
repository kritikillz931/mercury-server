from django.db import models

class EmployeeSchedule(models.Model):
    """Employee Schedule"""
    employeeId = models.ForeignKey("Employee_Id", on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    totalHours = models.IntegerField()