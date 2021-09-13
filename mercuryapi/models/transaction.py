from django.db import models

class Transaction(models.Model):
    """Transaction Model"""

    date = models.DateField()
    employee = models.ForeignKey("employee", on_delete=models.CASCADE)
    product = models.ForeignKey("product", on_delete=models.CASCADE)
    priceSold = models.IntegerField()
    quantity = models.IntegerField()