from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeProfileViewSet, OutletViewSet, EmployeeProfileReadOnlyViewSet
from .new_views import create_transaction_from_user_and_product

router = DefaultRouter()
router.register(r'employee-profiles_api', EmployeeProfileViewSet, basename='employeeprofile')
router.register(r'outlets_api', OutletViewSet, basename='outlet' )
router.register(r'employee-readonly', EmployeeProfileReadOnlyViewSet, basename='employee-readonly')

urlpatterns = [
    path('', include(router.urls)),
    
    path('api/daily-transaction/', create_transaction_from_user_and_product),

   
]
