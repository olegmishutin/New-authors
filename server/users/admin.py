from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_author', 'is_staff')
    fieldsets = [
        ('Основная информация', {'fields': ['username', 'full_name', 'email', 'date_joined']}),
        ('Статусы', {'fields': ['is_staff', 'is_active', 'is_author']}),
        ('Второстепенная информация', {'fields': ['photo', 'short_description']})
    ]
    search_fields = ('username', 'full_name', 'email')
    list_filter = ('is_staff', 'is_active', 'is_author')
    readonly_fields = ('username', 'photo', 'short_description', 'full_name', 'email', 'date_joined')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
