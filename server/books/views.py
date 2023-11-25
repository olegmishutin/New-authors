from django.shortcuts import render
from django.http import HttpResponse


def books(request):
    return render(request, 'books/books.html', {'isAdmin': False})


def booksAdmin(request):
    if request.user.is_superuser:
        return render(request, 'books/books.html', {'isAdmin': True})
    return HttpResponse(status=403)


def book(request):
    return render(request, 'books/book.html')


def bookPublication(request):
    return render(request, 'books/book publication.html')
