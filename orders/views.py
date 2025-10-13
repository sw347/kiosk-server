from django.shortcuts import render
from rest_framework import viewsets
from .models import Order, OrderProduct, OrderStatus
from .serializers import OrderSerializer, OrderCreatSerializer
from django.utils import timezone
from django.db.models import Sum, Count

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreatSerializer
        return OrderSerializer

def order_dashboard(request):
    today = timezone.localtime().date()
    
    status_summary = Order.objects.values('order_status__description').annotate(
        count=Count('order_status')
    )

    seven_days_ago = today - timezone.timedelta(days=7)
    daily_sales = Order.objects.filter(
        datetime__date__gte=seven_days_ago
    ).extra(select={'day': 'date(datetime)'}).values('day').annotate(
        total_price=Sum('price')
    ).order_by('day')
    
    top_products = OrderProduct.objects.values('product__name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:5]

    context = {
        'status_summary': list(status_summary),
        'daily_sales_data': list(daily_sales),
        'top_products': list(top_products),
    }
    return render(request, 'admin/order_dashboard.html', context)