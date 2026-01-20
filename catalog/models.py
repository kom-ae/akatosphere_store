import os
from base64 import urlsafe_b64encode
from uuid import uuid4

from unidecode import unidecode
from django.db import models
from django.utils.text import slugify

from constants import MAX_LENGTH_NAME


class CategoryAbstractModel(models.Model):
    """Абстрактная модель для категории и подкатегории."""

    folder_img = 'catalog/category'

    def generate_filename(self, filename: str) -> str:
        """Генерирует уникальное имя файла."""
        ext = filename.split('.')[-1]
        name = urlsafe_b64encode(uuid4().bytes).decode().rstrip('=')
        filename = f'{name}.{ext}'
        return os.path.join(self.folder_img, filename)

    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME,
        unique=True,
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
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class Category(CategoryAbstractModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(CategoryAbstractModel):
    """Модель подкатегории."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        default_related_name = 'subcategories'
