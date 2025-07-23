from django.db import models

class Product(models.Model):
    Itcode = models.CharField(max_length=50, unique=True)
    ItDesc = models.CharField(max_length=255)
    RackNo = models.CharField(max_length=50)
    barcode = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Itcode} - {self.ItDesc}"


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    outlet = models.ForeignKey('emp.Outlet', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'outlet')

    def __str__(self):
        return f"{self.product} @ {self.outlet}: {self.quantity}"
