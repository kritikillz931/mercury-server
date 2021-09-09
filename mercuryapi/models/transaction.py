from django.db import models

class Transaction(models.model):
    """Transaction Model"""

    date = models.DateField()
    employee_Id = models.ForeignKey("Employee", on_delete=models.CASCADE)
    product_Id = models.ForeignKey("Product", on_delete=models.CASCADE)
    priceSold = models.IntegerField()
    quantity = models.IntegerField()