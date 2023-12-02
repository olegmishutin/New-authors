from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('change-user-info/', views.changeUserInfo, name='change-user-info'),
    path('user-comments/', views.userComments, name='user-comments'),
    path('user-books/', views.userBooks, name='user-books'),
    path('users-admin/', views.usersAdmin, name='users-admin')
]
