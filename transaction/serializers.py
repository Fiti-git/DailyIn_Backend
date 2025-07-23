from rest_framework import serializers
from .models import Transaction
from product.models import Product
from emp.models import EmployeeProfile
from django.contrib.auth.models import User

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'product', 'employee', 'quantity', 'transaction_type', 'timestamp', 'remarks']

class TransactionCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    Itcode = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    transaction_type = serializers.ChoiceField(choices=['IN', 'OUT'], default='IN')
    remarks = serializers.CharField(required=False, allow_blank=True, max_length=500)


class TransactionDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'quantity', 'timestamp', 'remarks', 'product', 'employee']

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "Itcode": obj.product.Itcode,
            "ItDesc": obj.product.ItDesc,
        }

    def get_employee(self, obj):
        return {
            "id": obj.employee.id,
            "first_name": obj.employee.first_name,
            "last_name": obj.employee.last_name,
            "emp_code": obj.employee.emp_code,
        }
