import os
from uuid import uuid4
from base64 import urlsafe_b64encode

from django.db import models
from django.utils.text import slugify

from constants import MAX_LENGTH_NAME



class BaseCategory(models.Model):
    """Базовая модель для категории и подкатегории."""
    folder_img = 'catalog/category/'

    def generate_filename(self, filename: str) -> str:
        """Генерирует уникальное имя файла."""
        ext = filename.split('.')[-1]
        name = urlsafe_b64encode(uuid4().bytes).decode().rstrip('=')
        return os.path.join(self.folder_img,)

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
