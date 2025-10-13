from django.contrib import admin
from .models import Order, OrderProduct, OrderStatus
from django.urls import path
from .views import order_dashboard, order_status_management

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    fields = ('product', 'quantity', 'price') 
    readonly_fields = ('price',)

@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'order_id', 
        'pickup_number', 
        'order_status', 
        'price', 
        'datetime', 
        'display_total_items'
    )
    
    list_editable = (
        'order_status',
    )
    
    fields = (
        'order_id',
        'pickup_number',
        'price',
        'order_status',
    )
    
    readonly_fields = ('order_id', 'pickup_number', 'price', 'datetime')
    
    search_fields = ('order_id', 'pickup_number')
    list_filter = ('order_status', 'datetime')
    inlines = [OrderProductInline]
    
    def display_total_items(self, obj):
        return obj.orderproduct_set.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    display_total_items.short_description = 'Total Items'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', admin.site.admin_view(order_dashboard), name='order_dashboard'),
            path('status-manager/', self.admin_site.admin_view(order_status_management), name='orders_status_manager'),
        ]
        return custom_urls + urls
    
admin.site.register(OrderStatus)
admin.site.register(OrderProduct)