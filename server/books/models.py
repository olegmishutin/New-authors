import os
from django.db import models
from django.db.models import Avg, Count
from users.models import User
from categories.models import Category
from New_authors.helpers.functions import changeFile


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    categories = models.ManyToManyField(Category, db_table='BookCategories', verbose_name='Категории')
    name = models.CharField(max_length=250, verbose_name='Название')
    cover = models.ImageField(upload_to='books_images', verbose_name='Обложка')
    pages_number = models.IntegerField(verbose_name='Количесвто страниц')
    description = models.TextField(verbose_name='Описание')
    publication_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    file = models.FileField(upload_to='books_files', verbose_name='Файл')
    reviews = models.ManyToManyField(User, related_name='books_reviews', through='Review', verbose_name='Отзывы')

    class Meta:
        db_table = 'Book'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def setCover(self, newCover):
        self.cover = changeFile(self.cover, newCover)

    def setFile(self, newFile):
        self.file = changeFile(self.file, newFile)

    @classmethod
    def getBooks(cls, **kwargs):
        return cls.objects.filter(**kwargs).only('id', 'name', 'cover').annotate(
            rating=Avg('review__rating', default=0), reviewsCount=Count('review'))

    def getRating(self):
        return round(self.review_set.all().aggregate(rating=Avg('rating', default=0)).get('rating'), 1)

    def getReviewsCount(self):
        return self.review_set.all().count()

    def delete(self, using=None, keep_parents=False):
        changeFile(self.cover, deleteOnly=True)
        changeFile(self.file, deleteOnly=True)
        return super(Book, self).delete()

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    text = models.TextField(verbose_name='Текст')
    rating = models.FloatField(verbose_name='Рейтинг')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'Review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['user', 'book']

    def __str__(self):
        return self.text[:20]
