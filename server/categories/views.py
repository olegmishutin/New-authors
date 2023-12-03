import os
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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


def getCategoryInfoOrErrorRender(request, anotherContent):
    categoryName = ' '.join(request.POST.get('categoryName').split())
    categoryShortDescription = ' '.join(request.POST.get('categoryShortDescription').split())

    errorRender = None
    info = {'categoryIcon': request.FILES.get('categoryIcon'), 'categoryName': categoryName,
            'categoryShortDescription': categoryShortDescription}

    if not categoryName or not categoryShortDescription:
        content = {'categoryNameValue': categoryName, 'categoryShortDescriptionValue': categoryShortDescription}
        content.update(anotherContent)

        errorRender = render(request, 'categories/category editing.html', content)
    return info, errorRender


def creatingCategory(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            info, errorRender = getCategoryInfoOrErrorRender(request, {'type': 'create'})
            if errorRender:
                return errorRender

            Category.objects.create(icon=info.get('categoryIcon'), name=info.get('categoryName'),
                                    short_description=info.get('categoryShortDescription'))
            return redirect('categories:categories-admin')
        return render(request, 'categories/category editing.html', {'type': 'create'})
    return HttpResponse(status=403)


def editCategory(request, pk):
    if request.user.is_superuser:
        category = Category.objects.get(pk=pk)

        if request.method == 'POST':
            content = {'categoryId': pk, 'categoryIconValue': category.icon, 'type': 'edit'}
            info, errorRender = getCategoryInfoOrErrorRender(request, content)

            if errorRender:
                return errorRender

            categoryIcon = info.get('categoryIcon')
            if categoryIcon:
                os.remove(category.icon.path)
                category.icon = categoryIcon

            category.name = info.get('categoryName')
            category.short_description = info.get('categoryShortDescription')
            category.save(update_fields=['icon', 'name', 'short_description'])

            return redirect('categories:categories-admin')
        return render(request, 'categories/category editing.html',
                      {'categoryId': pk, 'categoryIconValue': category.icon, 'categoryNameValue': category.name,
                       'categoryShortDescriptionValue': category.short_description, 'type': 'edit'})
    return HttpResponse(status=403)


class DeleteCategory(generic.DeleteView):
    model = Category
    success_url = reverse_lazy('categories:categories-admin')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().post(request)
        return HttpResponse(status=403)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=403)
