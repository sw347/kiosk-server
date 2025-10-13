from django.db import models, transaction
from django.db.models import F
from django.utils import timezone
from products.models import Product

class OrderStatus(models.Model):
    order_status_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'order_status'
        verbose_name_plural = "Order Statuses"
        
    def __str__(self):
        return self.description

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, db_column='order_status_id', default=1)
    pickup_number = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    datetime = models.DateTimeField(auto_now_add=False, default=timezone.now)
    
    class Meta:
        db_table = 'order'
        ordering = ['-datetime']
        
    def __str__(self):
        return f"Order #{self.order_id} (Status: {self.order_status.description})"
    
    def assign_pickup_number(self):
        today = timezone.now().date()
        
        with transaction.atomic():
            sequence = PickupSequence.load()
            
            if sequence.last_assigned_date < today:
                sequence.current_number = 0
                sequence.last_assigned_date = today
            
            next_number = sequence.current_number + 1
            
            if next_number > 99:
                new_number = 1
            else:
                new_number = next_number
            
            self.pickup_number = new_number
            sequence.current_number = new_number
            sequence.save()
    
    def save(self, *args, **kwargs):
        if self.pickup_number is None:
            self.assign_pickup_number()

        super().save(*args, **kwargs)

class PickupSequence(models.Model):
    current_number = models.IntegerField(default=0)
    last_assigned_date = models.DateField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, defaults={'current_number': 0})
        return obj

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, db_column='product_id')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'order_product'
        
    def __str__(self):
        return f"Order #{self.order.order_id} - Product: {self.product.name}"