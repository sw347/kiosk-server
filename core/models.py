from django.db import models

class Categorie(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'categorie'
        
    def __str__(self):
        return self.name
    
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'image'
        
    def __str__(self):
        return self.filename