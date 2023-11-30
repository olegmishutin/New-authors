from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('change-profile-info/', views.changeProfileInfo, name='change-profile-info'),
    path('profile-comments/', views.profileComments, name='profile-comments'),
    path('profile-books/', views.profileBooks, name='profile-books'),
    path('users-admin/', views.usersAdmin, name='users-admin')
]