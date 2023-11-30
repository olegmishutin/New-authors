from django.db import models


class Category(models.Model):
    icon = models.ImageField(upload_to='categories_icons')
    name = models.CharField(max_length=250)
    short_description = models.CharField(max_length=400)
    books_number = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
