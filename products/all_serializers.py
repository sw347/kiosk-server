from rest_framework import serializers
from .models import Products
from core.models import Images
from core.serializers import CategorySerializer, ImageSerializer

class AllImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['filename']

class AllProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = ['name', 'filename', 'price', 'kcal']
        
    def get_filename(self, obj):
        return obj.image.filename