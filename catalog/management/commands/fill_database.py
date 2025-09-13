from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными для каталога'

    def handle(self, *args, **options):
        # Очищаем существующие данные
        self.stdout.write("Очищаем базу данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        self.stdout.write("Создаем категории...")
        categories_data = [
            {'name': 'Электроника', 'description': 'Техника и гаджеты'},
            {'name': 'Книги', 'description': 'Художественная и учебная литература'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(
                self.style.SUCCESS(f'Создана категория: {category.name}')
            )

        # Создаем товары
        self.stdout.write("Создаем продукты...")
        products_data = [
            {'name': 'Смартфон Samsung', 'description': 'Мощный смартфон с хорошей камерой',
             'category': categories['Электроника'], 'price': Decimal('29999.99')},
            {'name': 'Ноутбук HP', 'description': 'Игровой ноутбук для работы и развлечений',
             'category': categories['Электроника'], 'price': Decimal('75999.50')},
            {'name': 'Python для начинающих', 'description': 'Лучшая книга для изучения Python',
             'category': categories['Книги'], 'price': Decimal('1500.00')},
            {'name': 'Футболка хлопковая', 'description': 'Удобная хлопковая футболка',
             'category': categories['Одежда'], 'price': Decimal('999.99')},
            {'name': 'Наушники Sony', 'description': 'Беспроводные наушники с шумоподавлением',
             'category': categories['Электроника'], 'price': Decimal('12999.00')},
        ]

        for prod_data in products_data:
            product = Product.objects.create(**prod_data)
            self.stdout.write(
                self.style.SUCCESS(f'Создан товар: {product.name} - {product.price} руб.')
            )

        # Итоговая статистика
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Статистика: {Category.objects.count()} категорий, {Product.objects.count()} продуктов')
        )
        self.stdout.write("="*50)