from rest_framework import permissions
from rest_framework import viewsets

from catalog.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related(
        'subcategory',
        'subcategory__category'
    )
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_context(self):
        return {'request': self.request}


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
