from http import HTTPStatus

from django.db.models import F, Sum
from rest_framework import mixins
from rest_framework import permissions, viewsets
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


class CartViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Представление для корзины."""

    serializer_class = CartSerializer
    lookup_field = 'product'

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user).select_related(
            'product'
        )
        if self.action == 'view':
            return queryset.annotate(total_price=F('product__price')
                                     * F('count')
                                     )
        return queryset

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

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """Очистить корзину."""
        self.get_queryset().all().delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='view')
    def view(self, request):
        """Представление содержимого корзины с общими итогами."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        totals = queryset.aggregate(
            total_quantity=Sum('count'),
            total_amount=Sum('total_price')
        )
        return Response(
            {
                'cart': serializer.data,
                'total_in_cart': {
                    'total_quantity': totals['total_quantity'] or 0,
                    'total_amount': totals['total_amount'] or 0.00
                }
            }
        )
