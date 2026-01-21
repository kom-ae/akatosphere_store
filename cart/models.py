from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product
from utils import get_trim_line

User = get_user_model()


class Cart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
    )
    count = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )
    create_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        default_related_name = 'cart'
        ordering = ('user',)

    def __str__(self):
        return '{}: {}'.format(self.user, get_trim_line(self.product))
