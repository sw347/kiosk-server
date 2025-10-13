from rest_framework import serializers
from .models import Categorie, Image

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['category_id', 'name', 'description']

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['image_id', 'filename', 'description', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.filename)