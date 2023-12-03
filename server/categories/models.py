from django.db import models


class Category(models.Model):
    icon = models.ImageField(upload_to='categories_icons', verbose_name='Иконка')
    name = models.CharField(max_length=250, verbose_name='Название')
    short_description = models.CharField(max_length=400, verbose_name='Краткое описание')
    books_number = models.BigIntegerField(default=0, verbose_name='Количество книг')

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
