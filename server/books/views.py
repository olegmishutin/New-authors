from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from .models import Book
from categories.models import Category


def books(request):
    return render(request, 'books/books.html', {'isAdmin': False})


def booksAdmin(request):
    if request.user.is_superuser:
        return render(request, 'books/books.html', {'isAdmin': True})
    return HttpResponse(status=403)


class BookPage(generic.DetailView):
    model = Book
    template_name = 'books/book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = kwargs.get('object')
        context['reviews'] = book.review_set.all()
        return context


def getBookInfo(request, anotherContent):
    bookName = ' '.join(request.POST.get('bookName').split())
    bookDescription = ' '.join(request.POST.get('bookDesciption').split())
    bookPagesNumber = request.POST.get('bookPagesNumber')

    errorRender = None
    haveCategory = False
    bookCategories = []

    for category in anotherContent.get('categories'):
        if request.POST.get(f'checkbox-{category.id}') == 'on':
            haveCategory = True
            bookCategories.append(category)

    info = {'bookCover': request.FILES.get('bookCover'), 'bookName': bookName, 'bookDescription': bookDescription,
            'bookPagesNumber': bookPagesNumber, 'bookFile': request.FILES.get('bookFile'),
            'bookCategories': bookCategories}

    if not bookName or not bookDescription or not bookCategories:
        content = {'bookNameValue': bookName, 'bookDescriptionValue': bookDescription,
                   'bookPagesNumberValue': bookPagesNumber}
        content.update(anotherContent)

        errorRender = render(request, 'books/book editing.html', content)
    return info, errorRender


def publicateBook(request):
    if request.user.is_author:
        categories = Category.objects.all()

        if request.method == 'POST':
            info, errorRender = getBookInfo(request, {'categories': categories, 'type': 'publicate'})

            if errorRender:
                return errorRender
            book = Book.objects.create(author=request.user, cover=info.get('bookCover'), name=info.get('bookName'),
                                       description=info.get('bookDescription'),
                                       pages_number=info.get('bookPagesNumber'), file=info.get('bookFile'))

            for bookCategory in info.get('bookCategories'):
                book.categories.add(bookCategory)

            return redirect('users:user-books', request.user.id)
        return render(request, 'books/book editing.html', {'categories': categories, 'type': 'publicate'})
    return HttpResponse(status=403)


def editBook(request, pk):
    if request.user.is_author:
        book = Book.objects.get(pk=pk)
        bookCategories = list(book.categories.all())
        categories = list(Category.objects.all())

        for bookCategory in bookCategories:
            categories.remove(bookCategory)

        if request.method == 'POST':
            info, errorRender = getBookInfo(request, {'bookId': book.id, 'bookCover': book.cover,
                                                      'categories': Category.objects.all(), 'type': 'edit'})
            if errorRender:
                return errorRender

            for bookCategory in bookCategories:
                if not request.POST.get(f'checkbox-{bookCategory.id}'):
                    bookCategory.book_set.remove(book)

            for category in categories:
                if request.POST.get(f'checkbox-{category.id}') == 'on':
                    category.book_set.add(book)

            book.changeCover(info.get('bookCover'))
            book.name = info.get('bookName')
            book.description = info.get('bookDescription')
            book.pages_number = info.get('bookPagesNumber')
            book.changeFile(info.get('bookFile'))
            book.save(update_fields=['cover', 'name', 'description', 'pages_number', 'file'])

            return redirect('users:user-books', request.user.id)
        return render(request, 'books/book editing.html',
                      {'bookId': book.id, 'bookCover': book.cover, 'bookNameValue': book.name,
                       'bookDescriptionValue': book.description, 'bookPagesNumberValue': book.pages_number,
                       'bookCategories': bookCategories, 'categories': categories, 'type': 'edit'})
    return HttpResponse(status=403)


class DeleteBook(generic.DeleteView):
    model = Book

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_author:
            self.success_url = reverse_lazy('users:user-books', kwargs={'pk': request.user.id})
            return super().post(request)
        return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=403)
