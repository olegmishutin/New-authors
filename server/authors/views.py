from django.shortcuts import render


def authors(request):
    return render(request, 'authors/authors.html')
