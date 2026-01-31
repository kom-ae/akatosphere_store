from django.contrib import admin

from catalog.models import Category, Product, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий каталога."""

    list_display = ('name', 'slug', 'image', 'create_at', 'modified_at')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Админка категорий каталога."""

    list_display = (
        'name',
        'category',
        'slug',
        'image',
        'create_at',
        'modified_at',
    )
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка продуктов."""

    list_display = (
        'name',
        'subcategory',
        'price',
        'image',
        'slug',
        'create_at',
        'modified_at',
    )
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)


admin.site.empty_value_display = '-пусто-'
