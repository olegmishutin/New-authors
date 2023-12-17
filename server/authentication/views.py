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
    currentTemplate = 'authentication/sign-up.html'

    if request.method == 'POST':
        postData = dict(request.POST)

        for key, value in postData.items():
            postData[key] = value = ' '.join(value[0].split())
            if not value:
                return errorRender(request, currentTemplate, f'{key}Error', 'Это поле не может быть пустым!')

        fullName = postData.get('fullName')
        username = postData.get('username')
        email = postData.get('email')
        password = postData.get('password')
        userType = postData.get('userType')

        try:
            email = validate_email(email, check_deliverability=True).normalized
        except EmailNotValidError:
            return errorRender(request, currentTemplate, 'emailError', 'Недействительный адрес почты!')

        if ' ' in username:
            return errorRender(request, currentTemplate, 'usernameError',
                               'Имя пользователя не может содержать пробелы!')

        if ' ' in password:
            return errorRender(request, currentTemplate, 'passwordError', 'Пароль не может содержать пробелы!')

        if len(password) < 6:
            return errorRender(request, currentTemplate, 'passwordError', 'Пароль должен быть больше 5 символов!')

        try:
            user = User.objects.create_user(username=username, email=email, password=password, full_name=fullName,
                                            is_author=True if userType == 'author' else False)
        except IntegrityError:
            return errorRender(request, currentTemplate, 'usernameError', 'Такое имя пользователя уже занято!')
        return redirect('authentication:sign-in')

    if request.user.is_anonymous:
        return render(request, currentTemplate)
    return redirect('menu')


def signIn(request):
    currentTemplate = 'authentication/sign-in.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return errorRender(request, currentTemplate, f'usernameError', 'Поля не могут быть пустыми!')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('menu')
        return errorRender(request, currentTemplate, 'usernameError', 'Пользователь с таким именем и паролем не найден')

    if request.user.is_anonymous:
        return render(request, currentTemplate)
    return redirect('menu')


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('authentication:sign-in')
