from django.contrib import admin
from .models import Book, Review


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pages_number')
    fieldsets = [
        ('Основная информация', {'fields': ['author', 'categories', 'name', 'publication_date', 'file']}),
        ('Второстепенная информация', {'fields': ['cover', 'pages_number', 'description']})
    ]
    readonly_fields = ('author', 'name', 'file', 'publication_date', 'cover', 'pages_number', 'description')
    search_fields = ('name',)
    list_filter = ('publication_date', 'categories')

    def delete_queryset(self, request, queryset):
        for book in queryset:
            book.delete()


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating')
    fieldsets = [
        ('Основная информация', {'fields': ['user', 'book', 'rating', 'date_added']}),
        ('Второстепенная информация', {'fields': ['text']})
    ]
    readonly_fields = ('date_added', 'user', 'book', 'rating', 'text')
    search_fields = ('text',)
    list_filter = ('rating', 'date_added')


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
