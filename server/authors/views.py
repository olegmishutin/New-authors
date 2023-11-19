from django.shortcuts import render


def authors(request):
    return render(request, 'authors/authors.html')


def sendingEmail(request):
    return render(request, 'authors/email sending.html')
