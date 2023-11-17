from django.shortcuts import render


def books(request):
    return render(request, 'books/books.html')


def book(request):
    return render(request, 'books/book.html')


def bookPublication(request):
    return render(request, 'books/book publication.html')
