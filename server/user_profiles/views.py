from django.shortcuts import render
from django.http import HttpResponse


def profileComments(request):
    return render(request, 'profile/profile comments.html')


def profileBooks(request):
    return render(request, 'profile/profile books.html')


def usersAdmin(request):
    if request.user.is_superuser:
        return render(request, 'profile/users admin.html')
    return HttpResponse(status=403)
