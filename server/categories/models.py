import os
from django.db import models


class Category(models.Model):
    icon = models.ImageField(upload_to='categories_icons', verbose_name='Иконка')
    name = models.CharField(max_length=250, verbose_name='Название')
    short_description = models.CharField(max_length=400, verbose_name='Краткое описание')

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def delete(self, using=None, keep_parents=False):
        os.remove(self.icon.path)
        return super(Category, self).delete()

    def __str__(self):
        return self.name
