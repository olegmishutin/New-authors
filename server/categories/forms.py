from django import forms
from .models import Category


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        self.context_type = kwargs.pop('context_type', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit = ...):
        if self.context_type == 'edit':
            self.instance.refresh_from_db(fields=['icon'])
            self.instance.setIcon(self.cleaned_data.get('icon'))
            self.instance.save()
            return self.instance
        return super().save(commit)