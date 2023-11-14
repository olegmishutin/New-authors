from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('profile-comments/', views.profileComments, name='profile-comments'),
    path('profile-books/', views.profileBooks, name='profile-books'),
]