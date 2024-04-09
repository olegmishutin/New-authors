from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from .models import Category
from New_authors.helpers.classes import CustomDeleteView, AdminListView


class Categories(generic.ListView):
    model = Category
    template_name = 'categories/categories.html'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['isAdmin'] = False
        return self.context


class CategoriesAdmin(Categories, AdminListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        self.context['categoriesNumber'] = Category.objects.count()
        return self.context


def getCategoryInfoFromRequest(request, category=None):
    categoryInfo = {
        'icon': request.FILES.get('categoryIcon'),
        'name': ' '.join(request.POST.get('categoryName').split()),
        'short_description': ' '.join(request.POST.get('categoryShortDescription').split())
    }

    if category and not categoryInfo['icon']:
        categoryInfo['icon'] = category.icon

    categoryForError = category if category else categoryInfo
    for key, value in categoryInfo.items():
        if not value:
            return categoryForError, True
    return categoryInfo, False


def creatingCategory(request):
    if request.user.is_superuser:
        page = 'categories/category editing.html'

        if request.method == 'POST':
            categoryInfo, error = getCategoryInfoFromRequest(request)

            if error:
                return render(request, page, {'category': categoryInfo, 'type': 'create'})
            Category.objects.create(**categoryInfo)

            return redirect('categories:categories-admin')
        return render(request, page, {'type': 'create'})
    return HttpResponse(status=403)


def editCategory(request, pk):
    if request.user.is_superuser:
        page = 'categories/category editing.html'
        category = Category.objects.get(pk=pk)

        if request.method == 'POST':
            categoryInfo, error = getCategoryInfoFromRequest(request, category)

            if error:
                return render(request, page, {'category': category, 'type': 'edit'})

            category.setIcon(categoryInfo['icon'])
            category.name = categoryInfo['name']
            category.short_description = categoryInfo['short_description']
            category.save(update_fields=['icon', 'name', 'short_description'])

            return redirect('categories:categories-admin')
        return render(request, page, {'category': category, 'type': 'edit'})
    return HttpResponse(status=403)


class DeleteCategory(CustomDeleteView):
    model = Category
    success_url = reverse_lazy('categories:categories-admin')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().post(request)
        return HttpResponse(status=403)
