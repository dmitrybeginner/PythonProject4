from django import template
from catalog.models import Category

register = template.Library()

@register.inclusion_tag('catalog/category_menu.html')
def category_menu():
    categories = Category.objects.all()
    return {'categories': categories}
