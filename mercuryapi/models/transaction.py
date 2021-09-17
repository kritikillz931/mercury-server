from django.db import models

class Transaction(models.Model):
    """Transaction Model"""

    month = models.CharField(max_length=255)
    day = models.IntegerField()
    year = models.IntegerField()
    employee = models.ForeignKey("employee", on_delete=models.CASCADE)
    product = models.ForeignKey("product", on_delete=models.CASCADE)
    quantitySold = models.IntegerField()