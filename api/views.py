from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (CartSerializer, CartViewSerializer,
                             CategorySerializer, ProductSerializer)
from cart.models import Cart
from catalog.models import Category, Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для продуктов."""

    queryset = Product.objects.select_related(
        'subcategory',
        'subcategory__category'
    )
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_context(self):
        return {'request': self.request}


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для категорий."""

    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class CartViewSet(viewsets.ModelViewSet):
    """Представление для корзины."""

    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'view':
            return CartViewSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Добавить товар в корзину."""
        product_id = request.data.get('product')
        count = request.data.get('count', 1)

        if not product_id:
            return Response(
                {'detail': 'product не указан'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product = get_object_or_404(Product, pk=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=self.request.user,
            product=product,
            defaults={'count': count}
        )
        if not created:
            cart_item.count += count
            cart_item.save()
        serializer = self.get_serializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['put'],
        url_path=r'update-count/(?P<product_id>\d+)'
    )
    def update_count(self, request, product_id):
        """Изменить количество товара в корзине."""
        count = request.data.get('count')

        if count is None or count <= 0:
            return Response(
                {'detail': 'count должно быть больше 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = get_object_or_404(self.get_queryset(), product=product_id)

        cart_item.count = count
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['delete'],
        url_path=r'remove/(?P<product_id>\d+)'
    )
    def remove(self, request, product_id):
        """Удалить продукт из корзины."""
        product = get_object_or_404(self.get_queryset(), product=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """Очистить корзину."""
        self.get_queryset().all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='view')
    def view(self, request):
        queryset = self.get_queryset().select_related('product').annotate(
            total_price=F('product__price') * F('count')
        )
        serializer = self.get_serializer(queryset, many=True)

        totals = queryset.aggregate(
            total_quantity=Sum('count'),
            total_amount=Sum('total_price')
        )
        response_data = {
            'cart': serializer.data,
            'total_in_cart': {
                'total_quantity': totals['total_quantity'] or 0,
                'total_amount': totals['total_amount'] or 0.00
            }
        }

        return Response(response_data)
