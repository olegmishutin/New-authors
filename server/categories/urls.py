from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('categories/', views.Categories.as_view(), name='categories'),
    path('categories-admin/', views.CategoriesAdmin.as_view(), name='categories-admin'),
    path('creating-category/', views.creatingCategory, name='creating-category')
]
