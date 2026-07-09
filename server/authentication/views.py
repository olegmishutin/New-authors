from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.models import User
from .forms import UserModelForm


class RegisterView(CreateView):
    model = User
    form_class = UserModelForm
    template_name = "authentication/sign-up.html"
    success_url = reverse_lazy("menu")


class SignInView(LoginView):
    template_name = "authentication/sign-in.html"


@login_required()
def logoutUser(request):
    logout(request)
    return redirect("authentication:sign-in")
