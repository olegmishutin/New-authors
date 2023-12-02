from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Category


class Categories(generic.ListView):
    model = Category
    template_name = 'categories/categories.html'
    paginate_by = 12
    context = {}

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context.update(super().get_context_data(**kwargs))
        self.context['isAdmin'] = False
        return self.context


class CategoriesAdmin(Categories):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        self.context['categoriesNumber'] = Category.objects.all().count()
        return self.context


def creatingCategory(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            categoryIcon = request.FILES.get('categoryIcon')
            categoryName = ' '.join(request.POST.get('categoryName').split())
            categoryShortDescription = ' '.join(request.POST.get('categoryShortDescription').split())

            if not categoryName or not categoryShortDescription:
                return render(request, 'categories/creating category.html',
                              {'categoryNameValue': categoryName,
                               'categoryShortDescriptionValue': categoryShortDescription})

            Category.objects.create(icon=categoryIcon, name=categoryName, short_description=categoryShortDescription)
            return redirect('categories:categories-admin')
        return render(request, 'categories/creating category.html')
    return HttpResponse(status=403)
