from django.contrib import admin
from django.urls import path, include
from orders.views import order_dashboard

urlpatterns = [
    path('admin/orders/dashboard/', order_dashboard, name='order_dashboard'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
]
