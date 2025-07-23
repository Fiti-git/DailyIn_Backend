from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from emp.models import EmployeeProfile
from product.models import Product
from transaction.models import Transaction
from transaction.serializers import TransactionCreateSerializer
from django.core.cache import cache
from django.db import transaction as db_transaction

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_transaction_from_user_and_product(request):
    serializer = TransactionCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    data = serializer.validated_data
    user_id = data['user_id']
    itcode = data['Itcode']
    quantity = data['quantity']
    transaction_type = data['transaction_type']
    remarks = data.get('remarks', '')

    try:
        employee = EmployeeProfile.objects.only('id').get(user__id=user_id)
    except EmployeeProfile.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

    cache_key = f"product_itcode_{itcode}"
    product = cache.get(cache_key)
    if not product:
        try:
            product = Product.objects.only('id').get(Itcode=itcode)
            cache.set(cache_key, product, timeout=300)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

    with db_transaction.atomic():
        txn = Transaction.objects.create(
            product=product,
            employee=employee,
            quantity=quantity,
            transaction_type=transaction_type,
            remarks=remarks
        )

    return Response({
        "emp_id": employee.id,
        "product_id": product.id,
        "transaction_id": txn.id,
        "message": "Transaction created successfully."
    }, status=201)
