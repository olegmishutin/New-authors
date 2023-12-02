from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from email_validator import validate_email, EmailNotValidError
from users.models import User


def errorRender(request, template, errorType, message):
    return render(request, template, {errorType: message, 'fullNameValue': request.POST.get('fullName'),
                                      'usernameValue': request.POST.get('username'),
                                      'emailValue': request.POST.get('email'),
                                      'passwordValue': request.POST.get('password')})


def signUp(request):
    if request.method == 'POST':
        postData = dict(request.POST)
        currentTemplate = 'authentication/sign-up.html'

        for key, value in postData.items():
            postData[key] = value = ' '.join(value[0].split())
            if not value:
                return errorRender(request, currentTemplate, f'{key}Error', 'Это поле не может быть пустым!')

        try:
            email = validate_email(postData.get('email'), check_deliverability=True)
            postData['email'] = email.normalized
        except EmailNotValidError:
            return errorRender(request, currentTemplate, 'emailError', 'Недействительный адрес почты!')

        if ' ' in postData.get('username'):
            return errorRender(request, currentTemplate, 'usernameError',
                               'Имя пользователя не может содержать пробелы!')

        if ' ' in postData.get('password'):
            return errorRender(request, currentTemplate, 'passwordError', 'Пароль не может содержать пробелы!')

        if len(postData.get('password')) < 6:
            return errorRender(request, currentTemplate, 'passwordError', 'Пароль должен быть больше 5 символов!')

        try:
            user = User.objects.create_user(username=postData.get('username'), email=postData.get('email'),
                                            password=postData.get('password'), full_name=postData.get('fullName'),
                                            is_author=True if postData.get('userType') == 'author' else False)
        except IntegrityError:
            return errorRender(request, currentTemplate, 'usernameError', 'Такое имя пользователя уже занято!')
        return redirect('authentication:sign-in')

    if request.user.is_anonymous:
        return render(request, 'authentication/sign-up.html')
    return redirect('menu')


def signIn(request):
    if request.method == 'POST':
        postData = dict(request.POST)
        currentTemplate = 'authentication/sign-in.html'

        if not postData.get('username')[0] or not postData.get('password')[0]:
            return errorRender(request, currentTemplate, f'usernameError', 'Поля не могут быть пустыми!')

        user = authenticate(username=postData.get('username')[0], password=postData.get('password')[0])
        if user is not None:
            if not user.full_name:
                user.full_name = user.username
                user.save(update_fields=['full_name'])
            login(request, user)
            return redirect('menu')
        return errorRender(request, currentTemplate, 'usernameError', 'Пользователь с таким именем и паролем не найден')

    if request.user.is_anonymous:
        return render(request, 'authentication/sign-in.html')
    return redirect('menu')


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('authentication:sign-in')
