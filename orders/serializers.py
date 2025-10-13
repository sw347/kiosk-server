from rest_framework import serializers
from django.db import transaction
from django.db.models import Sum
from .models import Order, OrderProduct, OrderStatus
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderProductCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)
    
    class Meta:
        model = OrderProduct
        fields = ['product_id', 'quantity']
        
    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        
        product_id = validated_data.get('product_id')
        
        try:
            product = Product.objects.get(pk=product_id)
        except Products.DoesNotExist:
            raise serializers.ValidationError("Product with ID {value} does not exist.")
        
        validated_data['product_instance'] = product
        
        return validated_data
    
class OrderCreatSerializer(serializers.ModelSerializer):
    items = OrderProductCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['order_status', "items", "order_id", "pickup_number", "price", "datetime"]
        read_only_fields = ['order_id', 'pickup_number', 'price', 'datetime']
        
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        order_products = []
        
        for item_data in items_data:
            product = item_data['product_instance']
            quantity = item_data['quantity']
            
            unit_price = product.price 
            
            item_total_price = unit_price * quantity
            total_price += item_total_price
            
            order_product = OrderProduct(
                order=order,
                product=product,
                price=unit_price,
                quantity=quantity
            )
            
            order_products.append(order_product)
        
        OrderProduct.objects.bulk_create(order_products)
        
        order.price = total_price
        order.save(update_fields=['price'])
        
        return order