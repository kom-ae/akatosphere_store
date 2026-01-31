from http import HTTPStatus

from django.db.models import F, Sum
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.schemas import (
    clear_cart,
    create_cart_product,
    delete_product_in_cart,
    retrieve_category,
    retrieve_product,
    update_count_cart_product,
    view_cart,
    view_categories,
    view_products,
)
from api.serializers import (
    CartSerializer,
    CartUpdateSerializer,
    CategorySerializer,
    ProductSerializer,
)
from cart.models import Cart
from catalog.models import Category, Product


@extend_schema_view(
    list=view_products,
    retrieve=retrieve_product,
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для продуктов."""

    queryset = Product.objects.select_related(
        'subcategory',
        'subcategory__category',
    )
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema_view(
    list=view_categories,
    retrieve=retrieve_category,
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для категорий."""

    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema_view(
    create=create_cart_product,
    update=update_count_cart_product,
    destroy=delete_product_in_cart,
    clear=clear_cart,
    view=view_cart,
)
class CartViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet,
):
    """Представление для корзины."""

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'product'
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = Cart.objects.filter(
            user=self.request.user).select_related('product')
        if self.action == 'view':
            return queryset.annotate(
                total_price=F('product__price') * F('count'))
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'update':
            return CartUpdateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='view')
    def view(self, request):
        """Представление содержимого корзины с общими итогами."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        totals = queryset.aggregate(
            total_quantity=Sum('count'),
            total_amount=Sum('total_price'),
        )
        return Response(
            {
                'cart': serializer.data,
                'total_in_cart': {
                    'total_quantity': totals['total_quantity'] or 0,
                    'total_amount': totals['total_amount'] or 0.00,
                },
            },
        )

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        product_cart = self.get_queryset().filter(
            product=product,
        ).first()

        if product_cart:
            data['count'] = data.get('count', 1) + product_cart.count
            serializer = self.get_serializer(product_cart, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=HTTPStatus.OK,
            )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """Очистить корзину."""
        self.get_queryset().all().delete()
        return Response(status=HTTPStatus.NO_CONTENT)
