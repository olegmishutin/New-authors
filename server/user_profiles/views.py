from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile


def changeProfileInfo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            def setNewInfo(oldInfo, newInfo):
                return newInfo if newInfo else oldInfo

            profile = Profile.objects.get(user__id=request.user.id)

            photo = request.FILES.get('photo')
            fullName = ' '.join(request.POST.get('fullName').split())
            shortDescription = request.POST.get('shortDescription')

            profile.photo = setNewInfo(profile.photo, photo)
            profile.full_name = setNewInfo(profile.full_name, fullName)
            profile.short_description = shortDescription

            profile.save(update_fields=['full_name', 'photo', 'short_description'])
    return redirect(request.META.get('HTTP_REFERER'))


def profileComments(request):
    return render(request, 'profile/profile comments.html')


def profileBooks(request):
    return render(request, 'profile/profile books.html')


def usersAdmin(request):
    if request.user.is_superuser:
        return render(request, 'profile/users admin.html')
    return HttpResponse(status=403)
