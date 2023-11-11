from django.shortcuts import render


def allBooks(request):
    return render(request, 'books/all books.html')
