from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """Список товаров"""
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        # Показываем только опубликованные товары для всех, кроме персонала
        if self.request.user.is_staff:
            return Product.objects.all().order_by('-created_at')
        return Product.objects.filter(is_published=True).order_by('-created_at')


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр товара"""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        is_owner = product.owner == request.user
        is_staff = request.user.is_staff

        if not (is_owner or is_staff):
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        is_owner = product.owner == request.user
        is_moderator = request.user.has_perm('catalog.delete_product')

        if not (is_owner or is_moderator):
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, View):
    """Отмена публикации продукта модератором"""
    def post(self, request, pk):
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden("У вас нет прав для выполнения этого действия.")
        
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        
        return redirect('catalog:product_list')


class ProductPublishView(LoginRequiredMixin, View):
    """Публикация продукта модератором"""
    def post(self, request, pk):
        if not request.user.has_perm('catalog.can_publish_product'):
            return HttpResponseForbidden("У вас нет прав для выполнения этого действия.")
        
        product = get_object_or_404(Product, pk=pk)
        product.is_published = True
        product.save()
        
        return redirect('catalog:product_list')


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