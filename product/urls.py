from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProductViewSet, StockViewSet


router = DefaultRouter()
router.register(r'products_api', ProductViewSet)
router.register(r'stocks_api', StockViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('', views.product_dashboard, name='product_dashboard'),

]
