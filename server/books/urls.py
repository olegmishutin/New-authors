from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('books/', views.books, name='books'),
    path('books-admin/', views.booksAdmin, name='books-admin'),
    path('book/', views.book, name='book'),
    path('book-publication/', views.bookPublication, name='book-publication')
]