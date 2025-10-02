from django.db import models
from products.models import Products

class OrderStatus(models.Model):
    order_status_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order_status'
        verbose_name_plural = "Order Statuses"
        
    def __str__(self):
        return self.description

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, db_column='order_status_id')
    pickup_number = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-datetime']
        
    def __str__(self):
        return f"Order #{self.order_id} (Status: {self.order_status.description})"

class OrderProduct(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='order_id')
    product = models.ForeignKey(Products, on_delete=models.PROTECT, db_column='product_id')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        db_table = 'order_product'
        
    def __str__(self):
        return f"Order #{self.order.order_id} - Product: {self.product.name}"