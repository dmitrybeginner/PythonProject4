from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'title': 'Skystore - Главная'
    }
    return render(request, "home.html", context)


def contacts(request):
    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получено сообщение от {name} ({phone}): {message}")

    return render(request, 'contacts.html')


def product_detail(request, pk):
    """Контроллер для отображения детальной информации о товаре"""
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
        'title': f'{product.name} - Детальная информация'
    }

    return render(request, 'catalog/product_detail.html', context)