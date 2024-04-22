from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from .models import User
from books.models import Book, Review
from New_authors.helpers.classes import CustomDeleteView, AdminListView


def changeUserInfo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = get_object_or_404(User.objects.all().only('full_name', 'photo', 'short_description'),
                                     pk=request.user.id)

            user.setPhoto(request.FILES.get('photo'))
            user.setFullName(' '.join(request.POST.get('fullName').split()))
            user.short_description = request.POST.get('shortDescription')
            user.save(update_fields=['full_name', 'photo', 'short_description'])

            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('menu')


class UserReviews(generic.DetailView):
    model = User
    template_name = 'profile/profile comments.html'
    context_object_name = 'profileUser'

    def createPagination(self, querySet, per_page):
        paginator = Paginator(querySet, per_page)
        return paginator.get_page(self.request.GET.get("page"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(user__id=context.get('profileUser').id).select_related(
            'book').prefetch_related('book__review_set').only('text', 'rating', 'book__id', 'book__name')

        context['page_obj'] = self.createPagination(reviews, 12)
        return context


class UserBooks(UserReviews):
    template_name = 'profile/profile books.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk'))

        if user.is_author:
            return super(generic.DetailView, self).get(request, *args, **kwargs)
        return HttpResponse(status=404)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.getBooks(author__id=context.get('profileUser').id)
        context['page_obj'] = self.createPagination(books, 6)
        return context


class UsersAdmin(AdminListView):
    model = User
    queryset = User.objects.exclude(is_author=True).only('full_name', 'photo')
    template_name = 'users admin.html'
    paginate_by = 24


class DeleteUser(CustomDeleteView):
    model = User

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().post(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
