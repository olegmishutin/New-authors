from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('books/', views.books, name='books'),
    path('books-admin/', views.booksAdmin, name='books-admin'),
    path('book/<int:pk>/', views.BookPage.as_view(), name='book'),
    path('book/<int:pk>/reviews-filtered/', views.FilteredReviewsBookPage.as_view(), name='book-filtered-reviews'),
    path('book/<int:bookId>/add-review', views.addReview, name='add-review'),
    path('delete-review/<int:pk>/', views.DeleteReview.as_view(), name='delete-review'),
    path('book-publication/', views.publicateBook, name='book-publication'),
    path('book/<int:pk>/editing/', views.editBook, name='book-editing'),
    path('delete-book/<int:pk>/', views.DeleteBook.as_view(), name='delete-book')
]
