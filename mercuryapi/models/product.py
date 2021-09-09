from django.db import models

class Product(models.Model):
    """Product Model"""

    image = models.TextField()
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    priceSold = models.IntegerField()
    stock = models.IntegerField()
    department_Id = models.ForeignKey("DepartmentName", on_delete=models.CASCADE)