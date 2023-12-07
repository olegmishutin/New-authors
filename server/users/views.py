from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from .models import User
from books.models import Book


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

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = User.objects.get(pk=pk)

        if (not request.user.is_author and request.user.id == pk) or not user.is_author:
            return HttpResponse(status=404)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.getAllWithStatistics(Book, author__id=context.get('profileUser').id)

        paginator = Paginator(books, 6)
        pageNumber = self.request.GET.get("page")
        pageObject = paginator.get_page(pageNumber)

        context['page_obj'] = pageObject
        return context


def userComments(request, pk):
    return render(request, 'profile/profile comments.html')


def usersAdmin(request):
    if request.user.is_superuser:
        return render(request, 'users admin.html')
    return HttpResponse(status=403)
