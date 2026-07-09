from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path("sign-up/", views.RegisterView.as_view(), name="sign-up"),
    path("sign-in/", views.SignInView.as_view(), name="sign-in"),
    path("logout/", views.logoutUser, name="logout"),
]
