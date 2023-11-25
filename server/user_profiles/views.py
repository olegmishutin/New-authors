from django.shortcuts import render


def profileComments(request):
    return render(request, 'profile/profile comments.html')

def profileBooks(request):
    return render(request, 'profile/profile books.html')


def usersAdmin(request):
    return render(request, 'profile/users admin.html')