from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class QuestionLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"


class QuestionLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")