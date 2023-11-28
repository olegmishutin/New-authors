from django.db import models
from user_profiles.models import Profile
from categories.models import Category


class Book(models.Model):
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, db_table='BookCategories')
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='books_images')
    pages_number = models.IntegerField()
    description = models.TextField()
    date_added = models.DateField(auto_now=True)
    file = models.FileField(upload_to='books_files')

    class Meta:
        db_table = 'Book'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name


class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
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
