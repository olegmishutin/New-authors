from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('authors/', views.Authors.as_view(), name='authors'),
    path('authors-admin/', views.AuthorsAdmin.as_view(), name='authors-admin')
]
