from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('all-books/', views.allBooks, name='all-books')
]