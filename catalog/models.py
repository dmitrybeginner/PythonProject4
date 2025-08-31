from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=100,
        verbose_name='наименование',
        help_text='Введите название категории'
    )
    description = models.TextField(
        verbose_name='описание',
        help_text='Введите описание категории',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(
        max_length=100,
        verbose_name='наименование',
        help_text='Введите название товара'
    )
    description = models.TextField(
        verbose_name='описание',
        help_text='Введите описание товара',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='изображение',
        help_text='Загрузите изображение товара',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        help_text='Выберите категорию товара',
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена за покупку',
        help_text='Введите цену товара',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего изменения'
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.price} руб."