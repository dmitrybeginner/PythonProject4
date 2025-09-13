from django.urls import path

from .views import RegisterView, EmailLoginView, SafeLogoutView


urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", SafeLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
