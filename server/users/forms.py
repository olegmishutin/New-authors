from django import forms
from .models import User


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'photo', 'short_description')
        
    def save(self):
        self.instance.refresh_from_db(fields=('photo',))
        self.instance.setPhoto(self.cleaned_data.get('photo'))
        self.instance.save()
        return self.instance