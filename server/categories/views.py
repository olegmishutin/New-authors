from django.shortcuts import render
from django.http import HttpResponse


def categories(request):
    return render(request, 'categories/categories.html', {'isAdmin': False})


def categoriesAdmin(request):
    if request.user.is_superuser:
        return render(request, 'categories/categories.html', {'isAdmin': True})
    return HttpResponse(status=403)


def creatingCategory(request):
    if request.user.is_superuser:
        return render(request, 'categories/creating category.html')
    return HttpResponse(status=403)
