from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Product


class ProductListView(ListView):
    """Контроллер для отображения списка товаров"""
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Главная'
        return context


class ProductDetailView(DetailView):
    """Контроллер для отображения детальной информации о товаре"""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - Детальная информация'
        return context


class ContactsView(View):
    """Контроллер для страницы контактов с обработкой формы"""
    template_name = 'contacts.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получено сообщение от {name} ({phone}): {message}")

        # После обработки формы снова показываем страницу контактов
        return render(request, self.template_name)