from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Order, OrderProduct, OrderStatus
from .serializers import OrderSerializer, OrderCreatSerializer
from django.utils import timezone
from django.db.models import Sum, Count, Case, When, Value, IntegerField
from django.db import transaction
from django.urls import reverse

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreatSerializer
        return OrderSerializer

def order_dashboard(request):
    today = timezone.localtime().date()
    seven_days_ago = today - timezone.timedelta(days=7)
    
    status_summary = Order.objects.values('order_status__description').annotate(
        count=Count('order_status')
    )

    top_products = OrderProduct.objects.values('product__name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:5]

    daily_sales = Order.objects.filter(
        datetime__date__gte=seven_days_ago
    ).extra(select={'day': 'date(datetime)'}).values('day').annotate(
        total_price=Sum('price')
    ).order_by('day')
    
    context = {
        'status_summary': list(status_summary),
        'daily_sales_data': list(daily_sales),
        'top_products': list(top_products),
    }
    return render(request, 'admin/order_dashboard.html', context)

def order_status_management(request):
    if request.method == 'POST':
        with transaction.atomic():
            for key, new_status_id in request.POST.items():
                if key.startswith('status_'):
                    order_id = key.split('_')[1]
                    try:
                        Order.objects.filter(pk=order_id).update(order_status_id=new_status_id)
                    except Exception:
                        continue 

        return redirect(reverse('admin:orders_status_manager'))

    statuses_to_show = ['Started', 'Placed and paid', 'Preparing', 'Ready for pickup', 'Picked up']
    
    sorting_order = Case(
        When(order_status__description='Picked up', then=Value(2)),
        default=Value(1),
        output_field=IntegerField()
    )
    
    orders_to_process = Order.objects.filter(
        order_status__description__in=statuses_to_show
    ).select_related('order_status').prefetch_related('orderproduct_set__product').annotate(
        status_order=sorting_order
    ).order_by('status_order', 'datetime') 
    
    context = {
        'orders_to_process': orders_to_process,
        'all_statuses': OrderStatus.objects.all(),
        'has_permission': True,
    }
    
    return render(request, 'admin/order_status_manager.html', context)
