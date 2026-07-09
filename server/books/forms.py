from django import forms
from .models import Book
from New_authors.helpers.classes import FormBasedOnType


class BookModelForm(FormBasedOnType, forms.ModelForm):
    class Meta:
        model = Book
        exclude = ["categories", "author", "publication_date", "reviews"]
        fields_to_refresh = (
            "cover",
            "file",
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def edit_refreshed(self):
        self.instance.setCover(self.cleaned_data.get("cover"))
        self.instance.setFile(self.cleaned_data.get("file"))

    def save(self, commit=True):
        if self.context_type == "edit":
            return super().save(commit)

        return self.Meta.model.objects.create(
            author=self.request.user, **self.cleaned_data
        )
