from rest_framework import viewsets
from rest_framework.response import Response
from .models import Products, Categories
from .idle_serializers import IdleProductSerializer
from .all_serializers import AllProductSerializer, CategoryProductSerializer

class IdleProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.filter(category_id__in=[1, 2])
    serializer_class = IdleProductSerializer
    
class AllProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoryProductSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().prefetch_related('products')
        
        serializer = self.get_serializer(queryset, many=True)
        raw_data = serializer.data
        
        final_list = []
        for category_data in raw_data:
            category_name = category_data['name'].lower()
            product_list = category_data['products']
            
            products_dict = [
                product for product in product_list
            ]
            
            final_list.append({
                "name": category_name,
                "data": products_dict
            })
            
        return Response(final_list)

class ProductByCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AllProductSerializer

    def get_queryset(self):
        queryset = Products.objects.all().select_related('category', 'image')
        category = self.request.query_params.get('category')
        
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        
        return queryset