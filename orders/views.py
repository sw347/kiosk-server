from django.shortcuts import render
from rest_framework import viewsets
from .models import Orders, OrderProduct, OrderStatus
from .serializers import OrderSerializer, OrderCreatSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreatSerializer
        return OrderSerializer