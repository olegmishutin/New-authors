from django.urls import path
from . import views

app_name = "categories"
urlpatterns = [
    path("categories/", views.Categories.as_view(), name="categories"),
    path("categories-admin/", views.CategoriesAdmin.as_view(), name="categories-admin"),
    path(
        "creating-category/",
        views.CreateCategoryView.as_view(),
        name="creating-category",
    ),
    path(
        "edit-category/<int:pk>", views.EditCategoryView.as_view(), name="edit-category"
    ),
    path(
        "delete-category/<int:pk>",
        views.DeleteCategory.as_view(),
        name="delete-category",
    ),
]
