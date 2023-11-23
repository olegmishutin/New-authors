from django.shortcuts import render


def books(request):
    return render(request, 'books/books.html', {'isAdmin': False})


def booksAdmin(request):
    return render(request, 'books/books.html', {'isAdmin': True})


def book(request):
    return render(request, 'books/book.html')


def bookPublication(request):
    return render(request, 'books/book publication.html')
