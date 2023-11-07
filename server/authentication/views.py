from django.shortcuts import render


def signUp(request):
    return render(request, 'authentication/sign-up.html')


def signIn(request):
    return render(request, 'authentication/sign-in.html')
