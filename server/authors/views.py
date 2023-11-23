from django.shortcuts import render


def authors(request):
    return render(request, 'authors/authors.html', {'isAdmin': False})


def authorsAdmin(request):
    return render(request, 'authors/authors.html', {'isAdmin': True})


def sendingEmail(request):
    return render(request, 'authors/email sending.html')
