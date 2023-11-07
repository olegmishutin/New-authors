from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('sign-up/', views.signUp, name='sign-up'),
    path('sign-in/', views.signIn, name='sign-in'),
]
