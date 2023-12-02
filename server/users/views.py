from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User


def changeUserInfo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            def setNewInfo(oldInfo, newInfo):
                return newInfo if newInfo else oldInfo

            user = User.objects.get(id=request.user.id)

            photo = request.FILES.get('photo')
            fullName = ' '.join(request.POST.get('fullName').split())
            shortDescription = request.POST.get('shortDescription')

            user.photo = setNewInfo(user.photo, photo)
            user.full_name = setNewInfo(user.full_name, fullName)
            user.short_description = shortDescription

            user.save(update_fields=['full_name', 'photo', 'short_description'])
    return redirect(request.META.get('HTTP_REFERER'))


def userComments(request):
    return render(request, 'profile/profile comments.html')


def userBooks(request):
    return render(request, 'profile/profile books.html')


def usersAdmin(request):
    if request.user.is_superuser:
        return render(request, 'users admin.html')
    return HttpResponse(status=403)
