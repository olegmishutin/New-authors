from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import generic
from .models import Category


class Categories(generic.ListView):
    model = Category
    template_name = 'categories/categories.html'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
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
        self.context['categoriesNumber'] = Category.objects.count()
        return self.context


def getCategory(request, anotherContent):
    errorRender = None
    category = Category(icon=request.FILES.get('categoryIcon'), name=' '.join(request.POST.get('categoryName').split()),
                        short_description=' '.join(request.POST.get('categoryShortDescription').split()))

    if not category.name or not category.short_description:
        oldCategory = anotherContent.get('oldCategory')
        if oldCategory:
            category.id = oldCategory.id
            category.icon = oldCategory.icon

        content = {'category': category}
        content.update(anotherContent)

        errorRender = render(request, 'categories/category editing.html', content)
    return category, errorRender


def creatingCategory(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            category, errorRender = getCategory(request, {'type': 'create'})
            if errorRender:
                return errorRender

            category.save()
            return redirect('categories:categories-admin')
        return render(request, 'categories/category editing.html', {'type': 'create'})
    return HttpResponse(status=403)


def editCategory(request, pk):
    if request.user.is_superuser:
        category = Category.objects.get(pk=pk)

        if request.method == 'POST':
            newCategory, errorRender = getCategory(request, {'oldCategory': category, 'type': 'edit'})

            if errorRender:
                return errorRender

            category.setIcon(newCategory.icon)
            category.name = newCategory.name
            category.short_description = newCategory.short_description
            category.save(update_fields=['icon', 'name', 'short_description'])

            return redirect('categories:categories-admin')
        return render(request, 'categories/category editing.html', {'category': category, 'type': 'edit'})
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
