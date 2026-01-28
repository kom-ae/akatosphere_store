from http import HTTPStatus

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
    # lookup_field = 'product'

    def get_queryset(self):
        return Cart.objects.filter(
            user=self.request.user
        ).select_related('product')

    def get_serializer_class(self):
        if self.action == 'view':
            return CartViewSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Добавить товар в корзину."""

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTPStatus.BAD_REQUEST
            )
        product_id = serializer.validated_data['product']
        count = serializer.validated_data['count']

        product_cart = self.get_queryset().filter(product=product_id).first()
        if product_cart:
            product_cart.count += count
            product_cart.save()
        else:
            product_cart = serializer.save(user=request.user)

        serializer = self.get_serializer(product_cart)

        return Response(serializer.data, status=HTTPStatus.CREATED)

    @action(
        detail=False,
        methods=['put'],
        url_path=r'update-count/(?P<product_id>\d+)'
    )
    def update_count(self, request, product_id):
        """Изменить количество товара в корзине."""
        product_cart = get_object_or_404(
            self.get_queryset(),
            product=product_id
        )

        serializer = self.get_serializer(
            product_cart,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
