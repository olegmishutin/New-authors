from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('change-user-info/', views.changeUserInfo, name='change-user-info'),
    path('user/<int:pk>/reviews/', views.UserReviews.as_view(), name='user-comments'),
    path('user/<int:pk>/books/', views.UserBooks.as_view(), name='user-books'),
    path('users-admin/', views.usersAdmin, name='users-admin')
]
