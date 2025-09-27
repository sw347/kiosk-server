from rest_framework import viewsets
from .models import Images
from .serializers import ImageSerializer

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer