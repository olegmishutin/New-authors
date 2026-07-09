from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from .models import Category
from .mixins import AdminCategoryUseCaseMixin
from New_authors.helpers.classes import CustomDeleteView, UserIsAdminMixin


class Categories(generic.ListView):
    model = Category
    queryset = Category.objects.all().prefetch_related('book_set')
    template_name = 'categories/categories.html'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['isAdmin'] = False
        return self.context


class CategoriesAdmin(UserIsAdminMixin, Categories):
    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        self.context['categoriesNumber'] = self.queryset.count()
        return self.context
    

class CreateCategoryView(AdminCategoryUseCaseMixin, generic.CreateView):
    context_type = 'create'
    

class EditCategoryView(AdminCategoryUseCaseMixin, generic.UpdateView):
    context_type = 'edit'


class DeleteCategory(CustomDeleteView):
    model = Category
    success_url = reverse_lazy('categories:categories-admin')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().post(request)
        return HttpResponse(status=403)
