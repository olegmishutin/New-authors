from django.shortcuts import render


def categories(request):
    return render(request, 'categories/categories.html', {'isAdmin': False})


def categoriesAdmin(request):
    return render(request, 'categories/categories.html', {'isAdmin': True})


def creatingCategory(request):
    return render(request, 'categories/creating category.html')
