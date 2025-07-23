from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionDetailSerializer
from product.models import Product

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related('product', 'employee__user')
    serializer_class = TransactionDetailSerializer
