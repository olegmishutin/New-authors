from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, FileResponse
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Book, Review
from .forms import BookModelForm, ReviewModelForm
from categories.models import Category
from authors.mixins import IsAuthMixin
from New_authors.helpers.functions import filterContext
from New_authors.helpers.classes import CustomDeleteView, UserIsAdminMixin


class Books(generic.ListView):
    model = Book
    template_name = "books/books.html"
    paginate_by = 21

    def get_queryset(self):
        self.categories = Category.objects.all()
        self.checkedCategories = [
            category
            for category in self.categories
            if self.request.GET.get(f"category-{category.id}")
        ]

        self.books = (
            Book.getBooks(categories__in=self.checkedCategories)
            if self.checkedCategories
            else Book.getBooks()
        )
        checkboxesFilters = {
            "newBooks": "-publication_date",
            "oldBooks": "publication_date",
            "hightRatingBooks": "-rating",
            "lowRatingBooks": "rating",
            "popularBooks": "-reviewsCount",
        }

        queryset, self.filters_context = filterContext(
            self.request, self.books, checkboxesFilters
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context["isAdmin"] = False
        self.context["categories"] = self.categories
        self.context["checkedCategories"] = self.checkedCategories
        self.context.update(self.filters_context)
        return self.context


class BooksAdmin(UserIsAdminMixin, Books):
    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context["isAdmin"] = True
        self.context["booksNumber"] = self.books.count()
        return self.context


class BookPage(generic.DetailView):
    model = Book
    template_name = "books/book.html"

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        checkboxesFilters = {
            "newReviews": "-date_added",
            "oldReviews": "date_added",
            "hightRatingReviews": "-rating",
            "lowRatingReviews": "rating",
        }

        book = kwargs.get("object")
        reviews = book.review_set.all().select_related("user")

        if self.request.user.is_authenticated:
            self.context["canComment"] = not book.review_set.filter(
                user=self.request.user
            ).exists()

        reviews, filters_context = filterContext(
            self.request, reviews, checkboxesFilters
        )
        self.context.update(filters_context)

        self.context["page_obj"] = Paginator(reviews, 30).get_page(
            self.request.GET.get("page")
        )
        return self.context


@login_required()
def downloadBookFile(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return FileResponse(open(book.file.path, "rb"), as_attachment=True)


@login_required()
@require_POST
def addReview(request, bookId):
    form = ReviewModelForm(
        request.POST, request=request, book_instance=get_object_or_404(Book, pk=bookId)
    )
    if form.is_valid():
        form.save()

    return redirect(request.META.get("HTTP_REFERER") + "#user-review")


class DeleteReview(CustomDeleteView):
    model = Review

    def post(self, request, *args, **kwargs):
        review = get_object_or_404(Review, pk=kwargs.get("pk"))

        if request.user == review.user:
            return super().post(request)
        return HttpResponse(status=403)

    def get_success_url(self):
        return reverse_lazy("users:user-comments", kwargs={"pk": self.request.user.id})


class BookManipulationAbstractView(IsAuthMixin):
    model = Book
    form_class = BookModelForm
    template_name = "books/book editing.html"

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)

        if self.context_type == "edit":
            if request.user.is_author and self.get_object().author == request.user:
                return res
            return self.handle_no_permission()
        return res

    def get_success_url(self):
        return reverse("users:user-books", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["context_type"] = self.context_type
        kwargs["request"] = self.request
        return kwargs


class PublicateBookView(BookManipulationAbstractView, generic.CreateView):
    context_type = "create"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().only("id", "name")
        context["type"] = "publicate"
        return context

    def form_valid(self, form):
        htt_resp = super().form_valid(form)
        self.object.categories.add(
            *[
                category.id
                for category in Category.objects.all().only("id")
                if self.request.POST.get(f"checkbox-{category.id}") == "on"
            ]
        )
        return htt_resp


class EditBookView(BookManipulationAbstractView, generic.UpdateView):
    context_type = "edit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.exclude(
            id__in=self.object.categories.all()
        ).only("id", "name")

        context["type"] = "edit"
        return context

    def form_valid(self, form):
        htt_resp = super().form_valid(form)
        self.object.categories.remove(*self.object.categories.all())
        self.object.categories.add(
            *[
                category.id
                for category in Category.objects.exclude(
                    id__in=self.object.categories.all()
                ).only("id")
                if self.request.POST.get(f"checkbox-{category.id}") == "on"
            ]
        )
        return htt_resp


class DeleteBook(CustomDeleteView):
    model = Book

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs.get("pk"))

        if request.user.is_superuser or request.user == book.author:
            return super().post(request)
        return HttpResponse(status=403)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")
