from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import CustomTokenObtainPairView, logout_view
from rest_framework_simplejwt.views import TokenRefreshView
from product import views


schema_view = get_schema_view(
    openapi.Info(
        title="Daily Inventory API",
        default_version='v1',
        description="API documentation for Daily Inventory Management System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # optional override
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... your app urls ...
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # ... authentication URLs
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', logout_view, name='logout'),
    # ... include your app URLs
   # path('api/', include('product.urls')),  # For products and stock
    path('api/product/', include('product.urls')),  # For employee profiles
    path('api/transaction/', include('transaction.urls')),  # For transactions
    path('api/emp/', include('emp.urls')),   # For employee profiles
    path('', views.product_dashboard, name='product_dashboard'),
    path('api/health/', views.health_data, name='health_data'),
    
]
