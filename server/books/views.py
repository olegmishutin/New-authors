from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Book, Review
from categories.models import Category
from New_authors.helpers.functions import filterContext
from New_authors.helpers.classes import CustomDeleteView, AdminListView


class Books(generic.ListView):
    model = Book
    template_name = 'books/books.html'
    paginate_by = 21

    def get_queryset(self):
        self.categories = Category.objects.all()
        self.checkedCategories = [category for category in self.categories if
                                  self.request.GET.get(f'category-{category.id}')]

        self.books = Book.getBooks(categories__in=self.checkedCategories) if self.checkedCategories else Book.getBooks()
        checkboxesFilters = {'newBooks': '-publication_date', 'oldBooks': 'publication_date',
                             'hightRatingBooks': '-rating', 'lowRatingBooks': 'rating', 'popularBooks': '-reviewsCount'}

        self.filteredContext = filterContext(self.request, self.books, checkboxesFilters)
        return self.filteredContext.get('queryset')

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['isAdmin'] = False
        self.context['categories'] = self.categories
        self.context['checkedCategories'] = self.checkedCategories
        self.context.update(self.filteredContext.get('context'))
        return self.context


class BooksAdmin(Books, AdminListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        self.context['booksNumber'] = self.books.count()
        return self.context


class BookPage(generic.DetailView):
    model = Book
    template_name = 'books/book.html'

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        checkboxesFilters = {'newReviews': '-date_added', 'oldReviews': 'date_added',
                             'hightRatingReviews': '-rating', 'lowRatingReviews': 'rating'}

        book = kwargs.get('object')
        reviews = book.review_set.all().select_related('user')

        if self.request.user.is_authenticated:
            self.context['canComment'] = not book.review_set.filter(user=self.request.user).exists()

        filteredContext = filterContext(self.request, reviews, checkboxesFilters)
        self.context.update(filteredContext.get('context'))

        reviews = filteredContext.get('queryset')
        self.context['page_obj'] = Paginator(reviews, 30).get_page(self.request.GET.get('page'))
        return self.context


@login_required()
def downloadBookFile(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return FileResponse(open(book.file.path, 'rb'), as_attachment=True)


@login_required()
def addReview(request, bookId):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=bookId)

        reviewText = ' '.join(request.POST.get('reviewText').split())
        reviewRating = request.POST.get('reviewRating')

        if reviewText and reviewRating:
            review, created = book.review_set.get_or_create(user=request.user, defaults={
                'text': reviewText, 'rating': reviewRating
            })
        return redirect(request.META.get('HTTP_REFERER') + '#user-review')
    return HttpResponse(status=404)


class DeleteReview(CustomDeleteView):
    model = Review

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get('pk'))

        if request.user == review.user:
            return super().post(request)
        return HttpResponse(status=403)

    def get_success_url(self):
        return reverse_lazy('users:user-comments', kwargs={'pk': self.request.user.id})


def getBookInfoFromRequest(request, categories, book=None):
    bookInfo = {
        'author': request.user,
        'cover': request.FILES.get('bookCover'),
        'name': ' '.join(request.POST.get('bookName').split()),
        'description': request.POST.get('bookDesciption'),
        'pages_number': request.POST.get('bookPagesNumber'),
        'file': request.FILES.get('bookFile')
    }

    if book and not bookInfo['cover']:
        bookInfo['cover'] = book.cover

    if book and not bookInfo['file']:
        bookInfo['file'] = book.file

    bookForError = book if book else bookInfo
    bookCategories = [category for category in categories if request.POST.get(f'checkbox-{category.id}') == 'on']

    for key, value in bookInfo.items():
        if not value:
            return bookForError, None, True
    return bookInfo, bookCategories, False


def publicateBook(request):
    if request.user.is_author:
        page = 'books/book editing.html'
        categories = Category.objects.all().only('name')

        if request.method == 'POST':
            bookInfo, bookCategories, error = getBookInfoFromRequest(request, categories)
            if error:
                return render(request, page, {'book': bookInfo, 'categories': categories, 'type': 'publicate'})

            book = Book.objects.create(**bookInfo)
            book.categories.add(*bookCategories)

            return redirect('users:user-books', request.user.id)
        return render(request, page, {'categories': categories, 'type': 'publicate'})
    return HttpResponse(status=403)


def editBook(request, pk):
    page = 'books/book editing.html'

    book = get_object_or_404(Book.objects.all().select_related('author').only(
        'name', 'cover', 'pages_number', 'description', 'file', 'author__photo', 'author__full_name',
        'author__short_description'), pk=pk)

    if request.user.is_author and book.author == request.user:
        notBookCategories = Category.objects.exclude(id__in=book.categories.all()).only('name')

        if request.method == 'POST':
            bookInfo, bookCategories, error = getBookInfoFromRequest(request, Category.objects.all(), book)
            if error:
                return render(request, page, {'book': book, 'categories': notBookCategories, 'type': 'edit'})

            book.categories.remove(*book.categories.all())
            book.categories.add(*bookCategories)

            book.setCover(bookInfo['cover'])
            book.name = bookInfo['name']
            book.description = bookInfo['description']
            book.pages_number = bookInfo['pages_number']
            book.setFile(bookInfo['file'])
            book.save(update_fields=['cover', 'name', 'description', 'pages_number', 'file'])

            return redirect('users:user-books', request.user.id)
        return render(request, page, {'book': book, 'categories': notBookCategories, 'type': 'edit'})
    return HttpResponse(status=403)


class DeleteBook(CustomDeleteView):
    model = Book

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get('pk'))

        if request.user.is_superuser or request.user == book.author:
            return super().post(request)
        return HttpResponse(status=403)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
