from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from email_validator import validate_email, EmailNotValidError
from user_profiles.models import Profile


def errorRender(request, errorType, message):
    return render(request, 'authentication/sign-up.html',
                  {errorType: message, 'fullNameValue': request.POST.get('fullName'),
                   'usernameValue': request.POST.get('username'), 'emailValue': request.POST.get('email'),
                   'passwordValue': request.POST.get('password')})


def signUp(request):
    if request.method == 'POST':
        postData = dict(request.POST)

        for key, value in postData.items():
            postData[key] = value = ' '.join(value[0].split())
            if not value:
                return errorRender(request, f'{key}Error', 'Это поле не может быть пустым!')

        try:
            email = validate_email(postData.get('email'), check_deliverability=True)
            postData['email'] = email.normalized
        except EmailNotValidError:
            return errorRender(request, 'emailError', 'Недействительный адрес почты!')

        if ' ' in postData.get('password'):
            return errorRender(request, 'passwordError', 'Пароль не может содержать пробелы!')

        if len(postData.get('password')) < 6:
            return errorRender(request, 'passwordError', 'Пароль должен быть больше 5 символов!')

        try:
            user = User.objects.create_user(username=postData.get('username'), email=postData.get('email'),
                                            password=postData.get('password'))
        except IntegrityError:
            return errorRender(request, 'usernameError', 'Такое имя пользователя уже занято!')

        is_author = True if postData.get('userType') == 'author' else False
        Profile.objects.create(user=user, full_name=postData.get('fullName'), is_author=is_author)

        return redirect('authentication:sign-in')
    return render(request, 'authentication/sign-up.html')


def signIn(request):
    return render(request, 'authentication/sign-in.html')
