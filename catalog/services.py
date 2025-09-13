from catalog.models import Product, Category


def get_products_by_category(category_id: int):
    """Возвращает все продукты для данной категории."""
    return Product.objects.filter(category_id=category_id)
