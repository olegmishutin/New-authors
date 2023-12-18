from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pages_number')
    fieldsets = [
        ('Основная информация', {'fields': ['author', 'categories', 'name', 'publication_date', 'file']}),
        ('Второстепенная информация', {'fields': ['cover', 'pages_number', 'description']})
    ]
    readonly_fields = ('author', 'name', 'file', 'publication_date', 'cover', 'pages_number', 'description')
    search_fields = ('name',)
    list_filter = ('publication_date', 'categories')


admin.site.register(Book, BookAdmin)
