from rest_framework import serializers

from catalog.models import Product, Category, SubCategory


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
        fields = ['name', 'slug', 'category', 'subcategory', 'price', 'images']


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий."""

    class Meta:
        model = SubCategory
        fields = ['name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'image', 'subcategories']
