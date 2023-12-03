from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book
from categories.models import Category


def books(request):
    return render(request, 'books/books.html', {'isAdmin': False})


def booksAdmin(request):
    if request.user.is_superuser:
        return render(request, 'books/books.html', {'isAdmin': True})
    return HttpResponse(status=403)


def book(request):
    return render(request, 'books/book.html')


def bookPublication(request):
    if request.user.is_author:
        categories = Category.objects.all()

        if request.method == 'POST':
            haveCategory = False
            bookCategories = []

            bookCover = request.FILES.get('bookCover')
            bookName = ' '.join(request.POST.get('bookName').split())
            bookDescription = ' '.join(request.POST.get('bookDesciption').split())
            bookPagesNumber = request.POST.get('bookPagesNumber')
            bookFile = request.FILES.get('bookFile')

            if not bookName or not bookDescription:
                return render(request, 'books/book editing.html',
                              {'bookNameValue': bookName, 'bookDescriptionValue': bookDescription,
                               'bookPagesNumberValue': bookPagesNumber, 'categories': categories})

            for category in categories:
                if request.POST.get(f'checkbox-{category.id}') == 'on':
                    haveCategory = True
                    bookCategories.append(category)

            if haveCategory:
                book = Book.objects.create(author=request.user, cover=bookCover, name=bookName,
                                           description=bookDescription, pages_number=bookPagesNumber, file=bookFile)

                for bookCategory in bookCategories:
                    book.categories.add(bookCategory)
            return redirect('users:user-books')
        return render(request, 'books/book editing.html', {'categories': categories})
    return HttpResponse(status=403)
