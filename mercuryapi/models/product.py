from django.db import models

class Product(models.Model):
    """Product Model"""

    image = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    priceSold = models.IntegerField()
    stock = models.IntegerField()
    department = models.ForeignKey("department", on_delete=models.CASCADE)