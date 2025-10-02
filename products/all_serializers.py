from rest_framework import serializers
from .models import Products
from core.models import Images, Categories
from core.serializers import CategorySerializer, ImageSerializer

class ProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()  

    class Meta:
        model = Products
        fields = ['product_id', 'name', 'filename', 'price', 'kcal', 'available'] 
        
    def get_filename(self, obj):
        return obj.image.filename
    
class AllProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = ['name', 'filename', 'price', 'kcal']
        
    def get_filename(self, obj):
        return obj.image.filename
    
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Categories
        fields = ['name', 'products']