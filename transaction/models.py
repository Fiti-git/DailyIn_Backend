from django.db import models
from product.models import Product
from emp.models import EmployeeProfile

TRANSACTION_TYPE_CHOICES = [
    ('IN', 'Stock In'),
    ('OUT', 'Stock Out'),
    ('ADJ', 'Adjustment'),
]

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES, default='IN')
    

    def __str__(self):
        return f"{self.transaction_type} - {self.product.Itcode} ({self.quantity}) by {self.employee.user.username} on {self.timestamp.strftime('%Y-%m-%d')}"
