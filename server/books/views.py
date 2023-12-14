from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Avg
from .models import Book, Review
from categories.models import Category


class Books(generic.ListView):
    model = Book
    template_name = 'books/books.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['isAdmin'] = False

        self.context['categories'] = Category.objects.all()
        self.context['checkedCategories'] = []

        filters = []
        categories = []

        for category in self.context['categories']:
            if self.request.GET.get(f'category-{category.id}'):
                categories.append(int(category.id))
                self.context['checkedCategories'].append(category)

        books = Book.getBooks(Book, categories__id__in=categories) if categories else Book.getBooks(Book)
        checkboxesFilters = {'newBooks': '-publication_date', 'oldBooks': 'publication_date',
                             'hightRatingBooks': '-rating', 'lowRatingBooks': 'rating', 'popularBooks': '-reviewsCount'}

        for checkbox, filter in checkboxesFilters.items():
            if self.request.GET.get(checkbox):
                filters.append(filter)
                self.context[checkbox] = 'checked'

        books = books.order_by(*filters)
        self.context['page_obj'] = Paginator(books, 21).get_page(self.request.GET.get('page'))
        return self.context


class BooksAdmin(Books):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        self.context['booksNumber'] = Book.objects.all().count()
        return self.context


class BookPage(generic.DetailView):
    model = Book
    template_name = 'books/book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = kwargs.get('object').review_set.all()

        filters = []
        checkboxesFilters = {'newReviews': '-date_added', 'oldReviews': 'date_added',
                             'hightRatingReviews': '-rating', 'lowRatingReviews': 'rating'}

        for checkbox, filter in checkboxesFilters.items():
            if self.request.GET.get(checkbox):
                filters.append(filter)
                context[checkbox] = 'checked'

        reviews = reviews.order_by(*filters)
        context['page_obj'] = Paginator(reviews, 30).get_page(self.request.GET.get('page'))
        return context


def downloadBookFile(request, pk):
    book = Book.objects.get(pk=pk)
    return FileResponse(open(book.file.path, 'rb'), as_attachment=True)


def addReview(request, bookId):
    if request.method == 'POST':
        book = Book.objects.get(pk=bookId)

        reviewText = ' '.join(request.POST.get('reviewText').split())
        reviewRating = request.POST.get('reviewRating')

        if not reviewText or not reviewRating:
            return redirect(request.META.get('HTTP_REFERER') + '#user-review')

        book.review_set.create(user=request.user, text=reviewText, rating=reviewRating)
        return redirect(request.META.get('HTTP_REFERER') + '#user-review')
    return HttpResponse(status=404)


class DeleteReview(generic.DeleteView):
    model = Review

    def post(self, request, *args, **kwargs):
        review = Review.objects.get(pk=kwargs.get('pk'))

        if request.user == review.user:
            return super().post(request)
        return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    def get_success_url(self):
        return reverse_lazy('users:user-comments', kwargs={'pk': self.request.user.id})


def getBookInfo(request, anotherContent):
    book = Book(author=request.user, cover=request.FILES.get('bookCover'),
                name=' '.join(request.POST.get('bookName').split()), description=request.POST.get('bookDesciption'),
                pages_number=request.POST.get('bookPagesNumber'), file=request.FILES.get('bookFile'))

    errorRender = None
    bookCategories = []

    for category in Category.objects.all():
        if request.POST.get(f'checkbox-{category.id}') == 'on':
            bookCategories.append(category)

    if not book.name or not bookCategories:
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
    book = Book.objects.get(pk=pk)

    if request.user.is_author and book.author == request.user:
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
        if request.user.is_superuser or (request.user == Book.objects.get(pk=kwargs.get('pk')).author):
            return super().post(request)
        return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
