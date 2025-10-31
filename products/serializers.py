from rest_framework import serializers
from .models import Product
from core.models import Image, Categorie
from core.serializers import CategorySerializer, ImageSerializer

class ProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()  

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'filename', 'price', 'kcal', 'available'] 
        
    def get_filename(self, obj):
        return obj.image.filename


class AllProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'filename', 'price', 'kcal', 'description', 'available']
        
    def get_filename(self, obj):
        return obj.image.filename
    
    def get_description(self, obj):
        return obj.image.description

   
class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Categorie
        fields = ['name', 'products']
        

class IdleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['filename']


class IdleProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['name', 'filename', 'price']
        
    def get_filename(self, obj):
        return obj.image.filename