from rest_framework import serializers

from cart.models import Cart
from catalog.models import Category, Product, SubCategory

from constants import DECIMAL_MAX_DIGITS, DECIMAL_PLACES


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов."""

    category = serializers.CharField(
        source='subcategory.category.name',
        read_only=True
    )
    subcategory = serializers.CharField(
        source='subcategory.name',
        read_only=True
    )

    images = serializers.SerializerMethodField()

    def get_images(self, obj: Product):
        request = self.context.get('request')
        images = []

        if obj.image_small and hasattr(obj.image_small, 'url'):
            images.append(
                {
                    'size': 'small',
                    'url': request.build_absolute_uri(obj.image_small.url),
                }
            )
        if obj.image_medium and hasattr(obj.image_medium, 'url'):
            images.append(
                {
                    'size': 'medium',
                    'url': request.build_absolute_uri(obj.image_medium.url),
                }
            )
        if obj.image_big and hasattr(obj.image_big, 'url'):
            images.append(
                {
                    'size': 'big',
                    'url': request.build_absolute_uri(obj.image_big.url),
                }
            )
        return images

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'category',
            'subcategory',
            'price',
            'images',
        )


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories',)


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины."""

    class Meta:
        model = Cart
        fields = ('id', 'product', 'count')

    def update(self, instance, validated_data):
        """Запрет обновления самого продукта."""
        validated_data.pop('product', None)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return CartViewSerializer(instance).data


class CartViewSerializer(serializers.ModelSerializer):
    """Сериализатор для представления корзины пользователю."""

    product = ProductSerializer(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'product', 'count', 'total_price']
