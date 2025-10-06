from django.contrib import admin
from .models import Orders, OrderProduct, OrderStatus

admin.site.register(OrderStatus)
admin.site.register(OrderProduct)
admin.site.register(Orders)