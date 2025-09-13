import logging
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, EmailAuthenticationForm

logger = logging.getLogger(__name__)


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email: str) -> None:
        subject = "Добро пожаловать"
        message = "Спасибо за регистрацию!"
        from_email = None  # DEFAULT_FROM_EMAIL
        try:
            send_mail(subject, message, from_email, [user_email], fail_silently=False)
        except Exception as e:
            # В учебном проекте игнорируем сбои отправки почты, чтобы не блокировать регистрацию
            logger.error(f"Не удалось отправить приветственное письмо на {user_email}: {e}")


class EmailLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("catalog:product_list")


class SafeLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:product_list")
