from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description')
    fieldsets = [
        ('Информация', {'fields': ['icon', 'name', 'short_description']})
    ]
    search_fields = ('name',)

    def delete_queryset(self, request, queryset):
        for category in queryset:
            category.delete()


admin.site.register(Category, CategoryAdmin)
