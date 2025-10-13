from django.db import models
from core.models import Categorie, Image

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='products')
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    kcal = models.IntegerField()
    available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'product'
        
    def __str__(self):
        return self.name