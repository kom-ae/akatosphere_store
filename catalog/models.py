from django.db import models
from django.utils.text import slugify

from constants import MAX_LENGTH_NAME
from catalog.utils import generate_filename


class BaseCategory(models.Model):
    """Базовая модель для категории и подкатегории."""

    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME,
        unique=True)
    slug = models.SlugField(max_length=MAX_LENGTH_NAME, unique=True)
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=f'catalog/category/{generate_filename}'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
