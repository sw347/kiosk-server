from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IdleProductViewSet, AllProductViewSet, ProductByCategoryViewSet

router = DefaultRouter()
router.register(r'products-idle', IdleProductViewSet, basename='idle-products') 
router.register(r'products-all', AllProductViewSet, basename='all-products') 
router.register(r'products-category', ProductByCategoryViewSet, basename='category-products')

urlpatterns = [
    path('', include(router.urls)),
]