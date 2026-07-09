from django import forms
from .models import Category
from New_authors.helpers.classes import FormBasedOnType


class CategoryModelForm(FormBasedOnType, forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        fields_to_refresh = ("icon",)

    def edit_refreshed(self):
        self.instance.setIcon(self.cleaned_data.get("icon"))
