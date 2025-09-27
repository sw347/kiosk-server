from django.db import models

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return self.name
    
class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=150, blank=True)
    
    class Meta:
        db_table = 'images'
        
    def __str__(self):
        return self.filename