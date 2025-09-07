from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """Список товаров"""
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')


class ProductDetailView(DetailView):
    """Детальный просмотр товара"""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    """Удаление товара"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')


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
