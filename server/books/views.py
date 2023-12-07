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
    book = Book(author=request.user, cover=request.FILES.get('bookCover'),
                name=' '.join(request.POST.get('bookName').split()),
                description=' '.join(request.POST.get('bookDesciption').split()),
                pages_number=request.POST.get('bookPagesNumber'), file=request.FILES.get('bookFile'))

    errorRender = None
    bookCategories = []

    for category in Category.objects.all():
        if request.POST.get(f'checkbox-{category.id}') == 'on':
            bookCategories.append(category)

    if not book.name or not book.description or not bookCategories:
        oldBook = anotherContent.get('oldBook')
        if oldBook:
            book.id = oldBook.id
            book.cover = oldBook.cover

        content = {'book': book}
        content.update(anotherContent)
        errorRender = render(request, 'books/book editing.html', content)
    return {'book': book, 'bookCategories': bookCategories}, errorRender


def publicateBook(request):
    if request.user.is_author:
        categories = Category.objects.all()

        if request.method == 'POST':
            info, errorRender = getBookInfo(request, {'categories': categories, 'type': 'publicate'})
            if errorRender:
                return errorRender

            book = info.get('book')
            book.save()

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
            info, errorRender = getBookInfo(request, {'oldBook': book, 'categories': categories, 'type': 'edit'})
            if errorRender:
                return errorRender

            for bookCategory in bookCategories:
                if not request.POST.get(f'checkbox-{bookCategory.id}'):
                    bookCategory.book_set.remove(book)

            for category in categories:
                if request.POST.get(f'checkbox-{category.id}') == 'on':
                    category.book_set.add(book)

            updatedBook = info.get('book')
            book.setCover(updatedBook.cover)
            book.name = updatedBook.name
            book.description = updatedBook.description
            book.pages_number = updatedBook.pages_number
            book.setFile(updatedBook.file)
            book.save(update_fields=['cover', 'name', 'description', 'pages_number', 'file'])

            return redirect('users:user-books', request.user.id)
        return render(request, 'books/book editing.html', {'book': book, 'categories': categories, 'type': 'edit'})
    return HttpResponse(status=403)


class DeleteBook(generic.DeleteView):
    model = Book

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_author:
            return super().post(request)
        return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=403)

    def get_success_url(self):
        return reverse_lazy('users:user-books', kwargs={'pk': self.request.user.id})
