from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(LoginRequiredMixin, ListView):
    """Список блоговых записей - только опубликованные"""
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Фильтрация: выводим только статьи с положительным признаком публикации"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр блоговой записи с увеличением счетчика просмотров"""
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при открытии статьи"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Создание новой блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование блоговой записи с перенаправлением на просмотр статьи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        """Перенаправляем на просмотр отредактированной статьи"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')