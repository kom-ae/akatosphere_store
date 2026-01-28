import os
from base64 import urlsafe_b64encode
from uuid import uuid4

from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from unidecode import unidecode

from constants import (DECIMAL_MAX_DIGITS, DECIMAL_PLACES, IMAGEKIT_FORMAT,
                       IMAGEKIT_OPTIONS, MAX_LENGTH_NAME, SIZE_BIG_IMAGE,
                       SIZE_MEDIUM_IMAGE, SIZE_SMALL_IMAGE)
from utils import get_trim_line


class CategoryProductsAbstractModel(models.Model):
    """Абстрактная модель для категорий, подкатегорий и продуктов."""

    folder_img = os.path.join('catalog', 'categories')

    def generate_filename(self, filename: str) -> str:
        """Генерирует уникальное имя файла."""
        ext = filename.split('.')[-1]
        name = urlsafe_b64encode(uuid4().bytes).decode().rstrip('=')
        filename = f'{name}.{ext}'
        return os.path.join(self.folder_img, filename)

    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=generate_filename,
        blank=True,
        null=True,
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
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return get_trim_line(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class Category(CategoryProductsAbstractModel):
    """Модель категории."""

    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME,
        unique=True,
        db_index=True,
    )

    class Meta(CategoryProductsAbstractModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(CategoryProductsAbstractModel):
    """Модель подкатегории."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    class Meta(CategoryProductsAbstractModel.Meta):
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        default_related_name = 'subcategories'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'category'),
                name='Unique category-subcategory constraint'
            ),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '{}_{}'.format(
                self.category.slug,
                slugify(unidecode(self.name))
            )
        super().save(*args, **kwargs)


class Product(CategoryProductsAbstractModel):
    """Модель продукта."""

    folder_img = os.path.join('catalog', 'products')

    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name='Подкатегория',
        on_delete=models.CASCADE,
    )
    image_small = ImageSpecField(
        processors=[ResizeToFit(*SIZE_SMALL_IMAGE),],
        source='image',
        format=IMAGEKIT_FORMAT,
        options=IMAGEKIT_OPTIONS,
    )
    image_medium = ImageSpecField(
        processors=[ResizeToFit(*SIZE_MEDIUM_IMAGE),],
        source='image',
        format=IMAGEKIT_FORMAT,
        options=IMAGEKIT_OPTIONS,
    )
    image_big = ImageSpecField(
        processors=[ResizeToFit(*SIZE_BIG_IMAGE),],
        source='image',
        format=IMAGEKIT_FORMAT,
        options=IMAGEKIT_OPTIONS,
    )

    class Meta(CategoryProductsAbstractModel.Meta):
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        default_related_name = 'products'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'subcategory'),
                name='Unique product-category constraint'
            ),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '{}_{}'.format(
                self.subcategory.slug,
                slugify(unidecode(self.name))
            )
        super().save(*args, **kwargs)
