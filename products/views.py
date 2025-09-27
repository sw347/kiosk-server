from rest_framework import viewsets
from .models import Products
from .idle_serializers import IdleProductSerializer
from .all_serializers import AllProductSerializer

class IdleProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.filter(category_id__in=[1, 2])
    serializer_class = IdleProductSerializer
    
class AllProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = AllProductSerializer

class ProductByCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AllProductSerializer

    def get_queryset(self):
        queryset = Products.objects.all().select_related('category', 'image')
        category = self.request.query_params.get('category')
        
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        
        return queryset