import random
from django.shortcuts import render
from users.models import User
from books.models import Book
from categories.models import Category


def menu(request):
    popularAuthor = User.getAuthors().order_by('-reviewsCount', '-rating')[:12]
    books = Book.getBooks()

    newBooks = books.order_by('-publication_date')[:12]
    popularBooks = books.order_by('-reviewsCount')[:12]

    categoriesToRandomise = [category for category in Category.objects.all() if category.book_set.count() > 0]
    return render(request, 'menu.html',
                  {'popularAuthor': popularAuthor, 'newBooks': newBooks, 'popularBooks': popularBooks,
                   'category': random.choice(categoriesToRandomise) if categoriesToRandomise else []})


def search(request):
    searchText = request.GET.get('search')
    books = Book.getBooks(name__icontains=searchText)
    authors = User.getAuthors(full_name__icontains=searchText)
    return render(request, 'search.html', {'books': books, 'authors': authors, 'searchText': searchText})
