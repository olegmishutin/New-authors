from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from .models import User
from books.models import Book, Review


def changeUserInfo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(id=request.user.id)

            user.setPhoto(request.FILES.get('photo'))
            user.setFullName(' '.join(request.POST.get('fullName').split()))
            user.short_description = request.POST.get('shortDescription')
            user.save(update_fields=['full_name', 'photo', 'short_description'])

            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('menu')


class UserBooks(generic.DetailView):
    model = User
    template_name = 'profile/profile books.html'
    context_object_name = 'profileUser'

    def createPagination(self, querySet, per_page):
        paginator = Paginator(querySet, per_page)
        return paginator.get_page(self.request.GET.get("page"))

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = User.objects.get(pk=pk)

        if (request.user.id == pk and not request.user.is_author) or not user.is_author:
            return HttpResponse(status=404)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.getBooks(Book, author__id=context.get('profileUser').id)
        context['page_obj'] = self.createPagination(books, 6)
        return context


class UserReviews(UserBooks):
    model = User
    template_name = 'profile/profile comments.html'

    def get(self, request, *args, **kwargs):
        return super(generic.DetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = self.createPagination(Review.objects.filter(user__id=context.get('profileUser').id), 12)
        return context


class UsersAdmin(generic.ListView):
    model = User
    template_name = 'users admin.html'
    paginate_by = 24

    def get_queryset(self):
        return User.objects.exclude(is_author=True)


class DeleteUser(generic.DeleteView):
    model = User

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().post(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
