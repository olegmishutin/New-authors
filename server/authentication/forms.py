from django import forms
from django.core.validators import MinLengthValidator
from users.models import User


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "full_name", "is_author", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].validators = [MinLengthValidator(6)]

    def save(self, commit=...):
        return User.objects.create_user(**self.cleaned_data)
