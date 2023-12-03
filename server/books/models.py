from django.db import models
from users.models import User
from categories.models import Category


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    categories = models.ManyToManyField(Category, db_table='BookCategories', verbose_name='Категории')
    name = models.CharField(max_length=250, verbose_name='Название')
    cover = models.ImageField(upload_to='books_images', verbose_name='Обложка')
    pages_number = models.IntegerField(verbose_name='Количесвто страниц')
    description = models.TextField(verbose_name='Описание')
    creation_date = models.DateField(auto_now=True, verbose_name='Дата создания')
    file = models.FileField(upload_to='books_files', verbose_name='Файл')

    class Meta:
        db_table = 'Book'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name


class Review(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField()
    date_added = models.DateField(auto_now=True)

    class Meta:
        db_table = 'Review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:20]
