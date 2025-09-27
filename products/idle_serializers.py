from rest_framework import serializers
from .models import Products
from core.models import Images
from core.serializers import CategorySerializer, ImageSerializer

class IdleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['filename']

class IdleProductSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = ['name', 'filename', 'price']
        
    def get_filename(self, obj):
        return obj.image.filename