from django import forms
from .models import Book, Review
from New_authors.helpers.classes import FormBasedOnType


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("text", "rating")
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('request').user
        self.book_instance = kwargs.pop('book_instance')
        super().__init__(*args, **kwargs)
        
    def save(self):
        review, _ = self.book_instance.review_set.get_or_create(
            user=self.user, defaults={**self.cleaned_data}
        )
        return review


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
