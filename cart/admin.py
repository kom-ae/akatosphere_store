from django.contrib import admin

from cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админка корзины."""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ('user', 'product', 'get_subcategory',
                    'count', 'create_at', 'modified_at')
    search_fields = ('user', 'product')
    list_filter = ('user', 'product')
    readonly_fields = (
        'user',
        'product',
        'get_subcategory',
        'count',
        'create_at',
        'modified_at',
    )

    @admin.display(description='Подкатегория')
    def get_subcategory(self, obj):
        return obj.product.subcategory
