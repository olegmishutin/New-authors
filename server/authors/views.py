from django.shortcuts import render
from django.http import HttpResponse


def authors(request):
    return render(request, 'authors/authors.html', {'isAdmin': False})


def authorsAdmin(request):
    if request.user.is_superuser:
        return render(request, 'authors/authors.html', {'isAdmin': True})
    return HttpResponse(status=403)


def sendingEmail(request):
    if request.user.is_superuser:
        return render(request, 'authors/email sending.html')
    return HttpResponse(status=403)
