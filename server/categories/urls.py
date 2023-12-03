from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('categories/', views.Categories.as_view(), name='categories'),
    path('categories-admin/', views.CategoriesAdmin.as_view(), name='categories-admin'),
    path('creating-category/', views.creatingCategory, name='creating-category'),
    path('edit-category/<int:pk>', views.editCategory, name='edit-category'),
    path('delete-category/<int:pk>', views.DeleteCategory.as_view(), name='delete-category')
]
