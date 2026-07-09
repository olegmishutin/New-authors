from django.urls import reverse_lazy
from New_authors.helpers.classes import UserIsAdminMixin
from .models import Category
from .forms import CategoryModelForm


class AdminCategoryUseCaseMixin(UserIsAdminMixin):
    model = Category
    form_class = CategoryModelForm
    template_name = "categories/category editing.html"
    success_url = reverse_lazy("categories:categories-admin")

    context_type: str = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = self.context_type
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["context_type"] = self.context_type
        return kwargs
